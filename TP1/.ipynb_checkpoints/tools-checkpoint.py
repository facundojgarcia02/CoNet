from typing import Union

import numpy as np
from scipy.sparse._arrays import csr_array

AdjMatrix = Union[np.ndarray, csr_array]

GRAPH_FMT = dict(
    # Node Format
    node_color='mediumpurple', linewidths=1.5, edgecolors='indigo',
    # Edge Format
    edge_color='lightgreen', width=3,
    # Label Format
    font_color='w', font_family='serif',
    )

DIGRAPH_FMT = dict(
    # Node Format
    node_color='mediumpurple', linewidths=1.5, edgecolors='indigo',
    # Edge Format
    edge_color='forestgreen', width=2,
    # Label Format
    font_color='w', font_family='serif',
    )


def calcular_grado_vector(A: AdjMatrix):
    '''The vector k whose elements are the degrees ki of all nodes
    i = 1, 2,..., N.'''
    return A.dot(np.ones(A.shape[0]))

def calcular_num_aristas(A: AdjMatrix):
    '''The total number of links, L, in the network.'''
    k = calcular_grado_vector(A)
    return k.dot(np.ones_like(k))/2


def calcular_num_triangulos(A: AdjMatrix):
    '''The number of triangles T present in the network,
    where a triangle means three nodes, each connected by links to
    the other two'''
    return (A@A@A).trace()/6

def calcular_knn_vector(A: AdjMatrix):
    '''The vector knn whose element i is the sum of the degrees of
    node i's neighbors.'''
    return (A@A).dot(np.ones(A.shape[0]))

def calcular_knnn_vector(A: AdjMatrix):
    '''The vector knnn whose element i is the sum of the degrees of
    node i's second neighbors.'''
    return (A@A@A).dot(np.ones(A.shape[0]))