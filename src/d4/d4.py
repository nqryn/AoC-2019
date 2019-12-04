def is_in_range(digits, r_max):
	number = 0
	for i, d in enumerate(digits):
		number += d * 10**i
	if number > r_max:
		return False
	# print(number)
	return True

def is_valid(digits):
	distinct_digits = list(set(digits))
	for dd in distinct_digits:
		if digits.count(dd) == 2:
			return True	
	return False

def solve(r_min, r_max):
	# Count number in the range [r_min, r_max] which follow these rules:
	# - going from left to right, the digits never decrease
	# - at least two adjacent digits are the same
	digits = []
	while r_min > 0:
		digits.append(r_min % 10)
		r_min //=  10

	# find smallest number that works
	idx = 0
	while idx < len(digits) - 1:
		if digits[idx] < digits[idx + 1]:
			digits[idx] = digits[idx + 1]
			idx = 0
		else:
			idx += 1

	# Compute numbers
	cnt = 0
	idx = 0
	while is_in_range(digits, r_max):
		if is_valid(digits):
			cnt += 1
		if digits[idx] != 9:
			digits[idx] += 1
			continue
		while digits[idx] == 9:
			idx += 1
		digits[idx] += 1
		for i in range(0, idx):
			digits[i] = digits[idx]
		idx = 0
	return cnt


if __name__ == '__main__':
	range_min, range_max = 136760, 595730
	solution = solve(range_min, range_max)
	print(f'There are {solution} different passwords.')