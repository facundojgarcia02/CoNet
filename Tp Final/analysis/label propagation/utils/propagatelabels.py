from abc import abstractclassmethod, ABCMeta
import networkx as nx

class GraphError(Exception):
    """
    Exception throwed when graph properties are 
    incorrect for current object.
    """
    pass

class IPropagate(metaclass = ABCMeta):

    @abstractclassmethod
    def propagate_once(self):
        """
        How propagation is calculated to first order neighbors.
        """
    
    @abstractclassmethod
    def propagate_all(self):
        """
        How propagation is calculated to every node in graph.
        """

class PropagateLabels(IPropagate):
    
    def __init__(self, G, initial_labels) -> None:
        self.G = G.copy()
        self.labels = initial_labels

        self.backup_labels = initial_labels.copy()

        self.nodes = G.nodes()
        self.neighbors = {node: nx.neighbors(self.G, node) for node in self.nodes}

    def restart(self):
        """
        Restart propagation.
        """
        self.labels = self.labels_backup

if __name__ == "__main__":
    # Test for abstract class. Should raise Exception.
    edges = [(1, 2), (2, 3), (4, 3), (1, 4), (1, 5),
             (5, 4), (3, 6), (4, 6), (6, 7)]
    labels = {1: "Science", 2: "Internet", 5: "Religion"}

    G = nx.DiGraph(edges)

    pg = PropagateLabels(G, labels)

    PropagateLabels().propagate_once()