import os
import sys
from tkinter import *

def ask_simplex_data():

    master = Tk()
    master.title('simplex data')
    mathDataString = None
    label = None

    Label(master, text='Label').grid(row=0,column = 0)
    labelvar = StringVar(master)
    labelvar.set('It\'s just like, a simplex, bro')
    labelentry = Entry(master, textvariable=labelvar)
    labelentry.grid(row = 0, column = 1)


    #data options on click
    options = ['None','golog', 'olog', 'text', 'file']
    Label( master, text = "Add Math Data?").grid(row = 1,column = 0)
    MathDataVariable = StringVar(master)
    MathDataVariable.set(options[0])
    mathDataMenu = OptionMenu(master, MathDataVariable, *options)
    mathDataMenu.grid(row = 1, column =1)
    creation = Button(master, text = 'create', command = master.destroy)
    creation.grid(row = 2)
    master.bind('<Return>',lambda event: master.destroy())

    master.bind("<FocusIn>", lambda entry: labelentry.selection_range(0, END))
    labelentry.focus()
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

def save_load_new():
    master = Tk()
    master.title('new golog?')
    Label(master, text='Save Location:').grid(row=0,column = 0)
    newvar = BooleanVar(master)
    savevar = StringVar(master)
    savevar.set('save/test.golog')
    saveentry = Entry(master, textvariable=savevar)
    saveentry.grid(row = 0, column = 1)
    #check if load location exists (and is a golog)
    def loadg():
        newvar.set(False)
        master.destroy()

    def newg():
        newvar.set(True)
        master.destroy()
    #data options on click
    Button(master, text = 'Load', command = loadg).grid(row = 1,column = 0)
    Button(master, text = 'New',command =  newg).grid(row = 1,column = 1)

    saveentry.focus()
    master.mainloop()
    #do after master tkbox is destroyed
    return (newvar.get(), savevar.get())

def edit_txt(fname):
    root = Tk()
    height = 300
    width = 300
    text_box = Text(root)


    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    left = (screen_width / 2) - (width / 2)
    top = (screen_height / 2) - (height /2)
    root.geometry('%dx%d+%d+%d' % (width, height, left, top))
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    text_box.grid(sticky = N + E + S + W)

    #open file and place in textbox
    try:
            root.wm_iconbitmap("Notepad.ico")
    except:
            pass
    root.title(os.path.basename(fname) + " - Notepad")
    with open(fname,"r") as file:
        text_box.delete(1.0,END)
        text_box.insert(1.0,file.read())

    def save_and_exit(event):
        with open(fname,'w') as file:
            file.write(text_box.get(1.0,END))
            root.destroy()
    root.bind('<Control-Key-s>', save_and_exit)
    root.mainloop()
    sys.exit()
