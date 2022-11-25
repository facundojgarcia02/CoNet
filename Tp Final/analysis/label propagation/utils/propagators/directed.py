import networkx as nx
import matplotlib.pyplot as plt

from random import choice
from tqdm import tqdm
from collections import Counter

from utils.propagatelabels import PropagateLabels, GraphError

class PropagateDirected(PropagateLabels):
    """
    Given a network G and initial labels, propagate labels through all directed graph.
    Currently limited to only one label for each propagated node.
    """

    def __init__(self, G, initial_labels, method):
        super().__init__(G, initial_labels, method)

        # Required for finding neighbors in directed graph.
        self.G_reversed = G.reverse()
        self.reversed_neighbors = {node: nx.neighbors(self.G_reversed, node) for node in self.nodes}

    def propagate_once(self) -> dict:
        """
        Propagate labels of G to first order neighbors.

        Returns:
            - dict: Propagated labels.
        Raises:
            - ValueError: If all nodes are already labels.
        """

        # Si ya están todos etiquetados no hacemos nada.
        if len(self.labels) == len(self.G.nodes()):
            raise ValueError("All nodes already has labels.")

        # Nodos con etiqueta sobre los que vamos a comenzar a iterar.
        nodes_with_labels = list(self.labels.keys()).copy()

        # Buscamos los vecinos de los nodos etiquetados.
        first_order_neighbors = []
        for node in tqdm(nodes_with_labels):
            neighbors = self.neighbors[node]
            # Nos quedamos con los que no están etiquetados o ya guardamos.
            for neigh in neighbors:
                if (neigh not in nodes_with_labels) and (neigh not in first_order_neighbors):
                    first_order_neighbors.append(neigh)


        # Pedimos los vecinos de cada nodo encontrado a primer orden. Nos fijamos
        # los que están etiquetados solamente.
        posible_labels = {}
        # Para buscar de donde vienen los nodos que encontramos.

        for node in tqdm(first_order_neighbors):
            # Guardamos una lista con las etiquetas de los vecinos etiquetados.
            posible_labels[node] = []
            neighbors = self.reversed_neighbors[node]
            for neigh in neighbors:
                if neigh in nodes_with_labels:
                    # Si el nodo original tiene una sola etiqueta o mas:
                    if isinstance(self.labels[neigh], list):
                        posible_labels[node] += self.labels[neigh]
                    else:
                        posible_labels[node].append(self.labels[neigh])

        propagated_labels = {}
        if self.method == "probability":
            # Finalmente elegimos UNA etiqueta (Se puede cambiar mas adelante):
            for node, labels in posible_labels.items():
                propagated_labels[node] = choice(labels)
        
        elif self.method == "local":
            for node, labels in posible_labels.items():
                # Nos fijamos cual aparece mas seguido.
                count_labels = Counter(labels)
                labels_by_count = dict(sorted(count_labels.items(), key = lambda x: x[1], reverse=True))
                # Si hay empate entre dos o mas con la misma cantidad.
                most_common = list(labels_by_count.values())[0]
                if Counter(labels_by_count.values())[most_common] > 1:
                    propagated_labels[node] = choice([l for l, c in labels_by_count.items() if c == most_common])
                else:
                    propagated_labels[node] = list(labels_by_count.keys())[0]

        elif self.method == "global":
            # Recolecto todas las etiquetas que me dieron en esta iteración.
            label_collector = []
            for n, l in self.labels.items():
                if isinstance(l, list):
                    label_collector += l
                elif isinstance(l, str):
                    label_collector += [l]
                else:
                    raise Exception("No deberían haber etiquetas que no sean listas o str.")

            ### Idea: El peso para elegir cada tópico va a ser peso local / peso global.
            
            # Peso global.
            global_weights = {t: v/len(label_collector) for t, v in Counter(label_collector).items()}
            
            # Peso local:
            for node, labels in posible_labels.items():
                local_weights = {t: v/len(labels) for t, v in Counter(labels).items()}
                
                labels_by_weight = {t: local_weights[t]/global_weights[t] for t in local_weights.keys()}
                labels_by_weight = dict(sorted(labels_by_weight.items(), key = lambda x: x[1], reverse=True))
                
                propagated_labels[node] = list(labels_by_weight.keys())[0]
                
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

        amount_of_labels = []
        while len(self.labels) < len(self.G.nodes()):
            self.propagate_once()
            print(f"{len(self.labels)} nodos etiquetados de {len(self.G.nodes())}.")
            if amount_of_labels == len(self.labels):
                print("No se encontraron nuevas etiquetas.")
                break
            else:
                amount_of_labels = len(self.labels)
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
