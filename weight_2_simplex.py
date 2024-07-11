import networkx as nx
from itertools import combinations
import random
import pickle
#带权重的网络计算节点的所有三角形的权重之和的情况，以级以node为顶点的直接联系的两边的和


def assign_random_weights(G, min_weight=1, max_weight=10):
    """
    为图G中的每条边分配一个随机权重。
    """
    for u, v in G.edges():
        G.edges[u, v]['weight'] = random.randint(min_weight, max_weight)


def find_triangles_with_edge_sums(G):
    """
    找到图G中每个节点所在的所有三角形，并计算：
    - 每个三角形与顶点node直接相连的两个边的权重和
    - 这个三角形三条边的权重和
    返回一个字典，键是节点，值是一个列表，包含该节点的所有三角形的信息。
    每个三角形的信息是一个字典，包括顶点集合、两边和以及三边和。
    """
    triangles = {}  # 存储每个节点及其所在三角形的信息

    for node in G.nodes():
        neighbors = set(G.neighbors(node))
        for n1, n2 in combinations(neighbors, 2):
            if G.has_edge(n1, n2):
                # 找到一个三角形
                triangle = frozenset([node, n1, n2])
                edge_weights = [
                    G[node][n1]['weight'],
                    G[node][n2]['weight'],
                    G[n1][n2]['weight']
                ]
                triangle_info = {
                    'vertices': triangle,
                    'side_sum': sum(edge_weights[:-1]),  # 直接相连的两条边的和
                    'perimeter': sum(edge_weights)  # 三条边的和
                }

                # 添加三角形信息到相关节点
                for n in triangle:
                    if n in triangles:
                        triangles[n].append(triangle_info)
                    else:
                        triangles[n] = [triangle_info]

    return triangles


# 创建并初始化图
# G = nx.Graph()
# edges = [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (4, 6), (2, 4)]
# G.add_edges_from(edges)

# 为每条边分配随机权重
# assign_random_weights(G)

G=nx.read_gexf("../网络/BA_n_2000_medium.gexf")

# 找到并打印每个节点所在的三角形及其边权重信息
triangles = find_triangles_with_edge_sums(G)
with open('../网络/weight_triangles_up.pkl', 'wb') as f:
    pickle.dump(triangles, f)

print(type(triangles))
for node, tris in triangles.items():
    if node=="0":
        print(f"节点 {node}:")
        print(tris[0])
        for tri in tris:
            print(f"  三角形顶点: {tri['vertices']}, 直接相连边权重和: {tri['side_sum']}, 三边权重和: {tri['perimeter']}")

