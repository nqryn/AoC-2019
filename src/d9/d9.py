import itertools

class IntcodeComputer:

	def __init__(self, intcode):
		self.intcode = intcode

	def run(self, in_value):
		relative_base = 0
		idx = 0
		mem_limit = len(self.intcode)

		while True:
			instr = int(self.intcode[idx])
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
				lambda:self.intcode[idx+1],	# mode 0: position mode
				lambda:idx+1, # mode 1: value mode -- should never happen
				lambda:self.intcode[idx+1] + relative_base, # mode 2: relative mode (relative address)
			][mode_param1]()

			if mem_address1 >= mem_limit:
				self.intcode.extend([0] * (mem_address1 - mem_limit + 1))
				mem_limit = mem_address1 + 1
			param1 = self.intcode[mem_address1]

			if opcode not in [3, 4, 9]:
				# 3 (PUT), 4 (GET) and 9 (ADJ) only have one param
				mem_address2 = [
					lambda:self.intcode[idx+2],	# mode 0: position mode
					lambda:idx+2, # mode 1: value mode -- should never happen
					lambda:self.intcode[idx+2] + relative_base, # mode 2: relative mode (relative address)
				][mode_param2]()

				if mem_address2 >= mem_limit:
					self.intcode.extend([0] * (mem_address2 - mem_limit + 1))
					mem_limit = mem_address2 + 1
				param2 = self.intcode[mem_address2]

			if opcode in [1, 2, 7, 8]:
				# 1 (ADD), 2 (MUL), 7 (<) and 8 (=) write to memory => compute the address
				mem_address = [
					lambda:self.intcode[idx+3],	# mode 0: position mode
					lambda:idx+3, # mode 1: value mode -- should never happen
					lambda:self.intcode[idx+3] + relative_base, # mode 2: relative mode (relative address)
				][mode_param3]()
				if mem_address >= mem_limit:
					self.intcode.extend([0] * (mem_address - mem_limit + 1))
					mem_limit = mem_address + 1
			if opcode == 99:
				print('Done!')
				return
			elif opcode == 1:
				# ADD
				self.intcode[mem_address] = param1 + param2
				idx += 4
			elif opcode == 2:
				# MUL
				self.intcode[mem_address] = param1 * param2
				idx += 4
			elif opcode == 3:
				# PUT
				self.intcode[mem_address1] = in_value
				idx += 2
			elif opcode == 4:
				# GET
				print(self.intcode[idx:idx+2])
				print(f'GET {param1}')
				idx += 2
			elif opcode == 5:
				# JUMP IF TRUE
				if param1 != 0:
					idx = param2
				else:
					idx += 3
			elif opcode == 6:
				# JUMP IF FALSE
				if param1 == 0:
					idx = param2
				else:
					idx += 3
			elif opcode == 7:
				# LESS THAN
				self.intcode[mem_address] = 1 if (param1 < param2) else 0
				idx += 4
			elif opcode == 8:
				# EQUALS
				self.intcode[mem_address] = 1 if (param1 == param2) else 0
				idx += 4
			elif opcode == 9:
				# adjusts the relative base
				relative_base += param1
				idx += 2
		
	
def solve():
	with open('d9.in', 'r') as fin:
		intcode = [int(x) for x in fin.readline().split(',')]

	IC = IntcodeComputer(intcode)
	IC.run(2)


if __name__ == '__main__':
	solve()
