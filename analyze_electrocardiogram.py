import numpy as np
import matplotlib.pyplot as plt

def identify_r(data):
	thvalue = 0.4
	r_candidate_range_list = []
	start = end = 0
	for i in range(1, len(data)):
		if not (data[i-1] >= thvalue) and data[i] >= thvalue:
			start = i
		if data[i-1] >= thvalue and not (data[i] >= thvalue):
			end = i
			r_candidate_range_list.append((start, end))

	r_list = []
	r_index_list = []
	for (start, end) in r_candidate_range_list:
		max_num = idx = -100
		for i in range(start, end):
			if data[i] >= max_num:
				max_num = data[i]
				idx = i
		r_list.append(max_num)
		r_index_list.append(idx)

	return r_index_list

def identify_pqst(data, r_index_list):
	return


f = open('./data_row.txt', 'r')
lines = f.read().split('\n')
f.close()

# datalist(mV per 2ms)
data = [float( (line.split('\t')[2]) ) for line in lines]

r_index_list = identify_r(data)

# 描画
plt.figure(figsize=(24,12))
plt.plot([i for i in range(len(data))], data)
plt.plot(r_index_list, [data[idx] for idx in r_index_list], 'o', color='red', label='R')
plt.minorticks_on()
plt.legend()
plt.savefig("./shindenzu.png")
