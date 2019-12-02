
def program_assist(intcode):
	i = 0
	while True:
		opcode = intcode[i]
		if opcode == 99:
			return intcode[0]
		elif opcode == 1:
			intcode[intcode[i+3]] = intcode[intcode[i+1]] + intcode[intcode[i+2]]
		elif opcode == 2:
			intcode[intcode[i+3]] = intcode[intcode[i+1]] * intcode[intcode[i+2]]
		i += 4

def solve():
	expected = 19690720
	with open('d2.in', 'r') as fin:
		intcode = [int(x) for x in fin.readline().split(',')]
		for i in range(100):
			intcode[1] = i
			for j in range(100):
				intcode[2] = j
				# Force a copy of the list to be sent, so that we don't modify it
				if program_assist(intcode[:]) == expected:
					print(i * 100 + j)
					return

if __name__ == '__main__':
	solve()
