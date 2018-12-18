import numpy as np
import sys, os
import pickle

def main():
	label_file = sys.argv[1]
	in_file = sys.argv[2]
	out_file = sys.argv[3]

	actual_labels_file = sys.argv[4]

	pickle_in = open(label_file, 'rb')
	dictionary = dict(pickle.load(pickle_in))
	pickle_in.close()

	new_dictionary = dict()
	for key in dictionary:
	    value = dictionary[key]
	    if value in new_dictionary:
	        new_dictionary[value] = new_dictionary[value] + list([int(key)])
	    else:
	        new_dictionary[value] = list([int(key)])

	active_graphs_ids = np.array(list(new_dictionary[1]))
	inactive_graphs_ids = np.array(list(new_dictionary[-1]))

	num_active = len(active_graphs_ids)

	filtered_inactive_ids = inactive_graphs_ids[np.random.choice(len(inactive_graphs_ids), size=num_active, replace=False)]

	fw = open(out_file,'w')
	fw1 = open(actual_labels_file,'w')

	with open(in_file,'r') as fr:
		for index,line in enumerate(fr):
			if (index in active_graphs_ids) or (index in filtered_inactive_ids):	
				fw.write(line)
			if index in active_graphs_ids:
				fw1.write('1\n')
			elif index in filtered_inactive_ids:
				fw1.write('-1\n')
	fw.close()
	fw1.close()







if __name__ == '__main__':
	main()