import sys
from golog_export import *
from direct.showbase.ShowBase import ShowBase
from golog import golog as Golog
from window_manager import *
from mode_head import *


class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()
        self.closeWindow(self.win)


        # need to migrate into gologToWindow
        base.accept("f5",sys.exit)
        base.accept("f6",sys.exit)

        # golog = Golog(self, label = 'run')
        golog = gimport(self,'save/test.golog')
        controllable_golog = mode_head(self,golog)
        controllable_golog.testing_mode()
        modeHeadToWindow(self, controllable_golog)

r = runner()
r.run()
