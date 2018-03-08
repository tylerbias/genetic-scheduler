import json
import random
import copy
from operator import itemgetter

# TO DO: Many more 'flaws' need to be defined and implemented. Additionally, need to have an ability to restrict availability beyond just a cap on hours.
# An employee must be able to have days for which they cannot be scheduled. Additionally, it must be possible to restrict the times during a particular day
# within which an employee can possibly be assigned a shift. Violating availability constraints would be a major blow to fitness, while some, like slightly
# underscheduling an employee or overscheduling, can be minimal. Also I want to implement the idea that closing one night and opening the next morning is
# suboptimal, and should be avoided if possible, but again, this is a flaw that will have to be treated as very minor, because we want it to still be able
# to rise to the top if the best available solution does need to resort to it.
# It may also be beneficial to assign special weight to certain employees if they are better in a particular role. For instance, if an employee is a particularly
# good closer, then a schedule's fitness evaluation may be raised slightly if that employee is given closing shifts.

DAY_LIST = ['Sunday',
			'Monday',
			'Tuesday',
			'Wednesday',
			'Thursday',
			'Friday',
			'Saturday']

INITIAL_FITNESS = 500

# Object instance. Set as default parameter in some functions. Function checks to see if it has been handed DEFAULT, and reacts accordingly.
DEFAULT = object()

class scheduler():

	def __init__(self, employees, week):
		# An array of employee objects
		self.emps = employees
		# A dictionary of day objects, indexed by day names
		self.week = week
		# An initial fitness value, defined globally
		self.fitness = INITIAL_FITNESS
		# Eventually holds a nested dictionary. First index is day of the week, second is name, which then returns a human readable shift string e.g. '5 to 10'
		self.shifts = {}
		# Stores human readable list of rule violations, used to explain fitness score given to a schedule
		self.violations = []

	def get_fitness(self):
		return self.fitness

	def get_week(self):
		return self.week


	# The employee class governs one of two primary object types that make up a schedule (employees and days).
	# The class contains specific constraints (min and max) that are used to evaluate a schedules fitness.class
	# When a schedule is generated, each shift given to an employee is also stored in employee.current, allowing one
	# to easily isolate a specific employees shifts.
	class employee():

		def __init__(self, name, minimum, maximum):
			self.name = name
			self.maxHours = maximum
			self.minHours = minimum
			# Current shifts. Dictionary indexed by day of the week, containing dictionary indexed by name, containing human readable shift string
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

	# Currently all flaws are treated equally. TODO: create multiple functions, some with low weight, some with high weight
	def flaw(self, flaws):
		self.fitness -= (flaws * 25)

	# Currently invokes only one type of flaw. Passes violations over to flaw function, in order to effect change in fitness value.
	# Also logs the violations that it picks up in the violations attribute of the scheduler object
	def define_fitness(self):
		for emp in self.emps:
			total = 0
			for shift in emp.current:
				shiftLength = emp.current[shift]['end'] - emp.current[shift]['start']
				total += shiftLength

			if total < emp.minHours:
				difference = emp.minHours - total
				self.flaw(difference)
				self.violations.append("%s is under by %i hour(s)" % (emp.name, difference))
			if total > emp.maxHours:
				difference = total - emp.maxHours
				self.flaw(difference)
				self.violations.append("%s is over by %i hour(s)" % (emp.name, difference))

	# Looks at each employee object, after shifts have been assigned, and consolidates all of the shift information into a shift master list
	# Stores data as strings for easy human readability.
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



# Produces a random schedule based on the employees and the week that are passed to it.
# Used to generate the first generation of schedules and to produce the occasional fully random new entry to a subsequent population.
def random_schedule(employees, week):
	sched = scheduler(employees, week)

	for day in DAY_LIST:
		# A copy of the list of all available employees is used to a assign shifts. An employee can only be given one shift per day,
		# so after an employee has been given a shift for any particular day, they are removed from the list and cannot be assigned another.
		availableEmps = list(sched.emps)
		for hr in range(0, 24):
			if sched.week[day].hours[hr] is not 0:
				while sched.week[day].coverage[hr] < sched.week[day].hours[hr]:
					# The schedule will not leave any hours of operation with zero coverage unless it has run out of employees to handle the requested coverage
					if len(availableEmps) is 0:
						break
					chosenEmp = random.choice(availableEmps)
					availableEmps.remove(chosenEmp)
					shiftEnd = hr + random.randint(4, 7)
					if shiftEnd >= (sched.week[day].closing-3):
						shiftEnd = sched.week[day].closing
					# When generated, shift is only stored in employee object. define_shifts() is later called to establish a master list
					chosenEmp.current[day] = {'start': hr, 'end': shiftEnd}
					for x in range(hr, shiftEnd+1):
						sched.week[day].coverage[x] += 1

	sched.define_shifts()
	sched.define_fitness()

	return sched

## The code below is used for isolated testing of scheduler functions.

emps = []

emps.append(scheduler.employee('Tyler', 0, 24))
emps.append(scheduler.employee('Isis', 0, 20))
emps.append(scheduler.employee('Dana', 0, 40))
emps.append(scheduler.employee('Blalock', 32, 40))
emps.append(scheduler.employee('Mike', 32, 40))


week = {}
requirements = {10: 2, 13: 3, 15: 3, 18: 2, 19: 2, 20: 2, 21: 2}
for dayName in DAY_LIST:
	week[dayName] = scheduler.day(10, 21, requirements)


originalCopyEmps = copy.deepcopy(emps)
originalCopyWeek = copy.deepcopy(week)
best = random_schedule(originalCopyEmps, originalCopyWeek)

for i in range(0, 50000):
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
print best.violations


















