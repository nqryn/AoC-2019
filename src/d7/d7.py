import itertools

class Amplifier:

	def __init__(self, phase_setting, intcode):
		self.inputs = [phase_setting]
		self.idx_inp = 0
		self.intcode = intcode
		self.idx = 0

	def input_signal(self, in_sign):
		self.inputs.append(in_sign)


	def run(self):
		while True:
			instr = int(self.intcode[self.idx])
			# Gett opcode and modes for params
			opcode = instr % 100
			instr //= 100
			mode1 = instr % 10
			instr //= 10
			mode2 = instr % 10

			if opcode == 99:
				return
			elif opcode == 1:
				# ADD
				param1 = self.intcode[self.idx+1] if mode1 else self.intcode[self.intcode[self.idx+1]] 
				param2 = self.intcode[self.idx+2] if mode2 else self.intcode[self.intcode[self.idx+2]] 
				self.intcode[self.intcode[self.idx+3]] = param1 + param2
				self.idx += 4
			elif opcode == 2:
				# MULT
				param1 = self.intcode[self.idx+1] if mode1 else self.intcode[self.intcode[self.idx+1]] 
				param2 = self.intcode[self.idx+2] if mode2 else self.intcode[self.intcode[self.idx+2]] 
				self.intcode[self.intcode[self.idx+3]] = param1 * param2
				self.idx += 4
			elif opcode == 3:
				# PUT
				self.intcode[self.intcode[self.idx+1]] = self.inputs[self.idx_inp]
				self.idx_inp += 1
				self.idx += 2
			elif opcode == 4:
				# GET
				param1 = self.intcode[self.idx+1] if mode1 else self.intcode[self.intcode[self.idx+1]] 
				output_signal = param1
				self.idx += 2
				return output_signal
			elif opcode == 5:
				# JUMP IF TRUE
				param1 = self.intcode[self.idx+1] if mode1 else self.intcode[self.intcode[self.idx+1]] 
				param2 = self.intcode[self.idx+2] if mode2 else self.intcode[self.intcode[self.idx+2]] 
				if param1 != 0:
					self.idx = param2
				else:
					self.idx += 3
			elif opcode == 6:
				# JUMP IF FALSE
				param1 = self.intcode[self.idx+1] if mode1 else self.intcode[self.intcode[self.idx+1]] 
				param2 = self.intcode[self.idx+2] if mode2 else self.intcode[self.intcode[self.idx+2]] 
				if param1 == 0:
					self.idx = param2
				else:
					self.idx += 3
			elif opcode == 7:
				# LESS THAN
				param1 = self.intcode[self.idx+1] if mode1 else self.intcode[self.intcode[self.idx+1]] 
				param2 = self.intcode[self.idx+2] if mode2 else self.intcode[self.intcode[self.idx+2]] 
				self.intcode[self.intcode[self.idx+3]] = 1 if (param1 < param2) else 0
				self.idx += 4
			elif opcode == 8:
				# EQUALS
				param1 = self.intcode[self.idx+1] if mode1 else self.intcode[self.intcode[self.idx+1]] 
				param2 = self.intcode[self.idx+2] if mode2 else self.intcode[self.intcode[self.idx+2]] 
				self.intcode[self.intcode[self.idx+3]] = 1 if (param1 == param2) else 0
				self.idx += 4
		
	
def solve():
	with open('d7.in', 'r') as fin:
		intcode = [int(x) for x in fin.readline().split(',')]

	max_thruster_signal = 0
	perms = list(itertools.permutations([5, 6, 7, 8, 9]))		

	for perm in perms:
		signal = 0
		A = Amplifier(perm[0], intcode)
		B = Amplifier(perm[1], intcode)
		C = Amplifier(perm[2], intcode)
		D = Amplifier(perm[3], intcode)
		E = Amplifier(perm[4], intcode)

		amplifiers = [A, B, C, D, E]
		current_amp = 0
		while True:
			amplifiers[current_amp].input_signal(signal)
			output = amplifiers[current_amp].run()
			if not output:
				# Amplifier has halted
				break
			signal = output
			current_amp = (current_amp + 1) % 5

		max_thruster_signal = max(max_thruster_signal, signal)

	return max_thruster_signal


if __name__ == '__main__':
	solution = solve()
	print(f'The highest signal that can be sent to the thrusters is {solution}')
	
