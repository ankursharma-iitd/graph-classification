import numpy as np
import pickle
import sys

def main():
	vec_file = open(sys.argv[1],'rb')
	all_vecs = pickle.load(vec_file)
	vec_file.close()
	# vec_file.close()
	# all_vecs = [x.rstrip().strip().split() for x in feature_vecs]
	# all_vecs = np.array(all_vecs)

	num_graphs = all_vecs.shape[0]
	num_features = all_vecs.shape[1]

	print(num_graphs)
	print(num_features)

	dict_file = open(sys.argv[2],'rb')
	label_mappings = pickle.load(dict_file)
	dict_file.close()

	out_file = open(sys.argv[3],'w')

	for i in range(num_graphs):
		label = label_mappings[i]
		out_file.write(str(label))
		for j in range(num_features):
			out_file.write(' ' + str(j+1) + ':' + str(int(all_vecs[i][j])))
		out_file.write('\n')

	out_file.close()


	








if __name__ == '__main__':
	main()