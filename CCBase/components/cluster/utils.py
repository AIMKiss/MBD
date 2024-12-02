from typing import Dict

class ClusterUtils:
    @staticmethod
    def clustering_options() -> Dict[str, str]:
        return {
            'spectral': 'Spectral Clustering',
            'random_walk': 'Random Walk Clustering'
        }