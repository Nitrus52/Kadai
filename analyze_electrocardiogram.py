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

	r_index_list = []
	for (start, end) in r_candidate_range_list:
		max_num = max_num_idx = -100
		for i in range(start, end):
			if data[i] > max_num:
				max_num = data[i]
				max_num_idx = i
		r_index_list.append(max_num_idx)

	return r_index_list

def identify_pqst(data, r_index_list):
	k = 50
	p_index_list, q_index_list, s_index_list, t_index_list = [],[],[],[]

	for r_idx in r_index_list:
		j = 0

		# Qを特定
		while True:
			if data[r_idx-j-k] > data[r_idx-j]:
				min_num, min_num_idx = 100, -1
				for t in range(r_idx-j-k, r_idx-j):
					if data[t] < min_num:
						min_num = data[t]
						min_num_idx = t
				q_index_list.append(min_num_idx)
				break
			else:
				j += 1

		# Pを特定
		while True:
			if data[r_idx-j-k] < data[r_idx-j]:
				max_num = max_num_idx = -100
				for t in range(r_idx-j-k, r_idx-j):
					if data[t] > max_num:
						max_num = data[t]
						max_num_idx = t
				p_index_list.append(max_num_idx)
				break
			else:
				j += 1

		j = 0

		# Sを特定
		while True:
			if data[r_idx+j+k] > data[r_idx+j]:
				min_num, min_num_idx = 100, -1
				for t in range(r_idx+j, r_idx+j+k):
					if data[t] < min_num:
						min_num = data[t]
						min_num_idx = t
				s_index_list.append(min_num_idx)
				break
			else:
				j += 1

		# Tを特定
		while True:
			if data[r_idx+j+k] < data[r_idx+j]:
				max_num = max_num_idx = -100
				for t in range(r_idx+j, r_idx+j+k):
					if data[t] > max_num:
						max_num = data[t]
						max_num_idx = t
				t_index_list.append(max_num_idx)
				break
			else:
				j += 1

	return p_index_list, q_index_list, s_index_list, t_index_list

def print_statistics(p_index_list, q_index_list, r_index_list, s_index_list, t_index_list):
	p_diff_list, q_diff_list, r_diff_list, s_diff_list, t_diff_list = [],[],[],[],[]
	p_diff_list = [(p_index_list[i]-p_index_list[i-1])*2 for i in range(1, len(p_index_list))]
	q_diff_list = [(q_index_list[i]-q_index_list[i-1])*2 for i in range(1, len(q_index_list))]
	r_diff_list = [(r_index_list[i]-r_index_list[i-1])*2 for i in range(1, len(r_index_list))]
	s_diff_list = [(s_index_list[i]-s_index_list[i-1])*2 for i in range(1, len(s_index_list))]
	t_diff_list = [(t_index_list[i]-t_index_list[i-1])*2 for i in range(1, len(t_index_list))]

	p_ave = q_ave = r_ave = s_ave = t_ave = 0
	p_ave = sum(p_diff_list)/len(p_diff_list)
	q_ave = sum(q_diff_list)/len(q_diff_list)
	r_ave = sum(r_diff_list)/len(r_diff_list)
	s_ave = sum(s_diff_list)/len(s_diff_list)
	t_ave = sum(t_diff_list)/len(t_diff_list)

	p_var = q_var = r_var = s_var = t_var = 0
	p_var = sum([(val-p_ave)**2 for val in p_diff_list])/(len(p_diff_list)-1)
	q_var = sum([(val-q_ave)**2 for val in q_diff_list])/(len(q_diff_list)-1)
	r_var = sum([(val-r_ave)**2 for val in r_diff_list])/(len(r_diff_list)-1)
	s_var = sum([(val-s_ave)**2 for val in s_diff_list])/(len(s_diff_list)-1)
	t_var = sum([(val-t_ave)**2 for val in t_diff_list])/(len(t_diff_list)-1)

	print("Pの平均値：{:.2f}[ms], Pの不偏標準誤差：{:.2f}".format( p_ave, np.sqrt( p_var/len(p_diff_list) ) ))
	print("Qの平均値：{:.2f}[ms], Qの不偏標準誤差：{:.2f}".format( q_ave, np.sqrt( q_var/len(q_diff_list) ) ))
	print("Rの平均値：{:.2f}[ms], Rの不偏標準誤差：{:.2f}".format( r_ave, np.sqrt( r_var/len(r_diff_list) ) ))
	print("Sの平均値：{:.2f}[ms], Sの不偏標準誤差：{:.2f}".format( s_ave, np.sqrt( s_var/len(s_diff_list) ) ))
	print("Tの平均値：{:.2f}[ms], Tの不偏標準誤差：{:.2f}".format( t_ave, np.sqrt( t_var/len(t_diff_list) ) ))


f = open('./data_row.txt', 'r')
lines = f.read().split('\n')
f.close()

# datalist(mV per 2ms)
data = [float( (line.split('\t')[2]) ) for line in lines]

r_index_list = identify_r(data)
p_index_list, q_index_list, s_index_list, t_index_list = identify_pqst(data, r_index_list)

# 描画
plt.figure(figsize=(24,12))
plt.plot([i for i in range(len(data))], data)
plt.plot(p_index_list, [data[idx] for idx in p_index_list], 'o', color='orange', label='P')
plt.plot(q_index_list, [data[idx] for idx in q_index_list], 'o', color='green', label='Q')
plt.plot(r_index_list, [data[idx] for idx in r_index_list], 'o', color='red', label='R')
plt.plot(s_index_list, [data[idx] for idx in s_index_list], 'o', color='black', label='S')
plt.plot(t_index_list, [data[idx] for idx in t_index_list], 'o', color='purple', label='T')
plt.minorticks_on()
plt.legend()
plt.savefig("./shindenzu.png")

# 統計情報
print_statistics(p_index_list, q_index_list, r_index_list, s_index_list, t_index_list)
