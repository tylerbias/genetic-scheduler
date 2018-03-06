import hit_the_target
import evolution_simulator
import scheduler
from Tkinter import *
import tkFont

BG_COLOR = "#4c8252"
BUTTON_COLOR = "#426fb7"

class initial_menu(Frame):

	eco = evolution_simulator.ecosystem()

	def __init__(self, master):

		Frame.__init__(self, master)
		self.master = master
		self.pack()
		self.make_widgets()

	def make_widgets(self):
		self.winfo_toplevel().title("Tyler's Project")

		self.intro = Label(self, text="Tyler's project has a GUI!", fg="white", width=60, height= 5)
		self.intro.pack()


		self.cataclysmButton = Button(self, text="Set Up Schedule", fg="white", bg="blue", command=self.schedule_set_up)
		self.cataclysmButton.pack()

		self.low_pad = Label(self, height=5)
		self.low_pad.pack()


	def spawn_first_generation(self):
		self.eco.first_generation()
		self.master.var.set("Creation successful\nNew creature: %s" % self.eco.most_recently_created)
		# f = open(self.eco.most_recently_created, "r")
		# self.master.var.set(f.read())

	def cataclysm(self):
		self.eco.cataclysmic_event()
		self.master.var.set("All creatures wiped out.")

	def schedule_set_up(self):
		schedule_frame(self.master)
		self.destroy()




class schedule_frame(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.master = master
		master.empVar = StringVar(self)
		master.empVar.set("")
		self.employeeList = []
		self.pack()
		self.make_widgets()


	def make_widgets(self):
		self.top_pad = Label(self, height=1, width=60)
		self.top_pad.pack()

		self.test = Button(self, text="Back", command=self.switch_back)
		self.test.pack()

		# Spacing labels, and the button used to trigger the recording of all input given
		# regarding the new employee that is being created.
		self.back_pad_bottom = Label(self, height=1)
		self.back_pad_bottom.pack()

		self.add = Button(self, text="Add an employee", bg="blue", command=self.add_employee)
		self.master.bind('<Return>', self.enter)
		self.add.pack()

		self.add_pad = Label(self, height=1)
		self.add_pad.pack()

		# Entry box widget used to receive new employee's name
		self.emp_entry = Entry(self, font=default_font)
		self.emp_entry.pack()

		# Frame containing widgets used to enter employee's minimum shifts
		self.min_shifts = Frame(self)
		self.min_shifts.pack()

		self.min_label = Label(self.min_shifts, text="Min. Shifts")
		self.min_label.pack(side=LEFT)

		self.min_space = Label(self.min_shifts, width=1)
		self.min_space.pack(side=LEFT)

		self.min_val = Spinbox(self.min_shifts, font=default_font, from_=0, to_=8, width=3)
		self.min_val.pack()

		# Frame containing widget used to set employee's maximum shifts
		self.max_shifts = Frame(self)
		self.max_shifts.pack()

		self.max_label = Label(self.max_shifts, text="Max. Shifts")
		self.max_label.pack(side=LEFT)

		self.max_space = Label(self.max_shifts, width=1)
		self.max_space.pack(side=LEFT)

		self.max_val = Spinbox(self.max_shifts, font=default_font, from_=0, to_=8, width=3)
		self.max_val.pack(side=RIGHT)

		# Dynamically updated list of all added employees
		self.emp_list = Label(self, textvariable=self.master.empVar)
		self.emp_list.pack()

		self.create_schedules = Button(self, text="Generate schedules", bg='blue', command=self.generate)
		self.create_schedules.pack()


	# Function that controls enter key behavior. Triggers addition of employee, same as pressing button
	def enter(self, event=None):
		self.add_employee()

	# The addition of a new employee. Collects all entered information (name, min, max) and produces an
	# employee object from the scheduler class. Triggered by both the button and the enter key.
	def add_employee(self):
		newName = self.emp_entry.get()
		newMin = int(self.min_val.get())
		newMax = int(self.max_val.get())
		self.emp_entry.delete(0, END)

		newEmployee = scheduler.scheduler.employee(newName, newMin, newMax)
		self.employeeList.append(newEmployee)

		theList = "Current Employees:\n"
		for emp in self.employeeList:
			theList+=("%s, %s to %s\n" % (emp.name, emp.min_shifts, emp.max_shifts))
		self.master.empVar.set(theList)

	def generate(self):
		best = scheduler.random_schedule(self.employeeList, 7, 2)
		for i in range(0, 1000):
			temp = scheduler.random_schedule(self.employeeList, 7, 2)
			if temp.get_fitness() > best.get_fitness():
				best = temp

		days = best.get_days()
		for day in days:
			print day
			for shift in sorted(best.get_shifts(day)):
				print "%s belongs to %s" % (shift, best.get_shift_emp(day, shift))
		print best
		print best.get_fitness()




	def switch_back(self):
		initial_menu(self.master)
		self.destroy()





root = Tk()
StringVar()
root.tk_setPalette(background=BG_COLOR)
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=18)

menu = initial_menu(root)

root.mainloop()
# root.destroy() # optional; see description below