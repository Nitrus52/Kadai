import math
import numpy as np
import matplotlib.pyplot as plt

def gaussian_calc(x, A, u, s):
	return float(A*math.exp(-1*math.pow(x-u, 2)/(2*math.pow(s, 2))))

def lorentzian_calc(x, A, u, d):
	return float(A*math.pow(d, 2)/(math.pow(d, 2) + pow(x-u, 2)))

f = open('./kadai4.txt', 'r')
lines = f.read().split('\n')
f.close()

# data
data = [float( (line.split('\t')[1]) ) for line in lines]

# guess
peak_str = [0, 0, (0, 0), (0, 0), (0, 0)]
peak_pos = [0, 0, (0, 0), (0, 0), (0, 0)]
width = [0, 0, (0, 0), (0, 0), (0, 0)]

# 1つ目の山
max_idx = max_num = -1
for i in range(200, 300):
	if data[i] > max_num:
		max_idx = i
		max_num = data[i]

hm = max_num/2
hm_idx1 = hm_idx2 = -1
for i in range(200, 300):
	if data[i-1] <= hm and hm <= data[i]:
		hm_idx1 = i
	if hm <= data[i] and data[i+1] <= hm:
		hm_idx2 = i

peak_str[0] = max_num
peak_pos[0] = max_idx
width[0] = hm_idx2-hm_idx1

print("1つ目の山：")
print(" ピーク強度：", peak_str[0])
print(" ピーク位置：", peak_pos[0]/10-100)
print(" 半値全幅：", width[0]/10)

# 2つ目の山
max_idx = max_num = -1
for i in range(400, 600):
	if data[i] > max_num:
		max_idx = i
		max_num = data[i]

hm = max_num/2
hm_idx1 = hm_idx2 = -1
for i in range(400, 600):
	if data[i-1] <= hm and hm <= data[i]:
		hm_idx1 = i
	if hm <= data[i] and data[i+1] <= hm:
		hm_idx2 = i

peak_str[1] = max_num
peak_pos[1] = max_idx
width[1] = hm_idx2-hm_idx1

print("2つ目の山：")
print(" ピーク強度：", peak_str[1])
print(" ピーク位置：", peak_pos[1]/10-100)
print(" 半値全幅：", width[1]/10)

# 3つ目の山
peak_str1 = peak_str2 = peak_idx1 = peak_idx2 = -1
count = 0
for i in range(800, 900):
	if data[i-1] <= data[i] and data[i+1] <= data[i]:
		if count == 0:
			peak_str1 = data[i]
			peak_idx1 = i
			count += 1
		if count == 1:
			peak_str2 = data[i]
			peak_idx2 = i

hm1 = peak_str1/2
hm2 = peak_str2/2
hm_idx1 = hm_idx2 = -1

for i in range(800, peak_idx1):
	if data[i-1] <= hm1 and hm1 <= data[i]:
		hm_idx1 = i

for i in range(peak_idx2, 900):
	if hm2 <= data[i] and data[i+1] <= hm2:
		hm_idx2 = i

peak_str[2] = (peak_str1, peak_str2)
peak_pos[2] = (peak_idx1, peak_idx2)
width[2] = ((peak_idx1-hm_idx1)*2, (hm_idx2-peak_idx2)*2)

print("3つ目の山：")
print(" 1つ目の関数：")
print("  ピーク強度：", peak_str[2][0])
print("  ピーク位置：", peak_pos[2][0]/10-100)
print("  半値全幅：", width[2][0]/10)
print(" 2つ目の関数：")
print("  ピーク強度：", peak_str[2][1])
print("  ピーク位置：", peak_pos[2][1]/10-100)
print("  半値全幅：", width[2][1]/10)

# 描画
guess_data = np.array([0.0 for i in range(len(data))])
guess_data += np.array([gaussian_calc(i, peak_str[0], peak_pos[0], width[0]/2) for i in range(len(data))])
guess_data += np.array([lorentzian_calc(i, peak_str[1], peak_pos[1], width[1]/2) for i in range(len(data))])
guess_data += np.array([gaussian_calc(i, peak_str[2][0], peak_pos[2][0], width[2][0]/2) for i in range(len(data))])
guess_data += np.array([gaussian_calc(i, peak_str[2][1], peak_pos[2][1], width[2][1]/2) for i in range(len(data))])

plt.figure(figsize=(24,12))
plt.plot([i/10-100 for i in range(len(data))], data)
plt.plot([i/10-100 for i in range(len(data))], guess_data, color='orange')
plt.minorticks_on()
plt.savefig("./curve_fit.png")
