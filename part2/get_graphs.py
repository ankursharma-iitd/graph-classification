import numpy as np
import sys
from collections import defaultdict
import pickle

string_to_int = {}
counter = 0

def preprocess(input_string):
    global counter
    if input_string in string_to_int:
        return string_to_int[input_string]
    else:
        counter = counter + 1
        string_to_int[input_string] = counter
        return counter


def convert_format_gaston(filename, new_file):
    graph_counter = 0
    vertex_counter = 0
    edge_counter = 0
    num_vertices = float("inf")
    flag = False
    start_flag = False
    end_flag = False
    final_flag = False
    num_edges = float("inf")
    with open(filename, 'r+') as fr:
        with open(new_file, 'w+') as fw:
            for line in fr:
                new_line = ''
                if ((line[:1] == '#') and not (start_flag) and not (flag)
                        and not (end_flag) and not (final_flag)):
                    new_line = 't # ' + str(graph_counter) + '\n'
                    flag = True
                    graph_counter = graph_counter + 1
                elif (flag and not (start_flag) and not (end_flag)
                      and not (final_flag)):
                    num_vertices = int(line)
                    # print('NUM VERTICES : ' + str(num_vertices))
                    start_flag = True
                    flag = False
                elif (start_flag and not (flag) and not (end_flag)
                      and not (final_flag)):
                    split_list = line.split(' ')
                    new_line = 'v ' + str(vertex_counter) + ' ' + str(preprocess(split_list[0].strip())) + '\n'
                    if (vertex_counter == (num_vertices - 1)):
                        vertex_counter = 0
                        end_flag = True
                        start_flag = False
                    vertex_counter = vertex_counter + 1
                elif (end_flag and not (start_flag) and not (flag)
                      and not (final_flag)):
                    num_edges = int(line)
                    # print('NUM EDGES : ' + str(num_edges))
                    final_flag = True
                    end_flag = False
                elif (final_flag and not (end_flag) and not (start_flag)
                      and not (flag)):
                    split_list = line.split(' ')
                    new_line = 'e ' + str(split_list[0]) + ' ' + str(split_list[1]) + ' ' + str(preprocess(split_list[2].strip())) + '\n'
                    edge_counter = edge_counter + 1
                    if (edge_counter == (num_edges)):
                        edge_counter = 0
                        final_flag = False
                        flag = False
                        start_flag = False
                        end_flag = False
                        vertex_counter = 0
                fw.write(new_line)
            fw.close()
        fr.close()
    return graph_counter



def main():
    mol_file = sys.argv[1]
    active_file = open(sys.argv[2], 'r')
    active_mol = active_file.read().split('\n')
    active_file.close()
    inactive_file = open(sys.argv[3],'r')
    inactive_mol = inactive_file.read().split('\n')
    inactive_file.close()

    mol_mapping = defaultdict(lambda: -1)

    with open(mol_file,'r') as fr:
    	for index,line in enumerate(fr):
    		if line[0] == '#':
    			mol_id = line[1:].rstrip().strip()
    			mol_mapping[mol_id] = len(mol_mapping)

    new_file = mol_file[:len(mol_file) - 4] + '_parsed_gaston.txt'
    num_graphs = convert_format_gaston(mol_file, new_file)

    out_active = open('./aido99_active_gaston.txt','w')
    out_inactive = open('./aido99_inactive_gaston.txt','w')
    out_all = open('./aido99_all_gaston.txt','w')

    active_mol = [mol_mapping[x] for x in active_mol]
    inactive_mol = [mol_mapping[x] for x in inactive_mol]

    flag = 0
    flag_ = 0
    act_count = 0
    inact_count = 0
    tot_count = 0
    label_mapping = {}

    with open(new_file,'r') as fr:
        for index,line in enumerate(fr):
            if line.split()[0] == 't':
            	mol_id = int(line.split()[2].rstrip().strip())
            	if mol_id in active_mol:
            		flag = 1
            		flag_ = 1
            	elif mol_id in inactive_mol:
            		flag = 2
            		flag_ = 1
            	else:
            		flag = 0
            		flag_ = 0
            if flag == 1:
            	if line.split()[0] == 't':
            		out_active.write('t # ' + str(act_count) + '\n')
            		act_count += 1
            	else:
            		out_active.write(line)
            elif flag == 2:
            	if line.split()[0] == 't':
            		out_inactive.write('t # ' + str(inact_count) + '\n')
            		inact_count += 1
            	else:
            		out_inactive.write(line)
            if flag_ == 1:
            	if line.split()[0] == 't':
                    out_all.write('t # ' + str(tot_count) + '\n')
                    if flag == 1:
                        label_mapping[tot_count] = 1
                    elif flag == 2:
                        label_mapping[tot_count] = -1
                    tot_count += 1
            	else:
            		out_all.write(line)
    pickle_file = open('label_mapping.pickle','wb')
    pickle.dump(label_mapping,pickle_file)
    pickle_file.close()




	
















if __name__ == '__main__':
	main()