import random
import math
import sys

min_range = 0
max_range = 100

def go(target, minimum, maximum, verbose):
	if minimum < 0:
		return "Minimum cannot be less than 0."
	if maximum > 1000:
		return "Maximum cannot be greater than 1000."
	if minimum >= maximum:
		return "Minimum must be less than the maximum."
	range_mean = (minimum+maximum)/2
	if abs(target-range_mean) > 15:
		return "Your target is too hard to hit. Target must be within 15 of the midpoint of the range."

	shot = 0
	counter = 0
	if verbose:
		print "Shooting for: %i" % target
	while shot != target:
		counter+=1
		if counter > 500:
			if verbose:
				sys.stdout.write("\r")
				return "Shot missed!"
			else:
				return -1
		if verbose:
			sys.stdout.write("\r%i" % counter)
			sys.stdout.flush()
		shot = averageAverages(minimum, maximum);
		
	
	if verbose:
		sys.stdout.write("\r")
		return "Iterations: %i" % counter
	else:
		return counter

def averageAverages(minimum, maximum):
	averages = []
	for x in range(0, 50):
		averages.append(createAverage(minimum, maximum))

	return (sum(averages)/len(averages))

def createAverage(minimum, maximum):
	nums = []
	for x in range(minimum, maximum):
		nums.append(random.randint(1,1000))

	return (sum(nums)/len(nums))





