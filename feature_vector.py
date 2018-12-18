import networkx as nx
import numpy as np
import networkx.algorithms.isomorphism as iso
import sys, os
import pickle
from multiprocessing import Pool
from functools import partial


def parse_gaston_to_nx(filename):
    Graphs = []
    # with open(filename, 'r') as graph_file:
    #     while True:
    #         line = graph_file.readline()
    #         if line == "":
    #             break
    #         if line[0] == 't':
    #             # start a new Graph
    #             g = nx.Graph()
    #             while True:
    #                 last_pos = graph_file.tell()
    #                 nl = graph_file.readline()
    #                 if nl == "":
    #                     graph_file.seek(last_pos)
    #                     break
    #                 nl_split = nl.split()
    #                 print(nl_split)
    #                 if nl_split[0] == 'v':
    #                     g.add_node(nl_split[1], label=nl_split[2])
    #                 elif nl_split[0] == 'e':
    #                     g.add_edge(nl_split[1], nl_split[2], label=nl_split[3])
    #                 elif nl_split[0] == 't':
    #                     graph_file.seek(last_pos)
    #                     Graphs.append(g)
    #                     break

    g = nx.Graph()
    with open(filename, 'r') as fr:
        for num,line in enumerate(fr):
            line = line.strip().split()
            if line[0] == 't':
                if num > 0:
                    Graphs.append(g)
                g = nx.Graph()
            elif line[0] == 'v':
                g.add_node(line[1], label = line[2])
            elif line[0] == 'e':
                g.add_edge(line[1], line[2], label=line[3])
    Graphs.append(g)
    
    return Graphs

def thread_function(graph, subGraphs):
    vec = np.zeros(len(subGraphs))
    for s_idx, subgraph in enumerate(subGraphs):
        GM = iso.GraphMatcher(graph, subgraph, node_match=iso.categorical_node_match('label', ''), edge_match=iso.categorical_edge_match('label', ''))
        if GM.subgraph_is_isomorphic():
            vec[s_idx] = 1
    return vec


def feature_vector(graphs_file, subgraphs_file):
    graphs = parse_gaston_to_nx(graphs_file)
    # subGraphs = parse_gaston_to_nx(subgraphs_file)
    fr = open(subgraphs_file,'rb')
    subGraphs = pickle.load(fr)
    fr.close()

    feature_vector = np.zeros((len(graphs), len(subGraphs)))

    func = partial(thread_function, subGraphs=subGraphs)
    pool = Pool(os.cpu_count())
    features = np.array(pool.map(func, graphs))

    feature_vector = features.reshape((len(graphs), len(subGraphs)))

    # for g_idx, graph in enumerate(graphs):
    #     for s_idx, subgraph in enumerate(subGraphs):
    #         GM = iso.GraphMatcher(graph, subgraph, node_match=iso.categorical_node_match('label', ''), edge_match=iso.categorical_edge_match('label', ''))
    #         if GM.subgraph_is_isomorphic():
    #             feature_vector[g_idx][s_idx] = 1
    
    return feature_vector

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python feature_vector.py graphs_file subgraphs_file")
        exit(-1)
    graphs_file = sys.argv[1]
    subgraphs_file = sys.argv[2]

    # print(feature_vector(graphs_file, subgraphs_file))
    pick_file = open('./feature_vector_test.pickle','wb')
    feature_vec = feature_vector(graphs_file, subgraphs_file)
    # print(feature_vec)
    pickle.dump(feature_vec,pick_file)
    pick_file.close()
    






