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
				# print('Done!')
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
				# print(f'\t got ={in_value}: {chr(in_value)}=')
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

class Cell(Enum):
	NewLine = '\n'
	Space = '.'
	Scaffold = '#'
	RobotUp = '^'
	RobotRight = '>'
	RobotDown = 'v'
	RobotLeft = '<'


def get_intersection_align_param(cam_view, x, y, rows, cols):
	# Returns the aligment parameter for intersection at (x, y)
	# If the location is not an intersection, it returns -1
	for dx in [-1, 1]:
		nx = x + dx
		if 0 <= nx < rows and cam_view[nx][y] == Cell.Space:
			return -1
	for dy in [-1, 1]:
		ny = y + dy
		if 0 <= ny < cols and cam_view[x][ny] == Cell.Space:
			return -1
	return x * y



def solve_first():
	with open('d17.in', 'r') as fin:
		intcode = [int(x) for x in fin.readline().split(',')]

	# Start the generator
	IC = IntcodeComputer(intcode)
	intcode_program = IC.run()

	camera_view = []
	row = []
	while True:
		try:
			ascii_code = next(intcode_program)
			if ascii_code is None:
				break
			cell = Cell(chr(ascii_code))
			if cell == Cell.NewLine:
				if row:
					camera_view.append(row)
				row = []
			else:
				row.append(cell)
		except StopIteration:
			break

	rows, cols = len(camera_view), len(camera_view[0])
	align_params_sum = 0


	for i in range(rows):
		for j in range(cols):
			if camera_view[i][j] == Cell.Scaffold:
				# Check if intersection
				align_param = get_intersection_align_param(camera_view, i, j, rows, cols)
				if align_param != -1:
					align_params_sum += align_param
					print('O', end='')
				else:
					print(camera_view[i][j].value, end='')
			else:
				print(camera_view[i][j].value, end='')
		print()

	print(f' - What is the sum of the alignment parameters for the scaffold intersections?\n - {align_params_sum}')



def solve_second():

	commands = 'A,C,A,B,C,A,B,C,A,B\n'
	A = 'L,6,L,4,R,12\n'
	B = 'L,6,L,10,L,10,L,6\n'
	C = 'L,6,R,12,R,12,L,8\n'
	video_feed = 'n\n'

	with open('d17.in', 'r') as fin:
		intcode = [int(x) for x in fin.readline().split(',')]

	# Start the generator
	IC = IntcodeComputer(intcode)
	intcode_program = IC.run()

	cnt = 0
	prev_code = 0
	to_send = [commands, A, B, C, video_feed]
	idx = 0
	while True:
		try:
			ascii_code = next(intcode_program)
			print(chr(ascii_code), end='')
			
			if prev_code in [ord(':'), ord('?')] and ascii_code == 10:
				next(intcode_program)
				for char in to_send[idx]:
					# print(f'Sending ={ord(char)}: {char}=')
					res = intcode_program.send(ord(char))
					if res:
						print(chr(res), end='')
						if res > 255:
							print(f'Dust {res}')
				idx += 1
			prev_code = ascii_code
		except Exception as exc:
			print(exc)
			break

if __name__ == '__main__':
	solve_second()