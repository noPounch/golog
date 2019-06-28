
from tkinter import *

def ask_simplex_data():

    master = Tk()
    master.title('simplex data')
    mathDataString = None
    label = None

    Label(master, text='Label').grid(row=0,column = 0)
    labelvar = StringVar(master)
    Entry(master, textvariable=labelvar).grid(row = 0, column = 1)


    #data options on click
    options = ['None','golog', 'olog', 'text', 'file']
    Label( master, text = "Add Math Data?").grid(row = 1,column = 0)
    MathDataVariable = StringVar(master)
    MathDataVariable.set(options[0])
    mathDataMenu = OptionMenu(master, MathDataVariable, *options)
    mathDataMenu.grid(row = 1, column =1)
    creation = Button(master, text = 'create', command = master.destroy)
    creation.grid(row = 2)

    master.mainloop()
    return (labelvar.get(), MathDataVariable.get())


def ask_math_type():
    master = Tk()
    master.title('simplex data')
    mathDataString = None
    label = None

    Label(master, text='Label').grid(row=0,column = 0)
    labelvar = StringVar(master)
    Entry(master, textvariable=labelvar).grid(row = 0, column = 1)


    #data options on click
    options = ['None','golog', 'olog', 'text', 'file']
    Label( master, text = "Math Data Type: ").grid(row = 1,column = 0)
    MathDataVariable = StringVar(master)
    MathDataVariable.set(options[0])
    mathDataMenu = OptionMenu(master, MathDataVariable, *options)
    mathDataMenu.grid(row = 1, column =1)
    creation = Button(master, text = 'create', command = master.destroy)
    creation.grid(row = 2)

    master.mainloop()
    return (labelvar.get(), MathDataVariable.get())
