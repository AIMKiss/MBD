from components.database import Database
from components.graph import DatabaseGraph
from typing import Any, Dict

class DatabaseFacade:
    def __init__(self, user: str, password: str, host: str, database: str) -> None:
        self.db: Database = Database(user, password, host, database)
        self.graph: DatabaseGraph = DatabaseGraph(user, password, host, database)

    def test_connection(self) -> bool:
        return self.db.test_connection()

    def fetch_table_dependencies(self) -> None:
        self.graph.fetch_table_dependencies()

    def create_graph(self) -> None:
        self.graph.create_graph()

    def visualize_graph_without_clustering(self, image_path: str) -> None:
        self.graph.visualize_graph_without_clustering(image_path)

    def load_graph(self, G: Any) -> None:
        self.graph.load_graph(G)

    def fetch_table_details(self) -> Dict[str, Any]:
        return self.graph.fetch_table_details()

    def visualize_table_schema(self, image_path: str, labels: Dict[str, str]) -> None:
        self.graph.visualize_table_schema(image_path, labels)