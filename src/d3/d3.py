

def solve():
	w1, w2 = [], []
	with open('d3.in', 'r') as fin:
		w1 = fin.readline().split(',')
		w2 = fin.readline().split(',')

	curr_x, curr_y = 0, 0
	w1_positions = dict()
	curr_steps = 0
	new_pos = None
	for val in w1:
		steps = int(val[1:])
		if val.startswith('U'):
			for x in range(curr_x, curr_x - steps, -1):
				if (x, curr_y) not in w1_positions:
					w1_positions[(x, curr_y)] = curr_steps + (curr_x - x)
			curr_x -= steps
		elif val.startswith('D'):
			for x in range(curr_x, curr_x + steps):
				if (x, curr_y) not in w1_positions:
					w1_positions[(x, curr_y)] = curr_steps + x - curr_x
			curr_x += steps
		elif val.startswith('L'):
			for y in range(curr_y, curr_y - steps, -1):
				if (curr_x, y) not in w1_positions:
					w1_positions[(curr_x, y)] = curr_steps + (curr_y - y)
			new_pos = [ ]
			curr_y -= steps
		elif val.startswith('R'):
			for y in range(curr_y, curr_y + steps):
				if (curr_x, y) not in w1_positions:
					w1_positions[(curr_x, y)] = curr_steps + y - curr_y
			curr_y += steps
		curr_steps += steps

	# Second wire
	curr_y, curr_x = 0, 0
	curr_steps = 0
	w2_positions = dict()
	for val in w2:
		steps = int(val[1:])
		if val.startswith('U'):
			for x in range(curr_x, curr_x - steps, -1):
				if (x, curr_y) not in w2_positions:
					w2_positions[(x, curr_y)] = curr_steps + (curr_x - x)
			curr_x -= steps
		elif val.startswith('D'):
			for x in range(curr_x, curr_x + steps):
				if (x, curr_y) not in w2_positions:
					w2_positions[(x, curr_y)] = curr_steps - curr_x + x
			curr_x += steps
		elif val.startswith('L'):
			for y in range(curr_y, curr_y - steps, -1):
				if (curr_x, y) not in w2_positions:
					w2_positions[(curr_x, y)] = curr_steps + (curr_y - y)
			new_pos = [ ]
			curr_y -= steps
		elif val.startswith('R'):
			for y in range(curr_y, curr_y + steps):
				if (curr_x, y) not in w2_positions:
					w2_positions[(curr_x, y)] = curr_steps - curr_y + y
			curr_y += steps
		curr_steps += steps

	intersections = set(w1_positions.keys()).intersection(set(w2_positions.keys()))

	min_sd = 10**9
	for int_point in intersections:
		if int_point != (0, 0):
			signal_delay = w1_positions[int_point] + w2_positions[int_point]
			print(f'{int_point}: {signal_delay}')
			min_sd = min(min_sd, signal_delay)

	return min_sd

if __name__ == '__main__':
	solution = solve()
	print(f'Closest intersection point is at {solution} from central port.')