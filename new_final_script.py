import os, sys
import pickle
from collections import defaultdict
from sklearn.metrics import f1_score
import numpy as np

# python3 new_final_script.py aido99_all.txt ca.txt ci.txt bullshit.txt 50 60
train_file = sys.argv[1]
active_file = sys.argv[2]
inactive_file = sys.argv[3]
test_file = sys.argv[4]
thresh_active = int(sys.argv[5])
thresh_inactive = int(sys.argv[6])

counter = 0
string_to_int = {}

def get_f_score(actual_filename, predicted_filename):
	y_pred = list(np.loadtxt(fname = predicted_filename))
	y_true = list(np.loadtxt(fname = actual_filename))
	return float(f1_score(y_true, y_pred))

def execute_command(inp_file, thresh = 50):
	# print("executing " + "./gaston " + str(int(float(1.0 * thresh * count) * 0.01)) + " " + inp_file + " " + out_file)
	string = "./gspan -f " + inp_file + " -s " + str(float(1.0 * thresh) * 0.01)  + " -o -i"
	print(string)
	os.system(string)
	return

def preprocess(input_string):
    global counter
    global string_to_int
    if input_string in string_to_int:
        return string_to_int[input_string]
    else:
        counter = counter + 1
        string_to_int[input_string] = counter
        return counter

def convert_format_gaston(filename, new_file):
	mol_mapping = defaultdict(lambda: -1)

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
					mol_mapping[line.strip()[1:]] = graph_counter
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
	return graph_counter, mol_mapping

def create_gaston_file(act_file, inact_file, out_file):
	#werite the code here
	of = open(out_file,'w')
	act_count = 0
	inact_count = 0
	with open(act_file,'r') as fr:
		for line in fr:
			if (line.strip() == '') or ((line.split()[0]) == 'x'):
				continue
			elif (line.split()[0] == 't'):
				act_count = act_count + 1
				of.write(line)
			else:
				of.write(line)

	with open(inact_file,'r') as fr:
		for line in fr:
			if (line.strip() == '') or ((line.split()[0]) == 'x'):
				continue
			elif (line.split()[0] == 't'):
				inact_count = inact_count + 1
				of.write(line)
			else:
				of.write(line)
	of.close()
	return act_count, inact_count

def do_something(vectors, label_mappings = {}): #converts to libsvm format

	vec_file = open(vectors,'rb')
	all_vecs = pickle.load(vec_file)
	vec_file.close()
	# vec_file.close()
	# all_vecs = [x.rstrip().strip().split() for x in feature_vecs]
	# all_vecs = np.array(all_vecs)

	num_graphs = all_vecs.shape[0]
	num_features = all_vecs.shape[1]


	out_file = open('./test.txt','w')

	for i in range(num_graphs):
		if not len(label_mappings) == 0:
			label = label_mappings[i]
		else:
			label = 0
		out_file.write(str(label))
		for j in range(num_features):
			out_file.write(' ' + str(j+1) + ':' + str(int(all_vecs[i][j])))
		out_file.write('\n')

	out_file.close()
	return

def main():
	global string_to_int
	global counter

	#task one - call get_graphs.py - return gaston format active, inactive and total files and true labels dict
	os.system("python3 get_graphs.py " + train_file + " " + active_file + " " + inactive_file)
	active_parsed = './aido99_active_gaston.txt'
	inactive_parsed = './aido99_inactive_gaston.txt'
	combined_parsed = './aido99_all_gaston.txt'
	label_dict = 'label_mapping.pickle'
	print('TASK 1 DONE!')

	#task two
	pickle_in = open(label_dict, 'rb')
	dictionary = pickle.load(pickle_in)

	active_subgraph_filename = active_parsed + '.fp'
	inactive_subgraph_filename = inactive_parsed + '.fp'
	execute_command(active_parsed, thresh_active)
	execute_command(inactive_parsed, thresh_inactive)

	#code for creating gaston format combined subgraohs file
	combined_file = 'sub_' + str(thresh_active) + '_' + str(thresh_inactive) + '.txt'
	act_count, inact_count = create_gaston_file(active_subgraph_filename, inactive_subgraph_filename, combined_file)
	print('TASK 2 DONE!')

	#task three
	os.system("python3 new_feature_vector.py " + combined_parsed + " " + active_subgraph_filename + " " + inactive_subgraph_filename + " " + combined_file + " " + str(act_count) + " " + str(inact_count))
	kandus_pickle = './feature_vector.pickle'
	print('TASK 3 DONE!')

	#task four
	os.system("python3 convert_to_lib.py " + kandus_pickle + " " + label_dict + " train.txt")
	print('TASK 4 DONE!')

	##for submission, comment this

	# # intermediate task 1 -> balance lib file
	# os.system("python3 balance_classes.py " + label_dict + " train.txt train_balanced.txt actual_train.txt")
	# print("INTERMEDIATE TASK 1 DONE")

	# #task five
	# os.system("./svm-train -t 0 ./train_balanced.txt")
	# os.system("./svm-predict ./train_balanced.txt train_balanced.txt.model output_train.txt")
	# print('TASK 5 DONE!')

	##till here

	#task six - convcert test file to gaston format using the bdindings of earlier mappings
	pickle_in = open('string_to_int_mapping.pickle', 'rb')
	string_to_int = pickle.load(pickle_in)
	counter = pickle.load(pickle_in)
	pickle_in.close()
	test_file_gaston = './test_gaston.txt'
	num_graphs, mol_mapping = convert_format_gaston(test_file, test_file_gaston)
	print('TASK 6 DONE!')

	#task 7 - convert test set to feature vectors
	os.system("python3 feature_vector.py " + test_file_gaston + " " + './new_subgraphs.pickle')
	label_mapping = defaultdict(lambda: -1)

# REMOVE THIS WHILE SUBMITTING

# 	active_files = open(active_file, 'r')
# 	active_mols = active_files.read().split('\n')
# 	active_mol = [mol_mapping[x.strip()] for x in active_mols]
	
# 	tot_count = 0

# 	with open(test_file_gaston,'r') as fr:
# 		for index,line in enumerate(fr):
# 			if line.split()[0] == 't':
# 				mol_id = int(line.split()[2].rstrip().strip())
# 				if mol_id in active_mol:
# 					label_mapping[tot_count] = 1
# 				tot_count += 1

# # TILL HERE

	do_something('./feature_vector_test.pickle', label_mapping)
	print("TASK 7 DONE!")

# 	# remove while submitting
# 	label_dict_new = open('./label_dict_new.pickle','wb')
# 	pickle.dump(dict(label_mapping),label_dict_new)
# 	label_dict_new.close()


# 	# Task 8 - run svm-predict
# 	os.system("python3 balance_classes.py label_dict_new.pickle test.txt libsvm_test_filtered.txt actual_test.txt")	

# 	os.system("./svm-predict ./libsvm_test_filtered.txt train_balanced.txt.model output_test.txt")
# 	print('TASK 8 DONE!')

# 	print('F Score for the train file : ' + str(get_f_score("actual_train.txt", "output_train.txt")))
# 	print('F Score for the test file : ' + str(get_f_score("actual_test.txt", "output_test.txt")))
	#till here


if __name__ == '__main__':
	main()
