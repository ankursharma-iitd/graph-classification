import pickle

def get_labels(dict_file, out_file):
	pickle_in = open(dict_file,'rb')
	label_mapping = pickle.load(pickle_in)
	pickle_in.close()

	with open(out_file,'w') as fw:
		for i in range(len(label_mapping)):
			fw.write(str(label_mapping[i]) + '\n')



def main():
	train_dict = 'label_mapping.pickle'
	test_dict = 'label_dict_new.pickle'
	get_labels(train_dict, 'actual_train.txt')
	get_labels(test_dict,'actual_test.txt')



if __name__ == '__main__':
	main()