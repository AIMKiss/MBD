from typing import Dict
import networkx as nx
from community import community_louvain

def estimate_clusters(G: nx.Graph) -> int:
    partition: Dict[int, int] = community_louvain.best_partition(G)
    num_clusters: int = len(set(partition.values()))
    return num_clusters