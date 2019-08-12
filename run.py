import sys
import tkinter as tk
from golog_export import *
from direct.showbase.ShowBase import ShowBase
from golog import golog as Golog
from window_manager import *
from mode_head import *
from tk_funcs import save_load_new


version = '1.0.0'

def new_golog(base, folder_path,golog_file):
    golog = Golog(base, label = golog_file.split('.golog')[0])
    golog_folder = os.path.join(folder_path,golog.label)
    if not os.path.exists(golog_folder): os.mkdir(golog_folder)
    save_location = os.path.join(golog_folder,golog.label+'.golog')


    gexport(golog, save_location)
    controllable_golog = mode_head(base,golog, folder_path = golog_folder)
    modeHeadToWindow(base, controllable_golog)
    return controllable_golog

def load_golog(base, folder_path, save_location):
    golog = gimport(base,save_location)
    controllable_golog = mode_head(base,golog, folder_path = folder_path)
    modeHeadToWindow(base, controllable_golog)
    return controllable_golog



class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType = 'none')
        self.disable_mouse()


        # need to migrate into gologToWindow
        base.accept("f5", sys.exit)
        base.accept("f6", sys.exit)

        (newv, save_location) = save_load_new()
        (folder_path, golog_file) = os.path.split(save_location)


        if newv: new_golog(self,folder_path, golog_file)

        elif not newv: load_golog(self, folder_path,save_location)


r = runner()
r.run()
