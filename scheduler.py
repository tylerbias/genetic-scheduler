import json
import random

class scheduler():

	def __init__(self, employees, days, shifts):
		self.emps = employees
		self.week = self.week(days, shifts)
		self.fitness = 500

	def get_days(self):
		return self.week.days

	def get_shifts(self, day):
		return self.week.days[day]

	def get_shift_emp(self, day, shift):
		return self.week.days[day][shift]

	def get_fitness(self):
		return self.fitness


	class employee():

		def __init__(self, name, minimum, maximum):
			self.name = name
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
		for emp in self.emps:
			assigned = len(emp.current)
			if assigned > emp.max_shifts:
				diff = assigned - emp.max_shifts
				self.flaw(diff)
			elif assigned < emp.min_shifts:
				diff = emp.min_shifts - assigned
				self.flaw(diff)

			double_count = 0
			for day in self.get_days():
				counter = 0
				for shift in self.get_shifts(day):
					if self.get_shift_emp(day, shift) == emp.name:
						counter += 1
				if counter > 1:
					double_count += (counter-1)
					self.flaw(double_count)





def random_schedule(employees, days, shifts):
	sched = scheduler(employees, days, shifts)
	for day in sched.week.days:
		for shift in sched.week.days[day]:
			randomEmp = random.choice(sched.emps)
			sched.week.days[day][shift] = randomEmp.name
			randomEmp.current.append((day, shift))

	sched.define_fitness()

	return sched

# emps = []

# emps.append(scheduler.employee('Tyler', 0, 6))
# emps.append(scheduler.employee('Isis', 0, 6))


# best = random_schedule(emps, 7, 2)
# for i in range(0, 10000):
# 	temp = random_schedule(emps, 7, 2)
# 	if temp.get_fitness() > best.get_fitness():
# 		best = temp

# days = best.get_days()
# for day in days:
# 	print day
# 	for shift in sorted(best.get_shifts(day)):
# 		print "%s belongs to %s" % (shift, best.get_shift_emp(day, shift))
# print best.get_fitness()


















