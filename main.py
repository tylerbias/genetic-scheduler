import hit_the_target
import evolution_simulator
from Tkinter import *
import tkFont

BG_COLOR = "#4c8252"
BUTTON_COLOR = "#426fb7"

class App(Frame):

	eco = evolution_simulator.ecosystem()

	def __init__(self, master):

		Frame.__init__(self, master)
		self.master = master
		master.var = StringVar(self)
		master.var.set("")
		self.pack()
		self.make_widgets()

	def make_widgets(self):
		self.winfo_toplevel().title("Tyler's Project")

		self.intro = Label(self, text="Tyler's project has a GUI!", fg="white", width=60, height= 5)
		self.intro.pack()

		self.centerFrame = Frame(self.master)
		self.centerFrame.pack()

		self.spawnButton = Button(self.centerFrame, text="Spawn", fg="white", width=7, bg=BUTTON_COLOR, command=self.spawn_first_generation)
		self.spawnButton.pack(side=LEFT)

		self.center_spacer = Label(self.centerFrame, text="", width=1)
		self.center_spacer.pack(side=LEFT)

		self.cataclysmButton = Button(self.centerFrame, text="Destroy", fg="white", width=7, bg="red", command=self.cataclysm)
		self.cataclysmButton.pack(side=RIGHT)

		self.low_pad = Label(self.master, textvariable=self.master.var, height=5)
		self.low_pad.pack()


	def spawn_first_generation(self):
		self.eco.first_generation()
		self.master.var.set("Creation successful\nNew creature: %s" % self.eco.most_recently_created)
		# f = open(self.eco.most_recently_created, "r")
		# self.master.var.set(f.read())

	def cataclysm(self):
		self.eco.cataclysmic_event()
		self.master.var.set("All creatures wiped out.")



root = Tk()
StringVar()
root.tk_setPalette(background=BG_COLOR)
root.tk
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=18)

app = App(root)

root.mainloop()
# root.destroy() # optional; see description below