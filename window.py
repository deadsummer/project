from tkinter import *
from tkinter.filedialog import *
import fileinput

def _open():
	op = askopenfilename()
	for l in fileinput.input(op):
		txt.insert(END,l)

root = Tk()

m = Menu(root)
root.config(menu=m)

fm = Menu(m)
m.add_cascade(label="File",menu=fm)
fm.add_command(label="Open...",command=_open)

txt = Text(root,width=40,height=15,font="12")
txt.pack()

root.mainloop()

