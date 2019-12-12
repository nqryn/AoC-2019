epsilon = 2.220446049250313e-10

class Asteroid:

	def __init__(self, pos_i, pos_j):
		self.i = pos_i
		self.j = pos_j

	def __eq__(self, other):
		return (self.i == other.i) and (self.j == other.j)

	def sees(self, other):
		# special cases: same line / row
		if self.j == other.j:
			for i in range(min(self.i, other.i) + 1, max(self.i, other.i)):
				if self.ast_map[i][self.j]:
					return False
			return True
		if self.i == other.i:
			for j in range(min(self.j, other.j) + 1, max(self.j, other.j)):
				if self.ast_map[self.i][j]:
					return False
			return True
		# Regular cases: compute slope and y-intercept
		m = (self.i - other.i) / (self.j - other.j)
		n = self.i - m * self.j
		for i in range(min(self.i, other.i) + 1, max(self.i, other.i)):
			j = (i - n) / m
			is_int = abs(round(j) - j) < epsilon
			if is_int and (0 <= j < self.map_size) and self.ast_map[i][round(j)]:
				return False
		return True

	def count_seen(self, ast_map, asteroids):
		self.ast_map = ast_map
		self.map_size = len(ast_map)
		seen_cnt = 0

		for a in asteroids:
			if a != self and self.sees(a):
				# if hasattr(a, 'ast_map') and not a.sees(self):
				# 	print(self.i, self.j, a.i, a.j)
				seen_cnt += 1

		return seen_cnt


def solve():
	ast_map = []
	with open('d10.in') as fin:
		for line in fin:
			ast_map.append([1 if c == '#' else 0 for c in line.strip()])
		
	map_size = len(ast_map)
	asteroids = []

	for i in range(map_size):
		for j in range(map_size):
			if ast_map[i][j]:
				asteroid = Asteroid(i, j)
				ast_map[i][j] = asteroid
				asteroids.append(asteroid)

	for i in range(map_size):
		for j in range(map_size):
			if not ast_map[i][j]:
				print(' ___ ', end='')
			else:
				print(f' {ast_map[i][j].count_seen(ast_map, asteroids)} ', end='')
		print()
	
	max_seen = 0
	max_location = 0
	print(f'There are {len(asteroids)} astroids')
	for a in asteroids:
		sees = a.count_seen(ast_map[:], asteroids)
		if sees > max_seen:
			max_seen = sees
			max_location = (a.i, a.j)

	return max_seen, max_location


if __name__ == '__main__':
	best_seen, best_location = solve()
	print(f' - How many other asteroids can be detected from the best location?\n - {best_seen}\n')
	print(f' - From where?\n - {best_location}')