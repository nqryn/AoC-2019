def _get_orbits():

	return orbit, is_orbited

def solve_first():
	orbits = {
		'COM': set(),
	}
	is_orbited = {
		'COM': set(),	
	}
	with open('d6.in', 'r') as fin:
		for line in fin:
			line = line.strip()
			obj1, obj2 = line.split(')')
			if obj2 not in orbits:
				orbits[obj2] = set()
			orbits[obj2].add(obj1)
			if obj1 not in is_orbited:
				is_orbited[obj1] = set()
			is_orbited[obj1].add(obj2)

	next_obj = ['COM']
	while len(next_obj) > 0:
		no = next_obj.pop(0)
		if no in is_orbited:
			for orbiter in is_orbited[no]:
				orbits[orbiter] |= orbits[no]
				next_obj.append(orbiter)

	total = 0
	for obj in orbits:
		total += len(orbits[obj])

	print(f'Orbit count checksum is {total}')

def solve_second():
	neighbours = {
		'COM': set()
	}

	with open('d6.in', 'r') as fin:
		for line in fin:
			line = line.strip()
			obj1, obj2 = line.split(')')
			if obj2 not in neighbours:
				neighbours[obj2] = set()
			neighbours[obj2].add(obj1)
			if obj1 not in neighbours:
				neighbours[obj1] = set()
			neighbours[obj1].add(obj2)

	next_obj = [('YOU', 0)]
	distance = 0
	visited = []
	while len(next_obj) > 0:
		(no, distance) = next_obj.pop(0)
		visited.append(no)
		for neigh in neighbours[no]:
			if no == 'SAN':
				print(f'Distance from YOU to SAN is {distance - 2}')
				return
			if neigh not in visited:
				next_obj.append((neigh, distance + 1))


if __name__ == '__main__':
	# solve_first()
	solve_second()
