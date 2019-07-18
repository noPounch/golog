import os, subprocess, platform
import sys
from tkinter import *
from tkinter import filedialog

def ask_simplex_data():

    master = Tk()
    master.title('simplex data')
    mathDataString = None
    label = None

    Label(master, text='Label').grid(row=0,column = 0)
    labelvar = StringVar(master)
    labelvar.set('Simplex')
    labelentry = Entry(master, textvariable=labelvar)
    labelentry.grid(row = 0, column = 1)


    #data options on click
    options = ['None','golog', 'latex', 'file']
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

def ask_math_data(Default_Label = 'Simplex'):
    master = Tk()
    master.title('simplex data')
    mathDataString = None
    master.returner = None

    Label(master, text='Label').grid(row=0,column = 0)
    labelvar = StringVar(master)
    labelvar.set(Default_Label)
    Entry(master, textvariable=labelvar).grid(row = 0, column = 1)


    #data options on click
    options = ['None','golog', 'file','latex']
    Label(master, text = "Math Data Type: ").grid(row = 1,column = 0)
    MathDataVariable = StringVar(master)
    MathDataVariable.set(options[0])
    mathDataMenu = OptionMenu(master, MathDataVariable, *options)
    mathDataMenu.grid(row = 1, column =1)

    def create():
        master.returner = (labelvar.get(), MathDataVariable.get())
        master.destroy()
    Button(master, text = 'new', command = create).grid(row = 2,column = 0)

    def cancel():
        master.destroy()
    Button(master, text = 'cancel', command = cancel).grid(row = 2, column = 1)

    master.mainloop()
    return master.returner #if create, returns type, if cancel, returns None

# print(ask_math_data('hello'))

def save_load_new(default_location = os.path.abspath('./save')):
    master = Tk()
    master.title('New / Load golog')
    master.newvar = False
    master.namevar = StringVar(master)
    Label(text = 'Golog Name:').grid(row = 0, column = 0)
    Entry(textvariable = master.namevar).grid(row = 0, column = 1)


    master.loc = None
    def loadg():
        master.loc = filedialog.askopenfilename(initialdir = default_location,title = "Select file", filetypes = (("gologs","*.golog"),("all files","*.*")))
        if master.loc: #if location is provided, destroy and return. Else go back to save_load_new
            master.destroy()

    def newg():
        master.newvar = True
        proploc = os.path.join(filedialog.askdirectory(initialdir = default_location),master.namevar.get()+'.golog')
        if os.path.exists(proploc): #if proposed location already exists change name
            master.namevar.set(master.namevar.get()+"(new)")
            return
        master.loc = proploc
        master.destroy()

    #data options on click
    Button(master, text = 'Load', command = loadg).grid(row = 1,column = 0)
    Button(master, text = 'New',command =  newg).grid(row = 1,column = 1)

    master.mainloop()
    #do after master tkbox is destroyed
    return (master.newvar, master.loc)

# print(save_load_new())

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

def ask_file_location(initial_dir = os.path.abspath(os.path.dirname(__file__))):
    root = Tk()
    filename =  filedialog.askopenfilename(initialdir = initial_dir,title = "Select file")#,filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    root.destroy()
    return filename

def ask_folder_location(initial_dir = os.path.abspath(os.path.dirname(__file__))):
    root = Tk()
    folder_path = os.path.abspath(filedialog.askdirectory(initialdir = initial_dir, title = "Select Folder"))
    root.destroy()
    return folder_path

def run_program(default_program = '', file=''):
    root = Tk()
    root.title('Command')
    programvar = StringVar(root)
    programvar.set(default_program)
    programentry = Entry(root, textvariable=programvar)
    programentry.grid(row = 0,column = 0)
    root.bind("<FocusIn>", lambda *event: programentry.selection_range(0, END))

    filevar = StringVar(root)
    filevar.set(file)
    filelabel=Label(textvariable = filevar)
    filelabel.grid(row=0,column = 1)
    def getprogram():
        programpath = filedialog.askopenfilename(initialdir = os.path.abspath(os.path.dirname(__file__)),title = "Select Program")
        programvar.set(programpath)
    Button(root, text = 'Select Program',command=getprogram).grid(row=1,column=0)

    def selectfile():
        filepath = filedialog.askopenfilename(initialdir = os.path.abspath(os.path.dirname(__file__)),title = "Select File")
        filevar.set(filepath)
    Button(root, text = 'Select File',command=selectfile).grid(row=1,column=1)

    def docommand():
        #do command
        root.destroy()
        if not programvar.get():
            if platform.system() == 'Darwin':       # macOS
                subprocess.call(('open', filevar.get()))
            elif platform.system() == 'Windows':    # Windows
                os.startfile(filevar.get())
            else:                                   # linux
                subprocess.call(('xdg-open', filevar.get()))
            # subprocess.run(['xdg-open',filevar.get()], check = True)
        else: subprocess.run([programvar.get(),filevar.get()])

    Button(root, text = 'run command', command = docommand).grid(row=1,column=2)
    root.mainloop()

def pdf_or_tex(pdf_file,tex_file):
    root = Tk()
    def openpdf():
        root.destroy()
        run_program('',file=pdf_file)
    if pdf_file: Button(root, text ='open'+os.path.basename(pdf_file),command = openpdf).grid(row = 0 , column = 0)
    else: Label(root, text ='No PDF File').grid(row = 0 , column = 0)

    def opentex():
        root.destroy()
        run_program('',file=tex_file)
    if tex_file: Button(root, text ='open'+os.path.basename(tex_file),command = opentex).grid(row = 0 , column = 1)
    else: Label(root, text ='No Tex File').grid(row = 0 , column = 1)
    root.mainloop()
