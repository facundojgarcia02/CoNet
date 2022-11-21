import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from utils.learn import learn_embeddings
from utils.graph import Graph

if __name__ == "__main__":
    path_to_gexf = "state_files/red_artistas.gexf"

    # Arguments.
    p = 1
    q = 1
    directed = False
    num_walks = 30
    walk_length = 80
    dimensions = 8
    window_size = 10
    workers = 1
    epochs = 1
    output = "output 3d.emb"

    # Read network.
    print("[DEBUG] - Loading network.")
    nx_G = nx.read_gexf(path_to_gexf)
    nx.set_edge_attributes(nx_G, 1, name = "weight")
    G = Graph(nx_G, directed = directed, p = p, q = q)
    del(nx_G)
    print("[DEBUG] - Network loaded.")

    # Simulate walks.
    print("[DEBUG] - Simulating Walks.")
    G.preprocess_transition_probs()
    walks = G.simulate_walks(num_walks, walk_length)
    walks = [list(map(str, walk)) for walk in walks]
    del(G)
    print("[DEBUG] - Walks simulated.")


    # Learn embeddings.
    print("[DEBUG] - Learning embeddings.")
    learn_embeddings(walks, dimensions = dimensions, window_size = window_size, 
                     workers = workers, epochs = epochs, output = output)
    print("[DEBUG] - Embeddings Learned.")