from itertools import cycle
from functools import reduce # only in Python 3
import time


def get_patterns(size):
	# Pattern = [0, 1, 0, -1] based on position
	base_pattern = [0, 1, 0, -1]
	patterns = []
	for s in range(size):
		curr_pattern = []
		base_cycle = cycle(base_pattern)
		next_val = next(base_cycle)
		while len(curr_pattern) - 1 < size:
			curr_pattern.extend([next_val] * (s + 1))
			next_val = next(base_cycle)
		patterns.append(curr_pattern[1:size + 1])
	return patterns

def compute_phase(in_digits, size, patterns):
	out_digits = [0] * size

	for i in range(size):
		out_digits[i] = reduce((lambda x, y: x + y), [in_digits[j] * patterns[i][j] for j in range(size)])
		out_digits[i] = abs(out_digits[i]) % 10

	return out_digits

def fast_compute_phase(in_digits, size):
	out_digits = [0] * size
	# plus, skip, minus, skip
	operations = [
		lambda arr: sum(arr),
		lambda arr: 0,
		lambda arr: -sum(arr),
		lambda arr: 0
	]
	for i in range(size):
		# print(f'{i}: ', end=' ')
		for j in range(i, size, i + 1):
			op_idx = ((j - i) // (i + 1)) % 4
			out_digits[i] += operations[op_idx](in_digits[j: j + i + 1])
			# print(f'{in_digits[j: j + i + 1]}', end=' + ')
		# print(f' = {out_digits[i]}', end=' ')
		out_digits[i] = abs(out_digits[i]) % 10
		# print(f' => {out_digits[i]}')
	return out_digits


def main():
	with open('d16.in', 'r') as fin:
		digits = fin.readline()
		digits = [int(d) for d in digits]
	
	real_digits = []
	for _ in range(10000):
		real_digits.extend(digits)
	size = len(real_digits)


	t1 = time.time()

	for _ in range(100):
		real_digits = fast_compute_phase(real_digits, size)
		print('.', end='')

	t2 = time.time()
	print(f'\nTime fast: {t2 - t1}')

if __name__ == '__main__':
	main()