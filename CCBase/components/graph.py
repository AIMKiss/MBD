import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from graphviz import Digraph
from typing import Dict, List, Optional

class Graph:
    def __init__(self) -> None:
        self.graph: nx.Graph = nx.Graph()

    def create_graph(self, edgelist: pd.DataFrame, source: str = "source", target: str = "target") -> None:
        self.graph = nx.from_pandas_edgelist(edgelist, source=source, target=target, create_using=self.graph)

    def load_graph(self, graph: nx.Graph) -> None:
        self.graph = graph

    def visualize_graph(self, image_path: str, labels: Optional[List[int]] = None) -> None:
        pos: Dict[int, List[float]] = nx.spring_layout(self.graph, seed=42)
        fig, ax = plt.subplots(figsize=(20, 15))
        nx.draw_networkx_edges(self.graph, pos, alpha=0.5)
        
        if labels is not None:
            node_labels: List[int] = [labels[node] if node < len(labels) else 0 for node in range(len(self.graph.nodes()))]
            nx.draw_networkx_nodes(self.graph, pos, node_color=node_labels, cmap=plt.cm.rainbow, node_size=300)
        else:
            nx.draw_networkx_nodes(self.graph, pos, node_color='blue', node_size=300)
        
        nx.draw_networkx_labels(self.graph, pos, font_size=10)
        font = {"color": "k", "fontweight": "bold", "fontsize": 12}
        ax.set_title("Graph Visualization", font)
        
        if labels is not None:
            font["color"] = "r"
            ax.text(0.80, 0.05, "node color = cluster label", horizontalalignment="center", transform=ax.transAxes, fontdict=font)
        
        ax.margins(0.1, 0.05)
        fig.tight_layout()
        plt.axis("off")
        plt.savefig(image_path)
        plt.close(fig)

    def visualize_graph_without_clustering(self, image_path: str) -> None:
        self.visualize_graph(image_path)

    def visualize_table_schema(self, image_path: str, labels: List[int]) -> None:
        dot = Digraph(comment='Table Schema')
        
        clusters = set(labels)
        for cluster in clusters:
            with dot.subgraph(name=f'cluster_{cluster}') as c:
                c.attr(style='filled', color='lightgrey')
                c.node_attr.update(style='filled', color='white')
                cluster_nodes = [node for node in self.graph.nodes() if labels[node] == cluster]
                for node in cluster_nodes:
                    c.node(node)
        
        for edge in self.graph.edges():
            dot.edge(edge[0], edge[1])
        
        dot.render(image_path, format='png', cleanup=True)


class DatabaseGraph(Graph):
    def __init__(self, user: str, password: str, host: str, database: str) -> None:
        super().__init__()
        self.engine = create_engine(
            f'mssql+pyodbc://{user}:{password}@{host}/{database}?'
            'TrustServerCertificate=yes&'
            'driver=ODBC+Driver+17+for+SQL+Server'
        )
        self.table_dependencies: pd.DataFrame
        self.table_details: pd.DataFrame

    def fetch_table_dependencies(self) -> None:
        query = """
        SELECT [source] = baseTable.name,
               [source_schema] = schema_name(baseTable.schema_id),
               [target] = refdTable.name,
               [target_schema] = schema_name(refdTable.schema_id),
               [link] = baseTable.name + '.' + baseCol.name + '->' +  refdTable.name + '.' + refdCol.name,
               [qry] = 'select link=''' + baseTable.name + '.' + baseCol.name + '->' +  refdTable.name + '.' + refdCol.name + ''',source=''' + baseTable.name + ''',source_count= (select count(1) from ' + schema_name(baseTable.schema_id) + '.' + baseTable.name + '), ' + 
                       'target=''' + refdTable.name + ''',target_count= (select count(1) from '+ schema_name(refdTable.schema_id) + '.' + refdTable.name + '), ' +
                       'fk_count= (select count(1) from ' + schema_name(baseTable.schema_id) + '.' + baseTable.name + ' where ' + baseCol.name + ' is not null)'
        FROM [sys].[foreign_key_columns] fkc
        OUTER APPLY (SELECT * FROM sys.tables o WHERE o.object_id = fkc.[parent_object_id]) baseTable
        OUTER APPLY (SELECT * FROM sys.columns o WHERE o.object_id = fkc.[parent_object_id] AND o.column_id = fkc.parent_column_id) baseCol
        OUTER APPLY (SELECT * FROM sys.tables o WHERE o.object_id = fkc.[referenced_object_id]) refdTable
        OUTER APPLY (SELECT * FROM sys.columns o WHERE o.object_id = fkc.[referenced_object_id] AND o.column_id = fkc.referenced_column_id) refdCol
        """
        self.table_dependencies = pd.read_sql(query, self.engine)

    def create_graph(self) -> None:
        super().create_graph(self.table_dependencies, source="source", target="target")

    def fetch_table_details(self) -> None:
        query = """
        SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        """
        self.table_details = pd.read_sql(query, self.engine)

    def visualize_table_schema(self, image_path: str, labels: List[int]) -> None:
        dot = Digraph(comment='Table Schema')
        
        labels_dict: Dict[str, int] = {node: labels[i] for i, node in enumerate(self.graph.nodes())}

        clusters = set(labels_dict.values())
        for cluster in clusters:
            with dot.subgraph(name=f'cluster_{cluster}') as c:
                c.attr(style='filled', color='lightgrey')
                c.node_attr.update(style='filled', color='white', shape='plaintext')
                cluster_nodes = [node for node in self.graph.nodes() if labels_dict[node] == cluster]
                for node in cluster_nodes:
                    table_details = self.table_details[self.table_details['TABLE_NAME'] == node]
                    label = f"<<TABLE BORDER='0' CELLBORDER='1' CELLSPACING='0'><TR><TD COLSPAN='2'><B>{node}</B></TD></TR>"
                    for _, row in table_details.iterrows():
                        label += f"<TR><TD>{row['COLUMN_NAME']}</TD><TD>{row['DATA_TYPE']}</TD></TR>"
                    label += "</TABLE>>"
                    c.node(node, label=label)
        
        for edge in self.graph.edges():
            dot.edge(edge[0], edge[1])
        
        dot.render(image_path, format='png', cleanup=True)