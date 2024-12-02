from components.cluster.base_cluster import BaseCluster
from sklearn.cluster import spectral_clustering
import networkx as nx
from typing import List

class SpectralCluster(BaseCluster):
    def preprocess_graph(self, G: nx.Graph) -> None:
        pass

    def cluster_graph(self, G: nx.Graph, n_clusters: int) -> List[int]:
        labels: List[int] = spectral_clustering(nx.adjacency_matrix(G), n_clusters=n_clusters)
        return labels

    def postprocess_results(self, G: nx.Graph, labels: List[int]) -> None:
        for i, node in enumerate(G.nodes()):
            G.nodes[node]['cluster'] = labels[i]
