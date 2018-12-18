import networkx as nx
import numpy as np
import networkx.algorithms.isomorphism as iso
import sys
import pickle
from collections import Counter
import multiprocessing
from functools import partial
import os

global feature_vector
global active_subgraphs
global inactive_subgraphs
global graphs
global act_subgraphs_counter

feature_vector = np.array([])
active_subgraphs = []
inactive_subgraphs = []
graphs = []
act_subgraphs_counter = 0


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
    #                 # print(nl_split)
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


def thread_function_1(inactive_graph_id, active_subgraphs, graphs):
    feature_vector = np.zeros(len(active_subgraphs))

    # print("Thread  1 :  Num of Active Subgraphs : " + str(len(active_subgraphs)))
    # print("Thread  1 :  Num of graphs : " + str(len(graphs)))
    # print("Thread  1 :  id : " + str(inactive_graph_id))

    for s_idx, subgraph in enumerate(active_subgraphs):
        # print("\t\tchecking subgraph... " + str(s_idx))
        graph = graphs[inactive_graph_id]
        GM = iso.GraphMatcher(graph, subgraph, node_match=iso.categorical_node_match('label', ''), edge_match=iso.categorical_edge_match('label', ''))
        if GM.subgraph_is_isomorphic():
            feature_vector[s_idx] = 1
            # feature_vector[inactive_graph_id][s_idx] = 1
    return feature_vector

def thread_function_2(active_graph_id, inactive_subgraphs, graphs):
    feature_vector = np.zeros(len(inactive_subgraphs))

    # print("Thread  2 :  Num of Inactive Subgraphs : " + str(len(active_subgraphs)))
    # print("Thread  2 :  Num of graphs : " + str(len(graphs)))
    # print("Thread  2 :  id : " + str(active_graph_id))

    for s_idx, subgraph in enumerate(inactive_subgraphs):
        # print("\tchecking subgraph... " + str(s_idx + act_subgraphs_count))
        graph = graphs[active_graph_id]
        GM = iso.GraphMatcher(graph, subgraph, node_match=iso.categorical_node_match('label', ''), edge_match=iso.categorical_edge_match('label', ''))
        if GM.subgraph_is_isomorphic():
            feature_vector[s_idx] = 1
            # feature_vector[active_graph_id][s_idx + act_subgraphs_count] = 1
    return feature_vector


def feature_vector(all_graphs, active_gspan_output, inactive_gspan_output, combined_gaston_format_output, act_subgraphs_count, inact_subgraphs_count, active_graphs_ids, inactive_graphs_ids):
    global feature_vector
    global active_subgraphs
    global inactive_subgraphs
    global graphs
    global act_subgraphs_counter

    pool = multiprocessing.Pool(os.cpu_count())
    graphs = parse_gaston_to_nx(all_graphs)
    subGraphs = parse_gaston_to_nx(combined_gaston_format_output)
    print("Thread Main : Num of graphs : " + str(len(graphs)))
    print("Thread Main : Num of Subgraphs : " + str(len(subGraphs)))

    active_subgraphs_temp = subGraphs[:act_subgraphs_count]
    inactive_subgraphs_temp = subGraphs[act_subgraphs_count:]
    
# to keep inactive features start
    inactive_subgraphs = inactive_subgraphs_temp
    all_subgraphs = [g for g in inactive_subgraphs]
    active_ids = np.zeros(len(active_subgraphs_temp))

    for act_count, act_g in enumerate(active_subgraphs_temp):
        flag = 0
        for inact_g in inactive_subgraphs_temp:
            if nx.is_isomorphic(act_g, inact_g, node_match=iso.categorical_node_match('label', ''), edge_match=iso.categorical_edge_match('label', '')): #if they could be isomorphic, retain only inactive one
                flag = 1
                break
            # else: #both are definitely not isomorphic, retain both
        if flag == 0:
            active_ids[act_count] = 1
            active_subgraphs.append(act_g)
            all_subgraphs.append(act_g)
# to keep inactive features end

# uncomment the code below to remove both the features
    # all_subgraphs = []
    # active_ids = np.zeros(len(active_subgraphs_temp))
    # inactive_ids = np.zeros(len(inactive_subgraphs_temp))
    # for act_count, act_g in enumerate(active_subgraphs_temp):
    #     flag = 0
    #     for inact_g in inactive_subgraphs_temp:
    #         if nx.is_isomorphic(act_g, inact_g, node_match=iso.categorical_node_match('label', ''), edge_match=iso.categorical_edge_match('label', '')): #if they could be isomorphic, retain only inactive one
    #             flag = 1
    #             break
    #         # else: #both are definitely not isomorphic, retain both
    #     if flag == 0:
    #         active_ids[act_count] = 1
    #         active_subgraphs.append(act_g)
    #         all_subgraphs.append(act_g)
    # for inact_count, inact_g in enumerate(inactive_subgraphs_temp):
    #     flag = 0
    #     for act_g in active_subgraphs_temp:
    #         if nx.is_isomorphic(act_g, inact_g, node_match=iso.categorical_node_match('label', ''), edge_match=iso.categorical_edge_match('label', '')): #if they could be isomorphic, retain only inactive one
    #             flag = 1
    #             break
    #         # else: #both are definitely not isomorphic, retain both
    #     if flag == 0:
    #         inactive_ids[inact_count] = 1
    #         inactive_subgraphs.append(inact_g)
    # all_subgraphs.append(inact_g)

# uncomment the code above to remove above the features



    print("Finally, active subgraphs = " + str(len(active_subgraphs)) + ", inactive subGraphs = " + str(len(inactive_subgraphs)))
    act_subgraphs_count = len(active_subgraphs)
    inact_subgraphs_count = len(inactive_subgraphs)
    feature_vector = np.zeros((len(graphs), act_subgraphs_count + inact_subgraphs_count))
    # print(feature_vector.shape)

    counter = 0
    with open(active_gspan_output, 'r') as fr:
        for line in fr:
            line = line.strip()
            line_list = line.split(" ")
            if(line_list[0] == 'x'):
                if active_ids[counter] == 1:
                    graphs_with_pattern = line_list[1:]
                    graphs_with_pattern = list(map(int, graphs_with_pattern))
                    for graph in graphs_with_pattern:
                        feature_vector[graph][counter] = 1
                    counter = counter + 1

    # counter_ = 0
    with open(inactive_gspan_output, 'r') as fr:
        for line in fr:
            line = line.strip()
            line_list = line.split(" ")
            if(line_list[0] == 'x'):
                # if inactive_ids[counter_] == 1:
                    # print("Counter : " + str(counter))
                    # print("Act Count : " + str(act_subgraphs_count))
                    # if inactive_ids[counter - act_subgraphs_count] == 1:
                graphs_with_pattern = line_list[1:]
                graphs_with_pattern = list(map(int, graphs_with_pattern))
                for graph in graphs_with_pattern:
                    feature_vector[graph][counter] = 1
                counter = counter + 1
                # counter_ = counter_ + 1

    # THREADING STARTS HERE
    print("Starting thread 1...")
    func = partial(thread_function_1, active_subgraphs=active_subgraphs, graphs=graphs)
    active_features = pool.map(func, inactive_graphs_ids)
    
    print("Starting thread 2...")
    func = partial(thread_function_2, inactive_subgraphs=inactive_subgraphs, graphs=graphs)
    inactive_features = pool.map(func, active_graphs_ids)
    pool.close()
    pool.join()

    for index, inact_g in enumerate(inactive_graphs_ids):
        func_out = active_features[index]
    for c,val in enumerate(func_out):
        feature_vector[inact_g][c] = val

    for index, act_g in enumerate(active_graphs_ids):
        func_out = inactive_features[index]
    for c, val in enumerate(func_out):
        feature_vector[act_g][c+act_subgraphs_count] = val

    # for i in range(100):
    #     for j in range(act_subgraphs_count + inact_subgraphs_count):
    #         print(str(feature_vector[i][j]) + ' ')
    #     print('\n')

    
    # for s_idx, subgraph in enumerate(active_subgraphs):
    #     print("checking subgraph... " + str(s_idx))
    #     for g_idx in inactive_graphs_ids:
    #         graph = graphs[g_idx]
    #         GM = iso.GraphMatcher(graph, subgraph, node_match=iso.categorical_node_match('label', ''), edge_match=iso.categorical_edge_match('label', ''))
    #         if GM.subgraph_is_isomorphic():
    #             feature_vector[g_idx][s_idx] = 1

    # for s_idx, subgraph in enumerate(inactive_subgraphs):
    #     print("checking subgraph... " + str(s_idx + act_subgraphs_count))
    #     for g_idx in active_graphs_ids:
    #         graph = graphs[g_idx]
    #         GM = iso.GraphMatcher(graph, subgraph, node_match=iso.categorical_node_match('label', ''), edge_match=iso.categorical_edge_match('label', ''))
    #         if GM.subgraph_is_isomorphic():
    #             feature_vector[g_idx][s_idx + act_subgraphs_count] = 1

    new_subgraph_file = open('./new_subgraphs.pickle','wb')
    pickle.dump(all_subgraphs, new_subgraph_file)
    new_subgraph_file.close()

    return feature_vector

if __name__ == '__main__':
    all_graphs_input = sys.argv[1]
    active_gspan_output = sys.argv[2]
    inactive_gspan_output = sys.argv[3]
    combined_gaston_format_output = sys.argv[4]
    act_subgraphs_count = int(sys.argv[5])
    inact_subgraphs_count = int(sys.argv[6])

    #laad the dictionary
    pickle_in = open('label_mapping.pickle', 'rb')
    dictionary = dict(pickle.load(pickle_in))
    pickle_in.close()

    new_dictionary = dict()
    for key in dictionary:
        value = dictionary[key]
        if value in new_dictionary:
            new_dictionary[value] = new_dictionary[value] + list([int(key)])
        else:
            new_dictionary[value] = list([int(key)])

    active_graphs_ids = list(new_dictionary[1])
    inactive_graphs_ids = list(new_dictionary[-1])

    # print(feature_vector(graphs_file, subgraphs_file))
    pick_file = open('./feature_vector.pickle','wb')
    feature_vec = feature_vector(all_graphs_input, active_gspan_output, inactive_gspan_output, combined_gaston_format_output, act_subgraphs_count, inact_subgraphs_count, active_graphs_ids, inactive_graphs_ids)
    # print(feature_vec)
    pickle.dump(feature_vec,pick_file)
    pick_file.close()
