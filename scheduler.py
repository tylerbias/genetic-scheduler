import json
import random

class schedule():

	def __init__(self, employees, days, shifts):
		self.emps = {}
		for x in range(0, len(employees)):
			self.emps[employees[x]] = self.employee(7, 0)
		self.week = self.week(days, shifts)
		self.fitness = 500

	def get_emp_shifts(self, name):
		return self.emps[name].current

	def get_max(self, name):
		return self.emps[name].max_shifts

	def set_max(self, name, maximum):
		self.emps[name].max_shifts = maximum

	def get_min(self, name):
		return self.emps[name].min_shifts

	def set_min(self, name, minimum):
		self.emps[name].min_shifts = minimum

	def get_days(self):
		return self.week.days

	def get_shifts(self, day):
		return self.week.days[day]

	def get_shift_emp(self, day, shift):
		return self.week.days[day][shift]

	def get_fitness(self):
		return self.fitness






	class employee():

		def __init__(self, maximum, minimum):
			self.max_shifts = maximum
			self.min_shifts = minimum
			self.current = []

		def set_max(maximum):
			self.max_shifts = maximum

		def set_min(minimum):
			self.min_shifts = minimum

	class week():

		def __init__(self, days, shifts):
			self.days = {}
			for i in range(0, days):
				self.days[i] = self.gen_shifts(shifts)

		def gen_shifts(self, shifts):
			x = {}
			for i in range(0, shifts):
				x[("s%i" % (i+1))] = "NULL"
			return x

	def flaw(self, flaws):
		self.fitness -= (flaws * 25)

	def define_fitness(self):
		for name in self.emps:
			assigned = len(self.get_emp_shifts(name))
			if assigned > self.get_max(name):
				diff = assigned - self.get_max(name)
				self.flaw(diff)
			elif assigned < self.get_min(name):
				diff = self.get_min(name) - assigned
				self.flaw(diff)

			double_count = 0
			for day in self.get_days():
				counter = 0
				for shift in self.get_shifts(day):
					if self.get_shift_emp(day, shift) == name:
						counter += 1
				if counter > 1:
					double_count += (counter-1)
					self.flaw(double_count)





def random_schedule(employees, days, shifts):
	sched = schedule(employees, days, shifts)
	for x in sched.week.days:
		for y in sched.week.days[x]:
			randomName = random.choice(sched.emps.keys())
			sched.week.days[x][y] = randomName
			emp = sched.emps[randomName]
			emp.current.append((x, y))

	sched.define_fitness()

	return sched

emp = ["Tyler", "Isis"]


best = random_schedule(emp, 7, 2)
for i in range(0, 100):
	temp = random_schedule(emp, 7, 2)
	if temp.get_fitness() > best.get_fitness():
		best = temp

days = best.get_days()
for day in days:
	print day
	for shift in sorted(best.get_shifts(day)):
		print "%s belongs to %s" % (shift, best.get_shift_emp(day, shift))
print best.get_fitness()


















