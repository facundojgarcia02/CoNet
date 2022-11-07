import networkx as nx
import json

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

class SearchScope:

    def __init__(self, G) -> None:
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

if __name__ == "__main__":
    # Nodos con grado in 0 = Nodos que no dependen de nada.
    G = load_network("proc_jsons.json")
    print("Network Loaded")

    no_dep_nodes = [x[0] for x in list(filter(lambda x: x[1] == 0, tuple(G.in_degree())))]
    print("Starting search")
    search = SearchScope(G)

    for n in no_dep_nodes:
        search(n)

    print(search.scoped_nodes)