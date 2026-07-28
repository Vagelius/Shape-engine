from tkinter import *

master = Tk()

var1 = IntVar()
var2 = IntVar()

def update_sliders(value):
    print("Variable 1:", var1.get())
    print("Variable 2:", var2.get())

w1 = Scale(master, from_=0, to=42, variable=var1, command=update_sliders)
w1.pack()

w2 = Scale(master, from_=0, to=200, orient=HORIZONTAL, variable=var2, command=update_sliders)
w2.pack()

mainloop()