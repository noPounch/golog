import os, subprocess, platform, shutil
import sys
from tkinter import *
from tkinter import filedialog
from datetime import date



#? make windowsize larger
def ask_weblink():
    master = Tk()
    master.geometry('+'+ str(master.winfo_pointerxy()[0])+'+'+str(master.winfo_pointerxy()[1]))
    linkvar = StringVar()
    Label(master, text = 'Enter Web Address:').grid(row = 0, sticky = 'nesw')
    Entry(master, textvariable = linkvar).grid(row = 1, sticky = 'nesw')
    Button(master, text = 'ok', command = master.destroy).grid(row = 2, sticky = 'nesw')
    master.mainloop()
    link = linkvar.get()
    print(link[:8])
    if link[:8] != 'https://' : link = 'https://' + link #webbrowser now looks for https for whatever reason
    return link


def ask_delete_path(file_path):

    if os.path.isdir(file_path):dir = True
    elif os.path.isfile(file_path): dir = False
    else:
        print(file_path+" doesn't exist")
        return

    master = Tk()
    master.geometry('+'+ str(master.winfo_pointerxy()[0])+'+'+str(master.winfo_pointerxy()[1]))
    master.title('Are you sure you want to delete this path?')
    Label(master, text = file_path).grid(row = 0)
    def yes():
        if dir:
            shutil.rmtree(file_path)
            master.destroy()
        else:
            os.remove(file_path)
            master.destroy()
    Button(master,text = 'yes',command = yes).grid(row = 1,sticky='nesw')



    def no():
        master.destroy()
    Button(master,text = 'no',command = no).grid(row = 2,sticky='nesw')
    master.mainloop()


def are_you_sure(question):
    master = Tk()
    master.geometry('+'+ str(master.winfo_pointerxy()[0])+'+'+str(master.winfo_pointerxy()[1]))
    Label(master, text = question).grid(row = 0, column = 0, sticky = 'nesw')
    master.answer = None
    def yes():
        master.answer = 'yes'
        master.destroy()
    Button(master, text = 'yes',command = yes).grid(row = 1, column = 1, sticky = 'nesw')
    def no():
        master.answer = 'no'
        master.destroy()
    Button(master, text = 'no',command = no).grid(row = 1, column = 0, sticky = 'nesw')
    master.mainloop()
    return master.answer
# print(are_you_sure('Are you sure you want to delete this math_data?'))


def ask_math_data(Default_Label = 'Simplex'):
    master = Tk()
    master.title('simplex data')
    master.geometry('+'+ str(master.winfo_pointerxy()[0])+'+'+str(master.winfo_pointerxy()[1]))
    master.returner = None


    Label(master, text='Label').grid(row=0,column = 0)
    labelvar = StringVar(master)
    labelvar.set(Default_Label)
    labelentry = Entry(master, textvariable=labelvar)
    labelentry.grid(row = 0, column = 1)

    #data options on click
    options = ['None','golog', 'file','text','latex','weblink']
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

    master.bind("<FocusIn>", lambda entry: labelentry.selection_range(0, END))
    master.bind("<Return>", lambda entry: create())
    master.after(1,master.focus_force())
    master.after(1,labelentry.focus())
    master.mainloop()
    return master.returner #if create, returns type, if cancel, returns None



def unique_path(root, path = []):
    if not path: return path
    if isinstance(path,str): path = [path] #should pass a list, but just in case

    import os
    abs_path = os.path.join(root, *path)
    #if original path doesn't exist, just return path
    if not os.path.exists(abs_path):
        return path


    def cpesmd(num):
        abs_path = os.path.join(root,*path) + str(num) + ext
        if not os.path.exists(abs_path):
            #if path doesn't exist, return number
            return num
        else:
            print('oof'+str(num))
            return cpesmd(num+1)
    #get rid of extention for now, recover it on return
    path[-1], ext = os.path.splitext(path[-1])
    return path[:-1] + [path[-1] + str(cpesmd(0))+ext]



def save_load_new(default_location = os.path.abspath('./user_files/save'), recent_path = None):
    master = Tk()
    master.geometry('+'+ str(master.winfo_pointerxy()[0])+'+'+str(master.winfo_pointerxy()[1]))
    master.title('New / Load golog')
    master.newvar = False
    master.namevar = StringVar(master)
    master.namevar.set('Name_Your_Golog')
    Label(text = 'Golog Name:').grid(row = 0, column = 0)
    Entry(textvariable = master.namevar).grid(row = 0, column = 1)


    master.loc = None
    def loadg():
        master.loc = filedialog.askopenfilename(initialdir = default_location,title = "Select file", filetypes = (("gologs","*.golog"),("all files","*.*")))
        if master.loc: #if location is provided, destroy and return. Else go back to save_load_new
            master.destroy()
    Button(master, text = 'Load', command = loadg).grid(row = 1,column = 2)

    def newg():
        master.newvar = True
        if not master.namevar.get():
            master.namevar.set('Seriously')
            return
        proploc = os.path.join(os.path.abspath(filedialog.askdirectory(initialdir = default_location)),os.path.relpath(master.namevar.get()+'.golog'))
        if os.path.exists(proploc): #if proposed location already exists change name
            master.namevar.set(master.namevar.get()+"(new)")

        else:
            master.loc = proploc
            master.destroy()
    Button(master, text = 'New',command =  newg).grid(row = 1,column = 0)



    #data options on click

    def newD():
        daily_path = os.path.join(default_location,'daily_ontologies')
        if not os.path.exists(daily_path):os.mkdir(daily_path)
        master.newvar = True
        formatted_date = date.today().strftime('%b')+'_'+date.today().strftime('%d')+'_'+date.today().strftime('%Y')
        date_path = os.path.join(daily_path,formatted_date)
        if not os.path.exists(date_path):os.mkdir(date_path)
        master.loc = os.path.join(date_path,*unique_path(date_path,['daily_golog.golog']))
        master.destroy()
    Button(master, text = 'New Daily', command = newD).grid(row = 2,column = 0)



    def recg():
        master.newvar = False
        master.loc = recent_path
        master.destroy()




    if recent_path:
        Button(master, text = 'Recent',command =  recg).grid(row = 1,column = 1)
        Label(text = os.path.split(recent_path)[1]).grid(row = 2, column = 1)

    def loadD():
        daily_path = os.path.join(default_location,'daily_ontologies')
        if not os.path.exists(daily_path):os.mkdir(daily_path)
        master.loc = filedialog.askopenfilename(initialdir = daily_path,title = "Select file", filetypes = (("gologs","*.golog"),("all files","*.*")))
        if master.loc: master.destroy() #if location is provided



    Button(master, text = 'Load Daily',command =  loadD).grid(row = 2,column = 2)


    master.mainloop()
    #do after master tkbox is destroyed
    #return whether it is a new golog or loading a golog, and it's folder on this system
    return (master.newvar, master.loc)


# makes a unique path from a master in save with given name



def load_tex(abs_path):
    master = Tk()
    master.geometry('+'+ str(master.winfo_pointerxy()[0])+'+'+str(master.winfo_pointerxy()[1]))
    master.title('Load / New .tex File')
    master.loc = []
    Label(master, text = 'New Latex File, or Load').grid(row = 0, column = 1)
    def loadg():
        master.loc = filedialog.askopenfilename(initialdir = abs_path,title = "Select file", filetypes = (("Latex Files","*.tex"),("all files","*.*")))
        if master.loc:
            master.destroy()

    def newg():
        master.loc = True
        master.destroy()

    Button(master, text = 'Load', command = loadg).grid(row = 1,column = 0)
    Button(master, text = 'New',command =  newg).grid(row = 1,column = 1)


    master.mainloop()
    return master.loc

def edit_txt(fname = None, text = None):
    master = Tk()
    master.geometry('+'+ str(master.winfo_pointerxy()[0])+'+'+str(master.winfo_pointerxy()[1]))
    height = 300
    width = 300
    text_box = Text(master)
    if text: text_box.insert('1.0', text)


    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    left = (screen_width / 2) - (width / 2)
    top = (screen_height / 2) - (height /2)
    master.geometry('%dx%d+%d+%d' % (width, height, left, top))
    master.grid_rowconfigure(0, weight=1)
    master.grid_columnconfigure(0, weight=1)
    text_box.grid(sticky = N + E + S + W)

    #open file and place in textbox
    try:
            master.wm_iconbitmap("Notepad.ico")
    except:
            pass

    if not fname:
            master.mainloop()
            return

    master.title(os.path.abspath(fname) + " - Notepad")
    with open(fname,"r") as file:
        text_box.delete(1.0,END)
        text_box.insert(1.0,file.read())

    def save_and_exit(event):
        with open(fname,'w') as file:
            file.write(text_box.get(1.0,END))
            master.destroy()
    master.bind('<Control-Key-s>', save_and_exit)
    master.mainloop()

def ask_file_location(initial_dir = os.path.abspath(os.path.dirname(__file__))):
    master = Tk()
    master.geometry('+'+ str(master.winfo_pointerxy()[0])+'+'+str(master.winfo_pointerxy()[1]))
    filename =  filedialog.askopenfilename(initialdir = initial_dir,title = "Select file")
    master.destroy()
    return filename

def ask_folder_location(initial_dir = os.path.abspath(os.path.dirname(__file__))):
    master = Tk()
    master.geometry('+'+ str(master.winfo_pointerxy()[0])+'+'+str(master.winfo_pointerxy()[1]))
    folder_path = os.path.abspath(filedialog.askdirectory(initialdir = initial_dir, title = "Select Folder"))
    master.destroy()
    return folder_path

def run_program(default_program = '', file=''):
    master = Tk()
    master.geometry('+'+ str(master.winfo_pointerxy()[0])+'+'+str(master.winfo_pointerxy()[1]))
    master.title('Command')
    programvar = StringVar(master)
    programvar.set(default_program)
    programentry = Entry(master, textvariable=programvar)
    programentry.grid(row = 0,column = 0)
    master.bind("<FocusIn>", lambda *event: programentry.selection_range(0, END))

    filevar = StringVar(master)
    filevar.set(file)
    filelabel=Label(textvariable = filevar)
    filelabel.grid(row=0,column = 1)
    def getprogram():
        programpath = filedialog.askopenfilename(initialdir = os.path.abspath(os.path.dirname(__file__)),title = "Select Program")
        programvar.set(programpath)
    Button(master, text = 'Select Program',command=getprogram).grid(row=1,column=0)

    def selectfile():
        filepath = filedialog.askopenfilename(initialdir = os.path.abspath(os.path.dirname(__file__)),title = "Select File")
        filevar.set(filepath)
    Button(master, text = 'Select File',command=selectfile).grid(row=1,column=1)

    def docommand():
        #do command
        master.destroy()
        if not programvar.get():
            if platform.system() == 'Darwin':       # macOS
                subprocess.call(('open', filevar.get()))
            elif platform.system() == 'Windows':    # Windows
                os.startfile(filevar.get())
            else:                                   # linux
                subprocess.call(('xdg-open', filevar.get()))
            # subprocess.run(['xdg-open',filevar.get()], check = True)
        else: subprocess.run([programvar.get(),filevar.get()])

    Button(master, text = 'run command', command = docommand).grid(row=1,column=2)
    master.mainloop()

# run_program()

def error_reset_dialog(err):
    edit_txt(text = err)


def pdf_or_tex(pdf_file,tex_file):
    master = Tk()
    master.geometry('+'+ str(master.winfo_pointerxy()[0])+'+'+str(master.winfo_pointerxy()[1]))
    def openpdf():
        master.destroy()
        run_program('',file=pdf_file)
    if pdf_file: Button(master, text ='open'+os.path.basename(pdf_file),command = openpdf).grid(row = 0 , column = 0)
    else: Label(master, text ='No PDF File').grid(row = 0 , column = 0)

    def opentex():
        master.destroy()
        run_program('',file=tex_file)
    if tex_file: Button(master, text ='open'+os.path.basename(tex_file),command = opentex).grid(row = 0 , column = 1)
    else: Label(master, text ='No Tex File').grid(row = 0 , column = 1)
    master.mainloop()
