from __future__ import print_function
import os
from matplotlib import pyplot as plt
import timeit
import sys
import subprocess
import numpy as np
import _pickle as cPickle
filepath = os.path.dirname(os.path.abspath(__file__))

string_to_int = {}
counter = 0

pickle_out = open("stuff.pickle", "wb")

def preprocess(input_string):
    global counter
    if input_string in string_to_int:
        return string_to_int[input_string]
    else:
        counter = counter + 1
        string_to_int[input_string] = counter
        return counter

def convert_format_gspan(filename, new_file):
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
                    new_line = 'v ' + str(vertex_counter) + ' ' + str(line)
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
                    new_line = 'e ' + str(line)
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

def convert_format_fsg(filename, new_file):
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
                    new_line = 'v ' + str(vertex_counter) + ' ' + str(line)
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
                    new_line = 'u ' + str(line)
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

# thresholds = [5, 10, 25, 50, 95]
thresholds = [90]

# Please install gspan_mining from "pip3 install gspan-mining"
def gspan(filename):
    filename = os.path.join(filepath, filename)
    new_file = filename[:len(filename) - 4] + '_parsed_gspan.txt'
    num_graphs = convert_format_gspan(filename, new_file) + 1
    print('FILE PARSED GSPAN.')
    execution_times_gpsan = [
        timeit.timeit(
            "subprocess.run(\"python3 -m gspan_mining -s " + str(
                int(float(1.0 * x * num_graphs) * 0.01)) + " " + new_file
            + "\", shell=True)",
            setup="import subprocess",
            number=1) for x in thresholds
    ]
    return execution_times_gpsan

def fsg(filename):
    filename = os.path.join(filepath, filename)
    new_file = filename[:len(filename) - 4] + '_parsed_fsg.txt'
    num_graphs = convert_format_fsg(filename, new_file) + 1
    print('FILE PARSED FSG.')
    execution_times_fsg = [
        timeit.timeit(
            "subprocess.run(\"./pafi-1.0.1/Linux/fsg -s " + str(x) + " " +
            new_file + "\", shell=True)",
            setup="import subprocess",
            number=1) for x in thresholds
    ]
    return execution_times_fsg

def gaston(filename):
    filename = os.path.join(filepath, filename)
    new_file = filename[:len(filename) - 4] + '_parsed_gaston.txt'
    num_graphs = convert_format_gaston(filename, new_file) + 1
    print('FILE PARSED GASTON.')
    execution_times_gaston = [
        timeit.timeit(
            "subprocess.run(\"./gaston-1.1-re/gaston -s " + str(
                int(float(1.0 * x * num_graphs) * 0.01)) + " " + new_file +
            "\", shell=True)",
            setup="import subprocess",
            number=1) for x in thresholds
    ]
    return execution_times_gaston

def plot(gspan, fsg, gaston):
    plt.figure()
    plt.plot(thresholds, gspan, label='gspan')
    plt.plot(thresholds, fsg, label='fsg')
    plt.plot(thresholds, gaston, label='gaston')
    plt.title('Execution time comparison')
    plt.xlabel('Support threshold')
    plt.ylabel('Execution Time (s)')
    plt.legend()
    plt.show()
    return

if __name__ == '__main__':
    kwargs = {}
    if len(sys.argv) > 1:
        kwargs['filename'] = sys.argv[1]
    if len(sys.argv) > 2:
        sys.exit(
            "Not correct arguments provided. Use %s -h for more information"
            % (sys.argv[0]))
    execution_times_gspan = gspan(**kwargs)
    cPickle.dump(execution_times_gspan, pickle_out)
    execution_times_gaston = gaston(**kwargs)
    cPickle.dump(execution_times_gaston, pickle_out)
    execution_times_fsg = fsg(**kwargs)
    cPickle.dump(execution_times_fsg, pickle_out)
    pickle_out.close()
    plot(execution_times_gspan, execution_times_fsg, execution_times_gaston)