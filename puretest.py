import sys, os
from direct.showbase.ShowBase import ShowBase
from direct.showutil.Rope import Rope

from panda3d.core import *
# from direct.showbase.InputStateGlobal import inputState


version = '1.0.0'


class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()



r = runner()
# r.run()
