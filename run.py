import sys
from direct.showbase.ShowBase import ShowBase
from golog import golog as Golog
from window_manager import *
from mouse_wrapper import *


class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()
        self.closeWindow(self.win)


        # need to migrate into gologToWindow
        base.accept("f5",sys.exit)
        base.accept("f6",sys.exit)

        golog = Golog(self, label = "run")
        # self.win.requestProperties(wp)
        controllable_golog = selection_and_creation_mode(self,golog)
        gologToWindow(self, controllable_golog.golog)


r = runner()
r.run()
