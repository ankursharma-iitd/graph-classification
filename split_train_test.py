# inps - combined file, active file, inactive file
import numpy as np
import pickle
import sys

def main():
	combined_file = sys.argv[1]

	act_file = open(sys.argv[2],'r')
	act_id = act_file.read().split('\n')
	act_file.close()

	inact_file = open(sys.argv[3],'r')
	inact_id = inact_file.read().split('\n')
	inact_file.close()

	train_file = open('./train_bc.txt','w')
	test_file = open('./test_bc.txt','w')

	inact_count = 0
	act_count = 0

	num_act = 200
	num_inact = 5000

	flag = 0
	with open(combined_file,'r') as fr:
		for line in fr:
			if line[0] == '#': #new molecule
				mol_id = line.rstrip().strip()[1:]
				if mol_id in act_id:
					if act_count < num_act:
						flag = 1 #write in test file
					else:
						flag = 2 #write in train file
					act_count += 1
				elif mol_id in inact_id:
					if inact_count < num_inact:
						flag = 1 #write in test file
					else:
						flag = 2 #write in train file
					inact_count += 1
				else:
					flag = 0

			if flag == 1: #write in test
				test_file.write(line)
			elif flag == 2:
				train_file.write(line)














if __name__ == '__main__':
	main()








