import networkx as nx
import igraph as ig

def main(path_to_gexf: str):

    print("Loading network.")
    G = nx.read_gexf(path_to_gexf)
    # Mejor manera que la que teníamos. Conserva nombres.
    G_ig = ig.Graph.TupleList(G.edges(), directed=True)
    print("Network loaded.")

    sizes = [3, 4, 5]
    for s in sizes:
        print(f"Searching {s}-size motifs.")
        no_s = G_ig.motifs_randesu_no(size=s)
        print(f"Found motifs of size {s}: {no_s}.")

if __name__ == "__main__":
    path_to_gexf = "state_files/PyPi Network V4.gexf"
    main(path_to_gexf)