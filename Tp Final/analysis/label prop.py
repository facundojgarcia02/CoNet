import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from random import shuffle, choice


class GraphError(Exception):
    pass


class PropagateLabels:
    """
    Given a network G and initial labels, propagate labels throw all graph.
    Currently limited to only one label for each propagated node.
    """

    def __init__(self, G, initial_labels, DEBUG=False):
        self.G = G.copy()
        self.labels = initial_labels

        self.backup_G = G.copy()
        self.backup_labels = initial_labels.copy()

        self.DEBUG = DEBUG

    def restart(self):
        """
        Restart propagation.
        """
        self.G = self.backup_G.copy()
        self.labels = self.backup_labels.copy()

    def propagate_once(self) -> dict:
        """
        Propagate labels of G to first order neighbors.

        Returns:
            - dict: Propagated labels.
        """

        # Si ya están todos etiquetados no hacemos nada.
        if len(self.labels) == len(self.G.nodes()):
            raise ValueError("All nodes already has labels.")

        # Nodos con etiqueta sobre los que vamos a comenzar a iterar.
        nodes_with_labels = list(self.labels.keys()).copy()

        if self.DEBUG:
            print("DEBUG - Nodos etiquetados:")
            print(nodes_with_labels)

        # Buscamos los vecinos de los nodos etiquetados.
        first_order_neighbors = []
        for node in nodes_with_labels:
            neighbors = nx.neighbors(self.G, node)
            # Nos quedamos con los que no están etiquetados o ya guardamos.
            for neigh in neighbors:
                if neigh not in nodes_with_labels + first_order_neighbors:
                    first_order_neighbors.append(neigh)

        if self.DEBUG:
            print("DEBUG - Vecinos de los etiquetados:")
            print(first_order_neighbors)

        # Pedimos los vecinos de cada nodo encontrado a primer orden. Nos fijamos
        # los que están etiquetados solamente.
        posible_labels = {}
        # Para buscar de donde vienen los nodos que encontramos.
        reversed_G = self.G.reverse()
        for node in first_order_neighbors:
            # Guardamos una lista con las etiquetas de los vecinos etiquetados.
            posible_labels[node] = []
            neighbors = nx.neighbors(reversed_G, node)
            for neigh in neighbors:
                if neigh in nodes_with_labels:
                    # Si el nodo original tiene una sola etiqueta o mas:
                    if isinstance(self.labels[neigh], list):
                        posible_labels[node] += self.labels[neigh]
                    else:
                        posible_labels[node].append(self.labels[neigh])

        if self.DEBUG:
            print("DEBUG - Etiquetas recoletadas:")
            print(posible_labels)

        propagated_labels = {}
        # Finalmente elegimos UNA etiqueta (Se puede cambiar mas adelante):
        for node, labels in posible_labels.items():
            propagated_labels[node] = choice(labels)

        # Guardamos las etiquetas finales: Etiquetas iniciales + obtenidas.
        final_labels = {**self.labels, **propagated_labels}
        self.labels = final_labels

        return self.labels

    def propagate_all(self) -> dict:
        """
        Propagate labels of G to all graph.

        Returns:
            - dict: Propagated labels.

        Raises:
            - GraphError: If graph has more than one component. 
        """

        if not nx.is_connected(self.G.to_undirected()):
            raise GraphError("Graph must have one component.")

        while len(self.labels) < len(self.G.nodes()):
            self.propagate_once()
            print(f"{len(self.labels)} nodos etiquetados de {len(self.G.nodes())}.")

        return self.labels


if __name__ == "__main__":
    # Test network.
    edges = [(1, 2), (2, 3), (4, 3), (1, 4), (1, 5),
             (5, 4), (3, 6), (4, 6), (6, 7)]
    labels = {1: "Science", 2: "Internet", 5: "Religion"}

    G = nx.DiGraph(edges)

    pg = PropagateLabels(G, labels)
    final_labels = pg.propagate_all()

    print("Etiquetadas encontradas:")
    print(final_labels)

    nx.draw(G, with_labels=True)
    plt.show()
