import networkx as nx
from tqdm import tqdm

G = nx.read_gexf("state_files/PyPi Network V4.gexf")
with open('Network.txt', 'w') as f:
    for edge in tqdm(G.edges()):
        f.write(f'{edge[0]}\t{edge[1]}\t1\n')