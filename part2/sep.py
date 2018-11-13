# args - 
# 0 molecule file
# 1 active molecules
# 2 inactive molecules

import numpy as np
import sys


def main():
	mol_file = sys.argv[1]
	active_file = open(sys.argv[2], 'r')
	active_mol = active_file.read().split('\n')
	active_file.close()
	inactive_file = open(sys.argv[3],'r')
	inactive_mol = inactive_file.read().split('\n')
	inactive_file.close()

	out_active = open('./aido99_active.txt','w')
	out_inactive = open('./aido99_inactive.txt','w')

	test = open("./test.txt",'w')

	flag = 0
	act_count = 0
	inact_count = 0

	with open(mol_file, 'r') as fr:
		for line in fr:
			if line[0] == '#': #new molecule
				mol_id = line[1:].rstrip().strip()
				if mol_id in active_mol:
					# out_active.write(line)
					test.write(mol_id + '\n')
					flag = 1
					act_count += 1
				elif mol_id in inactive_mol:
					# out_inactive.write(line)
					flag = 2
					inact_count += 1
				else:
					flag = 0

			if flag == 1:
				out_active.write(line)
				
			if flag == 2:
				out_inactive.write(line)

	out_active.close()
	out_inactive.close()
	test.close()

	print("active molecules " + str(act_count))
	print("inactive molecules " + str(inact_count))




			








if __name__ == '__main__':
	main()