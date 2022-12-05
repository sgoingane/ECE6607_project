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

def get_movement_matrix(pre, post):
	categories = pre[0]
	pre_data = pre[2]
	post_data = post[2]

	movement = np.zeros((len(categories), len(categories)))

	for cc in range(pre_data.shape[0]):
		for rr in range(pre_data.shape[1]):
			if pre_data[cc, rr] != '':
				found = np.where(post_data==pre_data[cc, rr])

				if found:
					for f in range(len(found[0])):
						movement[cc, found[0][f]] += 1
	print(movement)
	return movement

def plot_pie(pre, post):
	fig = plt.figure(figsize=(8,3))
	fig.add_subplot(121)
	plt.pie(pre[1], labels=pre[0])

	fig.add_subplot(122)
	plt.pie(post[1], labels=post[0])

	plt.show()

def plot_heatmap(pre, post):
	move = get_movement_matrix(pre, post)

	fig = plt.figure(figsize=(5,5))
	plt.xlabel('To'), plt.ylabel('From')
	plt.xticks(ticks=np.arange(len(pre[0])), labels=pre[0], rotation=90)
	plt.yticks(ticks=np.arange(len(pre[0])), labels=pre[0])

	hm = plt.imshow(move, cmap='inferno')
	plt.colorbar(hm)

	plt.tight_layout(), plt.show()

if __name__ == '__main__':
	pre_data = read_csv(path_pre_net)
	post_data = read_csv(path_post_net)

	# plot_pie(pre_data, post_data)
	plot_heatmap(pre_data, post_data)