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

class mouse_wrapper(object):
    def __init__(self, wrapped_class,*args,**kwargs):
        self.wrapped_class = wrapped_class(*args,**kwargs)

    #inheret attributes from underlying object
    def __getattr__(self, attr):
        orig_attr = self.wrapped_class.__getattribute__(attr)
        #if callable, should pass *args and **kwargs
        if callable(orig_attr):
            def hooked(*arg, **kwargs):
                result == orig_attr(*args,**kwargs)
                if result == self.wrapped_class:
                    return self
                return result
            return hooked
        else:
            return orig_attr



class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()
        self.closeWindow(self.win)
        # self.win.requestProperties(wp)
        golog1 = mouse_wrapper(golog, self)
        golog2 = golog(self, label = "golog2")
        gologToWindow(self, golog1)
        gologToWindow(self, golog2)


r = runner()
r.run()
