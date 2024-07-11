import networkx as nx
from itertools import combinations
import random
import pickle
def assign_random_weights(G, min_weight=1, max_weight=10):

    for u, v in G.edges():
        G.edges[u, v]['weight'] = random.randint(min_weight, max_weight)

def find_triangles_with_edge_sums(G):
    triangles = {}
    for node in G.nodes():
        neighbors = set(G.neighbors(node))
        for n1, n2 in combinations(neighbors, 2):
            if G.has_edge(n1, n2):

                triangle = frozenset([node, n1, n2])
                edge_weights = [
                    G[node][n1]['weight'],
                    G[node][n2]['weight'],
                    G[n1][n2]['weight']
                ]
                triangle_info = {
                    'vertices': triangle,
                    'side_sum': sum(edge_weights[:-1]),
                    'perimeter': sum(edge_weights)
                }

                for n in triangle:
                    if n in triangles:
                        triangles[n].append(triangle_info)
                    else:
                        triangles[n] = [triangle_info]

    return triangles


G=nx.read_gexf("../BA_n_2000_medium.gexf")

triangles = find_triangles_with_edge_sums(G)
with open('../weight_triangle_up.pkl', 'wb') as f:
    pickle.dump(triangles, f)

print(type(triangles))
for node, tris in triangles.items():
    if node=="0":
        for tri in tris:
            print(f"  {tri['vertices']},{tri['side_sum']}, {tri['perimeter']}")

