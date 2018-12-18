import os, sys
import pickle

# python3 final_script.py aido99_all.txt ca.txt ci.txt bullshit.txt 50 60
train_file = sys.argv[1]
active_file = sys.argv[2]
inactive_file = sys.argv[3]
test_file = sys.argv[4]
thresh_active = int(sys.argv[5])
thresh_inactive = int(sys.argv[6])

def execute_command(inp_file, out_file, count, thresh = 50):
	# print("executing " + "./gaston " + str(int(float(1.0 * thresh * count) * 0.01)) + " " + inp_file + " " + out_file)
	os.system("./gspan-executable -f " + inp_file + " -s " + str(float(1.0 * thresh) * 0.01)  + " -o -i")
	return

def main():

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
	act_count = pickle.load(pickle_in)
	inact_count = pickle.load(pickle_in)
	tot_count = pickle.load(pickle_in)

	active_subgraph_filename = './active_subgraph_' + str(thresh_active) + '.txt'
	inactive_subgraph_filename = './inactive_subgraph_' + str(thresh_inactive) + '.txt'
	execute_command(active_parsed, active_subgraph_filename, act_count, thresh_active)
	execute_command(inactive_parsed, inactive_subgraph_filename, inact_count, thresh_inactive)

	combined_file = 'sub_' + str(thresh_active) + '_' + str(thresh_inactive) + '.txt'
	active_subgraph_filename = str(active_subgraph_filename.split('/')[1])
	inactive_subgraph_filename = str(inactive_subgraph_filename.split('/')[1])
	os.system("cat " + active_subgraph_filename + " " + inactive_subgraph_filename + " > " + combined_file)
	print('TASK 2 DONE!')

	#task three
	combined_parsed = str(combined_parsed.split('/')[1])
	os.system("python3 feature_vector.py " + combined_parsed + " " + combined_file)
	kandus_pickle = './feature_vector.pickle'
	print('TASK 3 DONE!')

	#task four
	os.system("python3 convert_to_lib.py " + kandus_pickle + " " + label_dict + " libsvm.txt")
	print('TASK 4 DONE!')

	#task five
	os.system("./libsvm-3.23/svm-train -t 0 ../libsvm.txt")
	os.system("./libsvm-3.23/svm-predict ../libsvm.txt libsvm.txt.model output.txt")
	print('TASK 5 DONE!')

if __name__ == '__main__':
	main()