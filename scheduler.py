import json
import random
import copy
from operator import itemgetter

## TO DO: Just wrote day class. Need to follow code, rework any function dependent on day / week (honestly, most of it)


DAY_LIST = ['Sunday',
			'Monday',
			'Tuesday',
			'Wednesday',
			'Thursday',
			'Friday',
			'Saturday']

# Object instance. Set as default parameter in some functions. Function checks to see if it has been handed DEFAULT, and reacts accordingly.
DEFAULT = object()

class scheduler():

	def __init__(self, employees, week):
		self.emps = employees
		self.week = week
		self.fitness = 500
		self.shifts = {}

	def get_fitness(self):
		return self.fitness

	def get_week(self):
		return self.week


	class employee():

		def __init__(self, name, minimum, maximum):
			self.name = name
			self.max_shifts = maximum
			self.min_shifts = minimum
			# Current shifts. Dictionary indexed by day of the week, containing start and end times as tuple
			self.current = {}

		def set_max(maximum):
			self.max_shifts = maximum

		def set_min(minimum):
			self.min_shifts = minimum


	class day():

		# opening and closing are integers, truncated military time
		# requirements is a dictionary, indexed by hour in truncated military time (int), and storing an int
		# that specifies the user's requirements for coverage for the hour in question
		# Coverage is updated as an employee is given a shift that cross that hour. Incremented by one.
		def __init__(self, opening, closing, requirements = DEFAULT):
			self.hours = []
			self.coverage = []
			self.opening = opening
			self.closing = closing
			for hr in range(0, 24):
				if hr >= opening and hr <= closing:
					self.hours.append(1) #Initialize all hours when the store is open as a minimum of 1
				else:
					self.hours.append(0) #Initialize all hours as no minimum employee

			# Once minimum coverage requirements are established, assign user specified coverage requirements
			if requirements is not DEFAULT:
				for key in requirements:
					self.hours[key] = requirements[key]

			for hr in range(0, 24):
				self.coverage.append(0)




	# class week():

	# 	# Days are stored in a dictionary indexed by the name of the day of the week.
	# 	# Each day has 
	# 	def __init__(self, days, shifts):
	# 		self.days = {}
	# 		for day in shifts:
	# 			self.days[day] = self.gen_shifts(shifts)

	# 	def gen_shifts(self, shifts):
	# 		x = {}
	# 		for i in range(0, shifts):
	# 			x[("s%i" % (i+1))] = "NULL"
	# 		return x

	def flaw(self, flaws):
		self.fitness -= (flaws * 25)

	def define_fitness(self):
		for emp in self.emps:
			goal = ((7*11)/3)
			total = 0
			for shift in emp.current:
				shiftLength = emp.current[shift]['end'] - emp.current[shift]['start']
				total += shiftLength

			difference = total - goal
			if difference < 0:
				difference = 0
			self.flaw(difference)

	def define_shifts(self):
		shiftDict = {}
		for day in DAY_LIST:
			shiftDict.update({day: {}})
		for day in DAY_LIST:
			for emp in self.emps:
				for key in emp.current:
					if key is day:
						shiftDict[day].update({emp.name: ("%s to %s" % (emp.current[day]['start'], emp.current[day]['end']))})

		self.shifts = shiftDict








def random_schedule(employees, week):
	sched = scheduler(employees, week)

	for day in DAY_LIST:
		availableEmps = list(sched.emps)
		for hr in range(0, 24):
			if sched.week[day].hours[hr] is not 0:
				while sched.week[day].coverage[hr] < sched.week[day].hours[hr]:
					if len(availableEmps) is 0:
						break
					chosenEmp = random.choice(availableEmps)
					availableEmps.remove(chosenEmp)
					shiftEnd = hr + random.randint(4, 7)
					if shiftEnd >= (sched.week[day].closing-3):
						shiftEnd = sched.week[day].closing
					chosenEmp.current[day] = {'start': hr, 'end': shiftEnd}
					for x in range(hr, shiftEnd+1):
						sched.week[day].coverage[x] += 1

	sched.define_shifts()
	sched.define_fitness()

	return sched

## The code below is used for isolated testing of scheduler functions.

emps = []

emps.append(scheduler.employee('Tyler', 0, 6))
emps.append(scheduler.employee('Isis', 0, 6))
emps.append(scheduler.employee('Dana', 0, 6))

week = {}
for dayName in DAY_LIST:
	week[dayName] = scheduler.day(10, 21)


originalCopyEmps = copy.deepcopy(emps)
originalCopyWeek = copy.deepcopy(week)
best = random_schedule(originalCopyEmps, originalCopyWeek)

for i in range(0, 100):
	newCopyEmps = copy.deepcopy(emps)
	newCopyWeek = copy.deepcopy(week)
	temp = random_schedule(newCopyEmps, newCopyWeek)
	if temp.get_fitness() > best.get_fitness():
		best = temp


for day in best.shifts:
	print day
	for shift in sorted(best.shifts[day].iteritems(), key=itemgetter(1)):
		print shift
print best.get_fitness()


















