import numpy as np
import sys

def main():
	complete_file = sys.argv[1]

	active_file = open(sys.argv[2],'r')
	act_mol = active_file.read().split('\n')
	active_file.close()

	inact_file = open('./inactives.txt','w')
	print(act_mol)

	print(len(act_mol))

	total = 0
	inact = 0
	with open(complete_file,'r') as fr:
		for line in fr:
			if line[0] == '#':
				total += 1
				mol_id = line.rstrip().strip()[1:]
				if mol_id not in act_mol: #then it is inactive
					inact += 1
					inact_file.write(mol_id + '\n')

	inact_file.close()

	print(total)
	print(inact)




if __name__ == '__main__':
	main()