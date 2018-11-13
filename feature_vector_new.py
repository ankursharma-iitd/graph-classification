import networkx as nx
import numpy as np
# import networkx.algorithms.isomorphism as iso
import sys
import graph_tool as gt

#conversion of networkx to graph tools adopted from "https://gist.github.com/bbengfort/a430d460966d64edc6cad71c502d7005"
def get_prop_type(value, key=None):
    """
    Performs typing and value conversion for the graph_tool PropertyMap class.
    If a key is provided, it also ensures the key is in a format that can be
    used with the PropertyMap. Returns a tuple, (type name, value, key)
    """
    if isinstance(key, unicode):
        # Encode the key as ASCII
        key = key.encode('ascii', errors='replace')

    # Deal with the value
    if isinstance(value, bool):
        tname = 'bool'

    elif isinstance(value, int):
        tname = 'float'
        value = float(value)

    elif isinstance(value, float):
        tname = 'float'

    elif isinstance(value, unicode):
        tname = 'string'
        value = value.encode('ascii', errors='replace')

    elif isinstance(value, dict):
        tname = 'object'

    else:
        tname = 'string'
        value = str(value)

    return tname, value, key

def nx2gt(nxG):
    """
    Converts a networkx graph to a graph-tool graph.
    """
    # Phase 0: Create a directed or undirected graph-tool Graph
    gtG = gt.Graph(directed=nxG.is_directed())

    # Add the Graph properties as "internal properties"
    for key, value in nxG.graph.items():
        # Convert the value and key into a type for graph-tool
        tname, value, key = get_prop_type(value, key)

        prop = gtG.new_graph_property(tname) # Create the PropertyMap
        gtG.graph_properties[key] = prop     # Set the PropertyMap
        gtG.graph_properties[key] = value    # Set the actual value

    # Phase 1: Add the vertex and edge property maps
    # Go through all nodes and edges and add seen properties
    # Add the node properties first
    nprops = set() # cache keys to only add properties once
    for node, data in nxG.nodes_iter(data=True):

        # Go through all the properties if not seen and add them.
        for key, val in data.items():
            if key in nprops: continue # Skip properties already added

            # Convert the value and key into a type for graph-tool
            tname, _, key  = get_prop_type(val, key)

            prop = gtG.new_vertex_property(tname) # Create the PropertyMap
            gtG.vertex_properties[key] = prop     # Set the PropertyMap

            # Add the key to the already seen properties
            nprops.add(key)

    # Also add the node id: in NetworkX a node can be any hashable type, but
    # in graph-tool node are defined as indices. So we capture any strings
    # in a special PropertyMap called 'id' -- modify as needed!
    gtG.vertex_properties['id'] = gtG.new_vertex_property('string')

    # Add the edge properties second
    eprops = set() # cache keys to only add properties once
    for src, dst, data in nxG.edges_iter(data=True):

        # Go through all the edge properties if not seen and add them.
        for key, val in data.items():
            if key in eprops: continue # Skip properties already added

            # Convert the value and key into a type for graph-tool
            tname, _, key = get_prop_type(val, key)

            prop = gtG.new_edge_property(tname) # Create the PropertyMap
            gtG.edge_properties[key] = prop     # Set the PropertyMap

            # Add the key to the already seen properties
            eprops.add(key)

    # Phase 2: Actually add all the nodes and vertices with their properties
    # Add the nodes
    vertices = {} # vertex mapping for tracking edges later
    for node, data in nxG.nodes_iter(data=True):

        # Create the vertex and annotate for our edges later
        v = gtG.add_vertex()
        vertices[node] = v

        # Set the vertex properties, not forgetting the id property
        data['id'] = str(node)
        for key, value in data.items():
            gtG.vp[key][v] = value # vp is short for vertex_properties

    # Add the edges
    for src, dst, data in nxG.edges_iter(data=True):

        # Look up the vertex structs from our vertices mapping and add edge.
        e = gtG.add_edge(vertices[src], vertices[dst])

        # Add the edge properties
        for key, value in data.items():
            gtG.ep[key][e] = value # ep is short for edge_properties

    # Done, finally!
    return gtG

def parse_gaston_to_nx(filename):
    Graphs = []
    with open(filename, 'r') as graph_file:
        while True:
            line = graph_file.readline()
            if line == "":
                break
            if line[0] == 't':
                # start a new Graph
                g = nx.Graph()
                while True:
                    last_pos = graph_file.tell()
                    nl = graph_file.readline()
                    if nl == "":
                        graph_file.seek(last_pos)
                        break
                    nl_split = nl.split()
                    print(nl_split)
                    if nl_split[0] == 'v':
                        g.add_node(nl_split[1], label=nl_split[2])
                    elif nl_split[0] == 'e':
                        g.add_edge(nl_split[1], nl_split[2], label=nl_split[3])
                    elif nl_split[0] == 't':
                        graph_file.seek(last_pos)
                        Graphs.append(nx2gt(g))
                        break
    return Graphs


def feature_vector(graphs_file, subgraphs_file):
    graphs = parse_gaston_to_nx(graphs_file)
    subGraphs = parse_gaston_to_nx(subgraphs_file)
    exit()
    feature_vector = np.zeros((len(graphs), len(subGraphs)))

    for s_idx, subgraph in enumerate(subGraphs):
        for g_idx, graph in enumerate(graphs):
            GM = iso.GraphMatcher(
                graph,
                subgraph,
                node_match=iso.categorical_node_match('label', ''),
                edge_match=iso.categorical_edge_match('label', ''))
            if GM.subgraph_is_isomorphic():
                feature_vector[g_idx][s_idx] = 1.0

    return feature_vector


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python feature_vector.py graphs_file subgraphs_file")
        exit(-1)
    graphs_file = sys.argv[1]
    subgraphs_file = sys.argv[2]

    print(feature_vector(graphs_file, subgraphs_file))
