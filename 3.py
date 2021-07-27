def field_to_string(field):
	field_string = ""

	for string in field:
		for cell in string:
			field_string = field_string + str(cell) + " "
		field_string = field_string + "\n"

	# print(field_string)
	return field_string

# def string_to_field(string):
# 	print(string)
# 	field = []
# 	sp_string = list(string.split("\n"))

# 	for string_ in sp_string:
# 		string_ = list(map(int, string_.split()))
# 		field.append(string_)

# 	return field

def first_letter(vvod):
	first = vvod
	
	while first >= 10:
		first //= 10

	return first

def any_to_ten(sys_base, chislo):
	desyat_chislo = 0
	mnojitel = 1

	for i in range(len(chislo) - 1, -1, -1):
		desyat_chislo += chislo[i] * mnojitel
		mnojitel *= sys_base

	return desyat_chislo

def ten_to_any(sys_base, desyat_chislo):
	new_chislo = []

	while desyat_chislo >= sys_base:
		new_chislo.append(desyat_chislo % sys_base)
		desyat_chislo //= sys_base

	new_chislo.append(desyat_chislo)
	new_chislo.reverse()

	# print(*new_chislo, end = "      ")
	return new_chislo

def next_num(sys_base, chislo):
	chislo[-1] += 1

	for i in range(len(chislo) - 1, 0, -1):
		if chislo[i] < sys_base:
			break
		else:
			chislo[i] = 0
			chislo[i - 1] += 1

	if chislo[0] == sys_base:
		chislo[0] = 1
		chislo.append(0)

	# print(*chislo, end = "      ")

	return chislo

# def get_stats(sys_base, ohvat):
# 	stats = list(list(0 for _ in range(sys_base)) for __ in range(sys_base))

# 	chislo = [0]

# 	for _ in range(ohvat):
# 		chislo = next_num(sys_base, chislo)

# 		desyat_chislo = any_to_ten(sys_base, chislo)
# 		desyat_chislo *= chislo[0]
# 		new_chislo = ten_to_any(sys_base, desyat_chislo)
		
# 		# print(chislo)
# 		# print(new_chislo)
# 		# print(stats)

# 		print(chislo[0], new_chislo[0])

# 		stats[chislo[0]][new_chislo[0]] += 1
# 	return stats

class Stats_table:
	def __init__(self, sys_base):
		self.sys_base = sys_base
		self.stats = list(list(0 for _ in range(sys_base)) for __ in range(sys_base))

	def add_range(self, begin, end):
		chislo = ten_to_any(self.sys_base, begin)

		for _ in range(begin, end):
			chislo = next_num(self.sys_base, chislo)

			desyat_chislo = any_to_ten(self.sys_base, chislo)
			desyat_chislo *= chislo[0]
			new_chislo = ten_to_any(self.sys_base, desyat_chislo)
			
			# print(chislo)
			# print(new_chislo)
			# print(stats)
			# print(chislo[0], new_chislo[0])

			self.stats[chislo[0]][new_chislo[0]] += 1


	# def add_nums(self, ranges):
	# 	for range_ in ranges:
	# 		self.add_num_range(range_[0], range_[1])

	def print(self):
		for num in range(self.sys_base):
			print(num, "    ", *self.stats[num])

	def print_cell(self, num, res):
		print(self.stats[num][res])

	def clear(self, sys_base):
		self.stats = list(list(0 for _ in range(sys_base)) for __ in range(sys_base))
		self.sys_base = sys_base

	def save(self, filename):
		with open(filename, 'w') as file:
			file.write(field_to_string(self.stats))

	def load(self, filename):
		self.stats = []

		with open(filename, 'r') as file:
			for line in file:
				self.stats.append(list(map(int, line.split())))

	def play(self):
		while True:
			comand = input()

			if comand == "add":
				begin = int(input())
				end = int(input())

				self.add_range(begin, end)

			elif comand == "print":
				self.print()

			elif comand == "print cell":
				num = int(input())
				res = int(input())
				self.print_cell(num, res)

			elif comand == "clear":
				sys_base = int(input())
				self.clear(sys_base)

			elif comand == "save":
				filename = input()
				self.save(filename)

			elif comand == "load":
				filename = input()
				self.load(filename)

			elif comand == "exit":
				break

def main():
	sys_base = int(input())

	if sys_base == 1:
		print("ne umeu")
		quit()

	table = Stats_table(sys_base)
	table.play()

if __name__ == '__main__':
	main()