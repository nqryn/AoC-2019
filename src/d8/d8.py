from collections import Counter

def solve_first(w=25, h=6):
	with open('d8.in') as fin:
		digits = fin.readline()

	min_zeroes = w * h
	solution = 0

	layers_cnt = len(digits) // (w * h)
	for i in range(layers_cnt):
		counters = Counter(digits[w*h*i:w*h*(i+1)])
		if counters['0'] < min_zeroes:
			min_zeroes = counters['0']
			solution = counters['1'] * counters['2']
	return solution

def solve_second(w=25, h=6):
	with open('d8.in') as fin:
		digits = fin.readline()

	visible_layer = ['2'] * (w * h)
	layers_cnt = len(digits) // (w * h)
	for i in range(layers_cnt):
		curr_layer = digits[w*h*i:w*h*(i+1)]
		for j in range(w * h):
			if visible_layer[j] == '2':
				visible_layer[j] = curr_layer[j]

	print('0' * w)
	for i in range(h):
		print(''.join(visible_layer[w*i:w*(i+1)]).replace('1', ' '))
	print('0' * w)

if __name__ == '__main__':
	# Not easy to read ascii, the image was JAFRA
	solve_second()