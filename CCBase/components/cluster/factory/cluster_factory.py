from components.cluster.spectral_cluster import SpectralCluster
from components.cluster.random_walk_cluster import RandomWalkCluster
from typing import Union

class ClusterFactory:
    @staticmethod
    def create_cluster(method: str) -> Union[SpectralCluster, RandomWalkCluster]:
        if method == 'spectral':
            return SpectralCluster()
        elif method == 'random_walk':
            return RandomWalkCluster()
        else:
            raise ValueError(f"Unknown clustering method: {method}")