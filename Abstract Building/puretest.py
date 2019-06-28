from tkinter import *

def get_label():
    master = Tk()
    master.title('enter label')
    label = None
    labelvar = StringVar(master)
    Entry(master, textvariable=labelvar).grid(row = 0)
    creation = Button(master, text = 'create', command = master.destroy)
    creation.grid(row = 1)

    master.mainloop()
    return labelvar.get()

def attach_math_data(simplex, mathData):
    #check type of data
    #if string, map to create mathData creation
    #if data, attach to simplex.mathData
    if isinstance(mathData, String):
        if mathData == 'golog':
            new_golog = golog.golog(self.base, label = get_label())
