import re

class Point3D:

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, other):
		return Point3D(
			self.x + other.x,
			self.y + other.y,
			self.z + other.z
		)

	def __str__(self):
		return f'<x={self.x:3}, y={self.y:3}, z={self.z:3}>'

class Moon:

	def __init__(self, name, init_pos):
		self.name = '🌑 ' + name + ' 🌑'
		self.position = Point3D(*init_pos)
		self.velocity = Point3D(0, 0, 0)

	def prepare_update(self, others):
		# Prepare to update the velocity based on the other moons
		self.update_x = 0
		self.update_y = 0
		self.update_z = 0

		coordinates = ['x', 'y', 'z']
		for m in others:
			for c in coordinates:
				if getattr(self.position, c) > getattr(m.position, c):
					setattr(self, 'update_' + c, getattr(self, 'update_' + c) - 1)
				elif getattr(self.position, c) < getattr(m.position, c):
					setattr(self, 'update_' + c, getattr(self, 'update_' + c) + 1)

	def step(self):
		# Update velocity, and then position
		self.velocity = self.velocity + Point3D(self.update_x, self.update_y, self.update_z)
		self.position = self.position + self.velocity

	def get_energy(self, energy_type):
		if energy_type == 'pot':
			return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)
		elif energy_type == 'kin':
			return abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)

	def __str__(self):
		return f'pos={self.position}, vel={self.velocity}'

def _debug_print(steps, moons):
	print(f'After {steps} steps:')
	for i, m in enumerate(moons):
		print(m)
	print()


def solve():

	names = ['Io', 'Europa', 'Ganymede', 'Callisto']
	moons = []
	regex = r'^<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>$'

	with open('sample.in', 'r') as fin:
		for name in names:
			line = fin.readline()
			matches = re.search(regex, line)
			position = (int(matches.group('x')), int(matches.group('y')), int(matches.group('z')))
			moons.append(Moon(name, position))

	_debug_print(0, moons)
	for _ in range(4686774924):
		for i, m in enumerate(moons):
			m.prepare_update(moons[:i] + moons[i+1:])

		for m in moons:
			m.step()

	_debug_print(4686774924, moons)

	# # Compute the energy
	# energy = 0
	# for m in moons:
	# 	pot = m.get_energy('pot')
	# 	kin = m.get_energy('kin')
	# 	energy += pot * kin

	# print(f'Total energy {energy}')

if __name__ == '__main__':
	solve()