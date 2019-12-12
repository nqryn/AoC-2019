import itertools
from enum import Enum

class IntcodeComputer:

	def __init__(self, intcode):
		self.intcode = intcode
		self.relative_base = 0
		self.idx = 0
		self.mem_limit = len(self.intcode)

	def run(self):
		while True:
			instr = int(self.intcode[self.idx])
			# Gett opcode and modes for params
			opcode = instr % 100
			instr //= 100
			mode_param1 = instr % 10
			instr //= 10
			mode_param2 = instr % 10
			instr //= 10
			mode_param3 = instr % 10

			# get actual params based on their modes and how many are needed
			mem_address1 = [
				lambda:self.intcode[self.idx+1],	# mode 0: position mode
				lambda:self.idx+1, # mode 1: value mode -- should never happen
				lambda:self.intcode[self.idx+1] + self.relative_base, # mode 2: relative mode (relative address)
			][mode_param1]()

			if mem_address1 >= self.mem_limit:
				self.intcode.extend([0] * (mem_address1 - self.mem_limit + 1))
				self.mem_limit = mem_address1 + 1
			param1 = self.intcode[mem_address1]

			if opcode not in [3, 4, 9]:
				# 3 (PUT), 4 (GET) and 9 (ADJ) only have one param
				mem_address2 = [
					lambda:self.intcode[self.idx+2],	# mode 0: position mode
					lambda:self.idx+2, # mode 1: value mode -- should never happen
					lambda:self.intcode[self.idx+2] + self.relative_base, # mode 2: relative mode (relative address)
				][mode_param2]()

				if mem_address2 >= self.mem_limit:
					self.intcode.extend([0] * (mem_address2 - self.mem_limit + 1))
					self.mem_limit = mem_address2 + 1
				param2 = self.intcode[mem_address2]

			if opcode in [1, 2, 7, 8]:
				# 1 (ADD), 2 (MUL), 7 (<) and 8 (=) write to memory => compute the address
				mem_address = [
					lambda:self.intcode[self.idx+3],	# mode 0: position mode
					lambda:self.idx+3, # mode 1: value mode -- should never happen
					lambda:self.intcode[self.idx+3] + self.relative_base, # mode 2: relative mode (relative address)
				][mode_param3]()
				if mem_address >= self.mem_limit:
					self.intcode.extend([0] * (mem_address - self.mem_limit + 1))
					self.mem_limit = mem_address + 1
			if opcode == 99:
				print('Done!')
				return
			elif opcode == 1:
				# ADD
				self.intcode[mem_address] = param1 + param2
				self.idx += 4
			elif opcode == 2:
				# MUL
				self.intcode[mem_address] = param1 * param2
				self.idx += 4
			elif opcode == 3:
				# PUT
				in_value = yield
				self.intcode[mem_address1] = in_value
				self.idx += 2
			elif opcode == 4:
				# GET
				yield param1
				self.idx += 2
			elif opcode == 5:
				# JUMP IF TRUE
				if param1 != 0:
					self.idx = param2
				else:
					self.idx += 3
			elif opcode == 6:
				# JUMP IF FALSE
				if param1 == 0:
					self.idx = param2
				else:
					self.idx += 3
			elif opcode == 7:
				# LESS THAN
				self.intcode[mem_address] = 1 if (param1 < param2) else 0
				self.idx += 4
			elif opcode == 8:
				# EQUALS
				self.intcode[mem_address] = 1 if (param1 == param2) else 0
				self.idx += 4
			elif opcode == 9:
				# adjusts the relative base
				self.relative_base += param1
				self.idx += 2
		
class Direction(Enum):
	Up = 0
	Right = 1
	Down = 2
	Left = 3

class Color(Enum):
	Black = 0
	White = 1

class Turn(Enum):
	Left = 0
	Right = 1
	
def solve():
	with open('d11.in', 'r') as fin:
		intcode = [int(x) for x in fin.readline().split(',')]

	# Start the generator
	IC = IntcodeComputer(intcode)
	intcode_program = IC.run()
	intcode_program.send(None)

	# Start on a single white panel
	curr_color = Color.White
	curr_direction = Direction.Up
	curr_location = (0, 0)
	panels = {}
	while True:
		try:
			paint = intcode_program.send(curr_color.value)
			turn = next(intcode_program)
			next(intcode_program)
		except StopIteration:
			break
		# Paint current panel with the result
		panels[curr_location] = Color(paint)
		# Turn in place
		if turn == Turn.Left.value:
			curr_direction = Direction((curr_direction.value - 1) % 4)
		elif turn == Turn.Right.value:
			curr_direction = Direction((curr_direction.value + 1) % 4)
		# Move to the next panel
		if curr_direction == Direction.Up:
			curr_location = (curr_location[0] + 1, curr_location[1])
		elif curr_direction == Direction.Down:
			curr_location = (curr_location[0] - 1, curr_location[1])
		elif curr_direction == Direction.Right:
			curr_location = (curr_location[0], curr_location[1] + 1)
		elif curr_direction == Direction.Left:
			curr_location = (curr_location[0], curr_location[1] - 1)

		# Get the color of the new panel
		if curr_location in panels:
			curr_color = panels[curr_location]
		else:
			curr_color = Color.Black

	print(f' - How many panels does it paint at least once?\n - {len(panels)}') 

	# Print out the registration identifier
	x_min, x_max, y_min, y_max = 1000, 0, 1000, 0
	for p in panels:
		if p[0] > x_max:
			x_max = p[0]
		elif p[0] < x_min:
			x_min = p[0]

		if p[1] > y_max:
			y_max = p[1]
		elif p[1] < y_min:
			y_min = p[1]

	# Print registration number
	for x in range(x_max, x_min - 1, -1):
		for y in range(y_min, y_max + 1):
			if (x, y) in panels:
				if panels[(x, y)] == Color.White:
					print(1, end='')
				else:
					print(' ', end='')
			else:
				print(' ', end='')
		print()


if __name__ == '__main__':
	panels_painted = solve()
	
