from node2vec import Node2Vec
from sklearn.cluster import KMeans
import networkx as nx
from sklearn.ensemble import GradientBoostingClassifier

from typing import List, Any
from components.cluster.base_cluster import BaseCluster

class RandomWalkCluster(BaseCluster):    
    def preprocess_graph(self, G: nx.Graph) -> None:
        pass

    def cluster_graph(self, G: nx.Graph, n_clusters: int) -> List[int]:
        cluster_labels: List[int] = self._random_walk_clustering(G, num_clusters=n_clusters)
        return cluster_labels

    def postprocess_results(self, G: nx.Graph, labels: List[int]) -> None:
        for i, node in enumerate(G.nodes()):
            G.nodes[node]['cluster'] = labels[i]

    def _random_walk_clustering(self, G: nx.Graph, 
                                num_clusters: int = 5, 
                                dimensions: int = 64, 
                                walk_length: int = 10, 
                                num_walks: int = 200, 
                                workers: int = 10) -> List[int]:
        
        node2vec: Node2Vec = Node2Vec(G, 
                                      dimensions=dimensions, 
                                      walk_length=walk_length, 
                                      num_walks=num_walks, 
                                      workers=workers)
        
        model: Any = node2vec.fit(window=5, 
                                  min_count=1, 
                                  batch_words=2)
        
        embeddings: List[List[float]] = [model.wv[str(node)] for node in G.nodes()]
        
        kmeans: KMeans = KMeans(n_clusters=num_clusters, random_state=42)
        cluster_labels: List[int] = kmeans.fit_predict(embeddings)

        gbc: GradientBoostingClassifier = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
        gbc.fit(embeddings, cluster_labels)
        
        cluster_labels = gbc.predict(embeddings)
        
        return cluster_labels
