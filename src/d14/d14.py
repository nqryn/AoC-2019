import re

def get_required_ore(fuel_quant, reactions):
	required = [(k, v * fuel_quant) for (k, v) in reactions['FUEL']['takes'].items()]
	ore_required = 0
	have_extra = {}
	while len(required) > 0:
		compound, quantity = required.pop(0)
		if compound == 'ORE':
			ore_required += quantity
			continue
		if compound in have_extra:
			if have_extra[compound] > quantity:
				have_extra[compound] -= quantity
				continue
			else:
				quantity -= have_extra[compound]
				del have_extra[compound]
		base_quantity = reactions[compound]['makes']
		if quantity % base_quantity == 0:
			# Perfect quantity
			batches = quantity // base_quantity
		else:
			# We need to make more, and we'll have some extra
			batches = quantity // base_quantity + 1
			have_extra[compound] = base_quantity * batches - quantity
		# see what's needed next
		new_required = [(k, v * batches) for k, v in reactions[compound]['takes'].items()]
		required.extend(new_required)
	return ore_required

def main():
	reactions = {}
	pattern = re.compile(r'(?P<quantity>\d+) (?P<compound>\w+)')

	with open('d14.in', 'r') as fin:
		for line in fin:
			in_chem, out_chem = line.split(' => ')
			out_quantity, out_compound = out_chem.split()

			ingredients = {}
			for match in pattern.findall(in_chem):
				ingredients[match[1]] = int(match[0])

			reactions[out_compound] = {
				'makes': int(out_quantity),
				'takes': ingredients
			}

	# Solution part 1: min amount of ORE for 1 FUEL
	ore_per_fuel = get_required_ore(1, reactions)
	print(f'The minimum amount of ORE required to produce 1 FUEL is {ore_per_fuel}')

	# Solution part 2: max amount of FUEL for 1 trilion ORE
	ore_quantity = 10**12
	max_fuel = ore_quantity // ore_per_fuel
	required_ore = get_required_ore(max_fuel, reactions)

	while required_ore <= ore_quantity:
		max_fuel += max((ore_quantity - required_ore) // ore_per_fuel, 1)
		required_ore = get_required_ore(max_fuel, reactions)

	print(f'The maximum amount of FUEL we can produce with 1 trilion ORE is {max_fuel - 1}')

if __name__ == '__main__':
	main()