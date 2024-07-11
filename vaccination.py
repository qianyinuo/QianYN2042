import pickle
import numpy as np
import networkx as nx
import random
def calculate_benefit(C_i_V_n, C_i_V_0, k):
    numerator = 1
    denominator = 1 + np.exp(-k * (C_i_V_n - C_i_V_0))
    v_i_n_value = numerator / denominator
    return v_i_n_value
def network_ini_attribute(BA_network):
      mean = 0.5
    std_dev = 0.1
    immune_values = np.random.normal(mean, std_dev, 2000).clip(0, 1)  
for node, immune_value in zip(BA_network.nodes(), immune_values):
        BA_network.nodes[node]['immune'] = immune_value
 cv=1
    for node in list(BA_network.nodes()):
        VA0 = []
        VA1 = []
        VA2 = []
        VA3 = []
        c = []
        d=[]
        #0.95、0.8、0.6、0.2 Benefit of COVID-19 vaccination accounting for potential risk compensation
        va0 =-(1-BA_network.nodes[node]['immune'])-(1-0.1)
        c.append(va0)
        va1 = -0.5*cv - (1 - BA_network.nodes[node]['immune'])-(1-0.4)
        c.append(va1)
        va2 = -0.7*cv - (1 - BA_network.nodes[node]['immune'])-(1-0.845)
        c.append(va2)
        va3 = - cv - (1 - BA_network.nodes[node]['immune'])-(1-0.935)
        c.append(va3)
        va0_p = calculate_benefit(va0, va0, 0.1)
        d.append(va0_p)
        va1_p=calculate_benefit(va1, va0, 0.1)
        d.append(va1_p)
        va2_p = calculate_benefit(va2, va0, 0.1)
        d.append(va2_p)
        va3_p = calculate_benefit(va3, va0, 0.1)
        d.append(va3_p)
        BA_network.nodes[node]['va_value'] = c
        BA_network.nodes[node]['va_value_p'] = d

def calculate_imitation_probability(node,node_status_list,trianle_node_list,optimal_triangles, G, omega):
    A0 = []
    A1 = []
    A2 = []
    A3 = []
      if node in trianle_node_list:
        # print(node)
        optimal_triangles.get("node")
        node_list=list((optimal_triangles.get(node)['vertices']))
        # print(node_list)
        node_list.remove(node)

        for i in node_list:
             i_state = node_status_list[i]
            if i_state=='S':
                a = calculate_benefit(G.nodes[node]['va_value'][0], G.nodes[i]['va_value'][0], 0.1)
                A0.append([node, i, a])
            elif i_state == 'I1':
                a = calculate_benefit(G.nodes[node]['va_value'][0], G.nodes[i]['va_value'][1], 0.1)
                A1.append([node,i,a])
            elif i_state == 'I2':
                a = calculate_benefit(G.nodes[node]['va_value'][0], G.nodes[i]['va_value'][2], 0.1)
                A2.append([node,i,a])
            else:
                a = calculate_benefit(G.nodes[node]['va_value'][0], G.nodes[i]['va_value'][3], 0.1)
                A3.append([node,i,a])
    else:
        max_edge_weight = max(G[node][n]['weight'] for n in G.neighbors(node))
        max_edge_neighbors = [n for n in G.neighbors(node) if G[node][n]['weight'] == max_edge_weight]


        for i in max_edge_neighbors:
            i_state = node_status_list[i]
            if i_state=='S':
                a = calculate_benefit(G.nodes[node]['va_value'][0], G.nodes[i]['va_value'][0], 0.1)
                A0.append([node, i, a])
            elif i_state=='I1':
                a=calculate_benefit(G.nodes[node]['va_value'][0],G.nodes[i]['va_value'][1],0.1)
                A1.append([node,i,a])
            elif i_state=='I2':
                a = calculate_benefit(G.nodes[node]['va_value'][0], G.nodes[i]['va_value'][2], 0.1)
                A2.append([node,i,a])
            else:
                a = calculate_benefit(G.nodes[node]['va_value'][0], G.nodes[i]['va_value'][3], 0.1)
                A3.append([node,i,a])

    if len(A0)>0:
        a0_average=0
        sum_a0_weight=0
        for i in A1:
            sum_a0_weight+=G[i[0]][i[1]]['weight']
        for i in A1:
            a0_average += G[node][i[1]]['weight']*i[2]

        max_benefit0=a0_average/ sum_a0_weight
    else:
        max_benefit0=0

    if len(A1)>0:
        a1_average=0
        sum_a1_weight=0
        for i in A1:
            sum_a1_weight+=G[i[0]][i[1]]['weight']
        for i in A1:
            a1_average += G[node][i[1]]['weight']*i[2]

        max_benefit1=a1_average/ sum_a1_weight
    else:
        max_benefit1=0

    if len(A2)>0:
        a2_average = 0
        sum_a2_weight = 0
        for i in A2:
            sum_a2_weight += G[i[0]][i[1]]['weight']
        for i in A2:
            a2_average += G[node][i[1]]['weight'] * i[2]
        max_benefit2 = a2_average / sum_a2_weight
    else:
        max_benefit2=0

    if len(A3) > 0:
        a3_average = 0
        sum_a3_weight = 0
        for i in A3:
            sum_a3_weight += G[i[0]][i[1]]['weight']
        for i in A3:
            a3_average += G[node][i[1]]['weight'] * i[2]
        max_benefit3 = a3_average / sum_a3_weight
    else:
        max_benefit3 = 0

    h=[]
    imitation_prob_v0 = omega * G.nodes[node]['va_value_p'][0] + (1 - omega) * max_benefit0
    imitation_prob_v1 = omega * G.nodes[node]['va_value_p'][1] + (1 - omega) * max_benefit1
    imitation_prob_v2 = omega * G.nodes[node]['va_value_p'][2] + (1 - omega) * max_benefit2
    imitation_prob_v3 = omega * G.nodes[node]['va_value_p'][3] + (1 - omega) * max_benefit3
    h.append(imitation_prob_v0)
    h.append(imitation_prob_v1)
    h.append(imitation_prob_v2)
    h.append(imitation_prob_v3)
    G.nodes[node]['va_value_p_state'] = h

    return h
with open("../weight_triangles_medium_after_screening_node_list.pkl", 'rb') as f:
   data1 = pickle.load(f)
trianle_node_list = data1

with open("../weight_triangles_medium_after_screening.pkl", 'rb') as f:
     data2 = pickle.load(f)
 optimal_triangles=data2
 BA_network= nx.read_gexf("../BA_n_2000_medium.gexf")
 BA_network=network_ini_attribute(BA_network)
 for node in list(BA_network.nodes()):
     print(node)
     imitation_prob_v1,imitation_prob_v2,imitation_prob_v3=calculate_imitation_probability(node,trianle_node_list,optimal_triangles, BA_network, 0.7)