#goal of this file is to create:
#1) an export function that returns simplecies
#2) an import function that checks face conditions on simplecies
#--That The faces even exist (raise exception)
#--That they satisfy the face conditions (return in conditions string)
#--That they satisfy degeneracy conditions (return in conditions string)

import os, sys
sys.path.append(os.path.abspath('..'))

from direct.showbase.ShowBase import ShowBase
from root.hcat import *
from root.golog import *
from root.window_manager import *

class mouse_wrapper(golog):
    def __init__(self,*args,**kwargs):
        golog.__init__(self, *args,**kwargs)
        pass


class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()
        self.closeWindow(self.win)
        # self.win.requestProperties(wp)
        golog1 = mouse_wrapper(self)
        # gologToWindow(self, golog1)


r = runner()
r.run()
