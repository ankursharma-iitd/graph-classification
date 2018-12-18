import numpy as np
import sys
import pickle

def main():
	active_file = sys.argv[1]
	inactive_file = sys.argv[2]
	samples = int(sys.argv[3])

	act_count = 0
	inact_count = 0

	new_act_file = active_file.split('.')[0] + '_' + str(samples) + '_samples.txt'
	new_inact_file = inactive_file.split('.')[0] + '_' + str(samples) + '_samples.txt'
	new_tot_file = 'total_' + str(samples) + '_samples.txt'

	af = open(new_act_file,'w')
	inf = open(new_inact_file,'w')
	tf = open(new_tot_file,'w')

	with open(active_file,'r') as fr:
		for line in fr:
			# for training set
			if line.split()[0] == 't':
				act_count += 1
			if act_count > samples:
				break
			af.write(line)
			tf.write(line)

			# for test set
			# if line.split()[0] == 't':
			# 	act_count += 1
			# if act_count <= samples:
			# 	continue
			# else:
			# 	af.write(line)
			# 	tf.write(line)

	with open(inactive_file,'r') as fr:
		for line in fr:
			if line.split()[0] == 't':
				inact_count += 1
			if inact_count > samples:
				break
			inf.write(line)

			if line.split()[0] == 't':
				tf.write('t # ' + str(samples+inact_count-1) + '\n')
			else:
				tf.write(line)

			# for test
			# if line.split()[0] == 't':
			# 	inact_count += 1
			# if inact_count <= samples:
			# 	continue
			# if inact_count > 200+samples:
			# 	break
			# else:
			# 	inf.write(line)
			# 	tf.write(line)


	af.close()
	inf.close()
	tf.close()

	new_label_mapping = {}
	# for i in range(2*samples):
	# 	if i < samples:
	# 		new_label_mapping[i] = 1
	# 	else:
	# 		new_label_mapping[i] = -1

	print(act_count)
	print(inact_count)

	for i in range(act_count + inact_count):
		if i < act_count:
			new_label_mapping[i] = 1
		else:
			new_label_mapping[i] = -1
	# print(new_label_mapping)




	pickle_file = open('new_label_mapping.pickle','wb')
	pickle.dump(new_label_mapping,pickle_file)
	pickle_file.close()









if __name__ == '__main__':
	main()