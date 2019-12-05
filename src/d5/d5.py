
def solve(ID):
	with open('d5.in', 'r') as fin:
		intcode = [int(x) for x in fin.readline().split(',')]
		i = 0
		while True:
			instr = int(intcode[i])
			# Gett opcode and modes for params
			opcode = instr % 100
			instr //= 100
			mode1 = instr % 10
			instr //= 10
			mode2 = instr % 10

			if opcode == 99:
				print('Done')
				return
			elif opcode == 1:
				# ADD
				param1 = intcode[i+1] if mode1 else intcode[intcode[i+1]] 
				param2 = intcode[i+2] if mode2 else intcode[intcode[i+2]] 
				intcode[intcode[i+3]] = param1 + param2
				i += 4
			elif opcode == 2:
				# MULT
				param1 = intcode[i+1] if mode1 else intcode[intcode[i+1]] 
				param2 = intcode[i+2] if mode2 else intcode[intcode[i+2]] 
				intcode[intcode[i+3]] = param1 * param2
				i += 4
			elif opcode == 3:
				# PUT
				intcode[intcode[i+1]] = ID
				i += 2
			elif opcode == 4:
				# GET
				param1 = intcode[i+1] if mode1 else intcode[intcode[i+1]] 
				print(param1)
				i += 2
			elif opcode == 5:
				# JUMP IF TRUE
				param1 = intcode[i+1] if mode1 else intcode[intcode[i+1]] 
				param2 = intcode[i+2] if mode2 else intcode[intcode[i+2]] 
				if param1 != 0:
					i = param2
				else:
					i += 3
			elif opcode == 6:
				# JUMP IF FALSE
				param1 = intcode[i+1] if mode1 else intcode[intcode[i+1]] 
				param2 = intcode[i+2] if mode2 else intcode[intcode[i+2]] 
				if param1 == 0:
					i = param2
				else:
					i += 3
			elif opcode == 7:
				# LESS THAN
				param1 = intcode[i+1] if mode1 else intcode[intcode[i+1]] 
				param2 = intcode[i+2] if mode2 else intcode[intcode[i+2]] 
				intcode[intcode[i+3]] = 1 if (param1 < param2) else 0
				i += 4
			elif opcode == 8:
				# EQUALS
				param1 = intcode[i+1] if mode1 else intcode[intcode[i+1]] 
				param2 = intcode[i+2] if mode2 else intcode[intcode[i+2]] 
				intcode[intcode[i+3]] = 1 if (param1 == param2) else 0
				i += 4
			


if __name__ == '__main__':
	solve(5)
