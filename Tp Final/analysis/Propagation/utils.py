import networkx as nx
import json
import numpy as np

def load_network(path: str ="../proc_jsons.json"):
    with open(path, "r") as f:
        deps = json.load(f)

    G = nx.DiGraph()
    nodes = [d["Name"] for d in deps]
    edges = []
    for d in deps:
        edges += [(p, d["Name"]) for p in d["Dependencies"]]

    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    return G


class ReachFinder:

    def __init__(self, G: nx.Graph, p: float = 1) -> None:
        self.G = G
        self.reached_from = {node: set() for node in G.nodes}
        self.calls = 0
        self.p = p
    
    def find_all_nodes(self) -> dict[set]:
        for n in self.G.nodes:
            self.find_from_node(n)

        print(f"\rDone. Function called {self.calls} times.")
        return self.reached_from
    
    def find_from_node(self, node: str, path: list = None) -> set:
        """
        Gets the reach of a node.

        Args:
            node (str): Node to search from.
            path (list, optional): List of nodes reached before. Defaults to None.
        """
        if len(self.reached_from[node]) == 0:  # Si ya estuve acá, no hago nada.
            self.reached_from[node].add(node)
            if path is None:
                path = []

            neighbors = list(nx.neighbors(self.G, node))
            for neigh in neighbors:
                if np.random.uniform(low=0, high=1, size = 1) >= 1-self.p:
                    if neigh not in path:
                        reach_from_neigh = self.find_from_node(neigh, path=path+[node])
                        self.reached_from[node].update(reach_from_neigh)
                    else:
                        self.reached_from[node].update(self.reached_from[neigh])
                        self.reached_from[neigh] = self.reached_from[node]
            
            self.calls += 1
            print(f"\rFunction called {self.calls} times.", end="")
        
        return self.reached_from[node]

    # Remove self nodes in scope.
    @staticmethod
    def remove_self_edges(reach):
        for k, v in reach.items():
            if v is not None:
                try:
                    v.remove(k)
                except KeyError:
                    print(k, "no estaba en el reach.")
                if v is None:
                    reach[k] = set()
            else:
                reach[k] = set()
        
        return reach


class SearchScope:

    def __init__(self, G: nx.Graph) -> None:
        self.G = G
        self.scoped_nodes = {}

    def __call__(self, node: str, path: list = None) -> None:
        """
        Search scope of a node.

        Args:
            node (str): Node to search.
            path (list, optional): List of nodes reached before. Defaults to None.
        """
        
        neighs = list(nx.neighbors(self.G, node))
        scope = set()
        if path is None:
            path = []

        for n in neighs:
            if n not in path:
                try:
                    partial_scope = self.scoped_nodes[n]
                except KeyError:
                    if node not in path:
                        path.append(node)
                    self(n, path = path)
                    partial_scope = self.scoped_nodes[n]
                finally:
                    scope = scope | partial_scope | set([n])

        self.scoped_nodes[node] = scope
        print(len(self.scoped_nodes), end="\r")
    
        return None