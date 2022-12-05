import os
import csv
import numpy as np
import matplotlib.pyplot as plt

path_pre_net = os.getcwd() + '\data\pre_net_sorted.csv'
path_post_net = os.getcwd() + '\data\post_net_sorted.csv'

def read_csv(path):
	categories = []
	data = []

	with open(path) as data_file:
		data_csv = csv.reader(data_file)

		first = True
		for row in data_csv:
			if first:
				categories = row
				first, second = False, True
			else:
				data.append(row)

	counts = []
	data = np.transpose(np.array(data))
	
	for cc in range(data.shape[0]):
		cnt = 0
		for rr in range(data.shape[1]):
			if data[cc, rr] != '':
				cnt += 1
		
		counts.append(cnt)

	print("Categories: ", categories)
	print("    Counts: ", counts, '\n')
	
	return categories, counts, data

def plot_pie(pre, post):
	fig = plt.figure(figsize=(8,3))
	fig.add_subplot(121)
	plt.pie(pre[1], labels=pre[0])

	fig.add_subplot(122)
	plt.pie(post[1], labels=post[0])

	plt.show()

if __name__ == '__main__':
	pre_data = read_csv(path_pre_net)
	post_data = read_csv(path_post_net)

	plot_pie(pre_data, post_data)