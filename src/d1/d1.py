def get_fuel(mass):
	fuel = 0
	while True:
		mass = mass // 3 - 2
		if mass <= 0:
			break
		fuel += mass
	return fuel

def solve_first():
	total = 0
	with open('d1.in', 'r') as f_in:
		for line in f_in:
			mass = int(line)
			fuel = get_fuel(mass)
			total += fuel
	return total

def solve_dp(rng):
	# Precompute all values using DP
	arr = [None] * rng
	arr[0] = 0
	for i in range(1, rng):
		fuel = max(0, i // 3 - 2)
		arr[i] = fuel + arr[fuel]
	
	# Solve
	total = 0
	with open('d1.in', 'r') as f_in:
		for line in f_in:
			mass = int(line)
			total += arr[mass]
	return total

if __name__ == '__main__':
	# Cheated a bit, and got the max value directly from the input file.
	total_fuel = solve_dp(15 * 10**4)
	print(f'Total fuel needed {total_fuel} L.')