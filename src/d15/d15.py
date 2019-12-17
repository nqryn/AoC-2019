import itertools
import random
from colorama import Fore, Back, Style
from time import sleep
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
		
class MovementCmd(Enum):
	North = 1
	South = 2
	West = 3
	East = 4


class Status(Enum):
	Unknown = -1
	Wall = 0
	Step = 1
	OxygenSys = 2

def move_cursor(x,y):
    print ("\x1b[{};{}H".format(y+1,x+1))

def _print_grid(grid):
	move_cursor(0, 0)
	sleep(0.1)
	for row in grid:
		for cell in row:
			if cell == Status.Unknown:
				print(' ', end='')
			elif cell == Status.Wall:
				print('#', end='')
			elif cell == Status.Step:
				print('.', end='')
			elif cell == Status.OxygenSys:
				print('O', end='')
		print()

def get_left(move):
	lefts = {
		MovementCmd.North: MovementCmd.West,
		MovementCmd.West: MovementCmd.South,
		MovementCmd.South: MovementCmd.East,
		MovementCmd.East: MovementCmd.North
	}
	return lefts[move]

	
def solve():
	with open('d15.in', 'r') as fin:
		intcode = [int(x) for x in fin.readline().split(',')]

	# Start the generator
	IC = IntcodeComputer(intcode)
	intcode_program = IC.run()
	intcode_program.send(None)

	# Init grid with size 100
	grid = []
	for _ in range(100):
		grid.append([Status.Unknown] * 100)
	curr_x, curr_y = 50, 50

	# Define movement
	move = {
		MovementCmd.North: lambda x, y: (x, y + 1),
		MovementCmd.South: lambda x, y: (x, y - 1),
		MovementCmd.West: lambda x, y: (x - 1, y),
		MovementCmd.East: lambda x, y: (x + 1, y)
	}
	next_move = MovementCmd.North

	score = 0
	min_x = min_y = 1000
	max_x = max_y = 0
	while True:
		# Send a movement command
		next_x, next_y = move[next_move](curr_x, curr_y)
		while grid[next_x][next_y] == Status.Wall:
			next_move = get_left(next_move)
			next_x, next_y = move[next_move](curr_x, curr_y)
		
		# if next_x < 0 or next_x > 999 or next_y < 0 or next_y > 999:
		# 	import pdb; pdb.set_trace()
		status = Status(intcode_program.send(next_move.value))
		next(intcode_program)
		if status == Status.OxygenSys:
			# min_x = min(500, next_x)
			# max_x = max(500, next_x)
			# min_y = min(500, next_y)
			# max_y = max(500, next_y)
			# _print_grid(grid, min_x, max_x, min_y, max_y)
			print(f'Found it at {next_x, next_y}')
			print(f'Score {score}')
			print(f'Min moves = {abs(next_x - 500) + abs(next_y - 500)}')
			return

		# min_x = min(min_x, next_x)
		# min_y = min(min_y, next_y)
		# max_x = max(max_x, next_x)
		# max_y = max(max_y, next_y)
		# if grid[next_x][next_y] != Status.Unknown and grid[next_x][next_y] != status:
		# 	import pdb; pdb.set_trace()

		grid[next_x][next_y] = status
		if status == Status.Step:
			curr_x, curr_y = next_x, next_y
		# score += 1
		# if score > 100:
		_print_grid(grid)


if __name__ == '__main__':
	solve()
	
