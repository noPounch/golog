import sys
import tkinter as tk
from golog_export import *
from direct.showbase.ShowBase import ShowBase
from golog import golog as Golog
from window_manager import *
from mode_head import *
from tk_funcs import save_load_new


version = '1.0.0'


class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType = 'none')
        self.disable_mouse()


        # need to migrate into gologToWindow
        base.accept("f5", sys.exit)
        base.accept("f6", sys.exit)

        (newv, save_location) = save_load_new()
        (folder_path, golog_file) = os.path.split(save_location)
        print(save_location)

        if newv:
            golog = Golog(self, label = golog_file.split('.golog')[0])
            gexport(golog, save_location)
            self.controllable_golog = mode_head(self,golog, folder_path = folder_path)
            self.controllable_golog.selection_and_creation()
            modeHeadToWindow(self, self.controllable_golog)

        elif not newv:
            golog = gimport(self,save_location)
            self.controllable_golog = mode_head(self,golog, folder_path = folder_path)
            self.controllable_golog.selection_and_creation()
            modeHeadToWindow(self, self.controllable_golog)


r = runner()
debug = r.controllable_golog
r.run()
