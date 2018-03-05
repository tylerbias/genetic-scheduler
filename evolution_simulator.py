import datetime
import random
import glob
import os

POP_SIZE = 50

class ecosystem:
	last_path = ""
	path_increment = 1
	most_recently_created = ""

	def first_generation(self):
		day = datetime.date.today().strftime("%d")
		month = datetime.date.today().strftime("%m")
		year = datetime.date.today().strftime("%Y")
		hour = datetime.datetime.now().strftime("%H")
		minute = datetime.datetime.now().strftime("%M")
		second = datetime.datetime.now().strftime("%S")

		filepath = ("./creatures/%s-%s-%s--%s-%s-%s.txt" % (month, day, year, hour, minute, second))

		if filepath == self.last_path:
			self.path_increment += 1
		else:
			self.last_path = filepath
			self.path_increment = 1

		if self.path_increment < 10:
			filepath = "./creatures/%s-%s-%s--%s-%s-%s--0%s.txt" % (month, day, year, hour, minute, second, self.path_increment)
		else:
			filepath = "./creatures/%s-%s-%s--%s-%s-%s--%s.txt" % (month, day, year, hour, minute, second, self.path_increment)


		creatureTxt = open(filepath, "w")

		for x in range(0, POP_SIZE):
			newCreature = []
			newCreature.append(random.randint(0, 1000))
			newCreature.append(random.randint(0, 1000))
			newCreature.sort()
			creatureTxt.write("%s (%s, %s)\n" % (x+1, newCreature[0], newCreature[1]))

		creatureTxt.close()

		self.most_recently_created = filepath

		return

	def cataclysmic_event(self):
		filesToRemove = glob.glob("./creatures/*")
		for f in filesToRemove:
			os.remove(f)
		return 1
