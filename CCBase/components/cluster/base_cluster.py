from abc import ABC, abstractmethod
from typing import Any, Tuple
import networkx as nx

class BaseCluster(ABC):
    def perform_clustering(self, G: nx.Graph, n_clusters: int) -> Tuple[nx.Graph, Any]:
        self.preprocess_graph(G)
        labels = self.cluster_graph(G, n_clusters)
        self.postprocess_results(G, labels)
        return G, labels

    @abstractmethod
    def preprocess_graph(self, G: nx.Graph) -> None:
        pass

    @abstractmethod
    def cluster_graph(self, G: nx.Graph, n_clusters: int) -> Any:
        pass

    @abstractmethod
    def postprocess_results(self, G: nx.Graph, labels: Any) -> None:
        pass