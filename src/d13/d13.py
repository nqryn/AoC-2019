import itertools
from enum import Enum
from colorama import Fore, Back, Style
from time import sleep

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

class Tile(Enum):
	Empty = 0
	Wall = 1
	Block = 2
	Paddle = 3
	Ball = 4
	

COLORS = {
	Tile.Empty: lambda : print(' ', end=''),
	Tile.Wall: lambda : print(Fore.BLUE + 'X', end=''),
	Tile.Block: lambda : print(Back.BLUE + '□', end=''),
	Tile.Paddle: lambda : print(Fore.RED + '_', end=''),
	Tile.Ball: lambda : print(Fore.GREEN + 'O', end='')
}

def move_cursor(x,y):
    print ("\x1b[{};{}H".format(y+1,x+1))
 
def clear():
    print ("\x1b[2J")

def show_frame(game, score):
	move_cursor(0, 1)
	sleep(0.002)
	print(Fore.GREEN + f'Score: {str(score):10}' + Style.RESET_ALL)
	for row in game:
		for tile in row:
			print(' ', end='')
			COLORS[tile]()
			print(Style.RESET_ALL, end='')
			print(' ', end='')
		print()
		print()

def solve():
	with open('d13.in', 'r') as fin:
		intcode = [int(x) for x in fin.readline().split(',')]

	# Start the generator
	IC = IntcodeComputer(intcode)
	intcode_program = IC.run()
	game = [] # 37 x 26
	score = None
	for _ in range(26):
		game.append([0] * 37)

	ball, paddle = 0, 0
	send_value = None
	start_frames = False
	while True:
		try:
			x = intcode_program.send(send_value)
			if x == None:
				x = intcode_program.send(send_value)
			y = intcode_program.send(send_value)
			if x == -1 and y == 0:
				start_frames = True
				score = intcode_program.send(send_value)
			else:
				tile_id = intcode_program.send(send_value)
				game[y][x] = Tile(tile_id)
				if tile_id == Tile.Ball.value:
					ball = (y, x)
				elif tile_id == Tile.Paddle.value:
					paddle = (y, x)
			if start_frames:
				if ball[1] < paddle[1]:
					send_value = -1
				elif ball[1] > paddle[1]:
					send_value = 1
				else:
					send_value = 0
				# print(f'Ball at {ball} and paddle at {paddle}, sent {send_value}')
				show_frame(game, score)
		except StopIteration:
			break

if __name__ == '__main__':
	solve()
	
