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
    def __init__(self, base,*args,**kwargs):
        golog.__init__(self,base,*args,**kwargs)
        self.buttons = {'mouse1':self.mouse1,'mouse3':self.mouse3}
        base.accept(self.label+"_mouse1",self.mouse1)
        base.accept(self.label+"_mouse3",self.mouse3)


    #Inheret attributes from wrapped golog
    # def __getattr__(self, attr):
    #     print('yo')
    #     if hasattr(self.golog,attr):
    #         orig_attr = self.golog.__getattribute__(attr)
    #
    #     else:
    #         return self.__getattribute__(attr)
    #     #if callable, should pass *args and **kwargs and return what call returns
    #     if callable(orig_attr):
    #         def hooked(*arg, **kwargs):
    #             result == orig_attr(*args,**kwargs)
    #             if result == self.wrapped_class:
    #                 return self
    #             return result
    #         return hooked
    #     else:
    #         return orig_attr

    def mouse1(self,mw):
        mpos = mw.node().getMouse()
        self.pickerRay.setFromLens(self.camNode,mpos.getX(),mpos.getY())
        self.cTrav.traverse(self.render)
        self.queue.sortEntries()
        entry = self.queue.getEntry(0)

        if entry.getIntoNodePath().getParent() == self.planeNode:
            for node in self.selected: node.setColorScale(1,1,1,1) #turn white
            self.selected = []
        else:
            if entry.getIntoNodePath().getParent() not in self.selected:
                self.selected.append(entry.getIntoNodePath().getParent())#.getTag('simplex'))
            entry.getIntoNodePath().getParent().setColorScale(1,0,0,0) #turn red

        if len(self.selected) >= 2:
            faces = tuple([self.graphicsToSimplex[faceGr] for faceGr in self.selected[-1:-3:-1]])
            self.createMorphism(faces) #reversed selected objects and creates a 1 - simplex from them


    def mouse3(self,mw):
        mpos = mw.node().getMouse()
        self.pickerRay.setFromLens(self.camNode,mpos.getX(),mpos.getY())
        self.cTrav.traverse(self.render)
        self.queue.sortEntries()
        entry = self.queue.getEntry(0)
        if entry.getIntoNodePath().getParent() == self.planeNode:
            for node in self.selected: node.setColorScale(1,1,1,1) #turn white
            self.selected = []
            self.createObject(setPos = entry.getSurfacePoint(entry.getIntoNodePath()),
                            label = str(len(self.sSet.rawSimps)))



class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()
        self.closeWindow(self.win)
        # self.win.requestProperties(wp)
        golog1 = mouse_wrapper(self)
        gologToWindow(self, golog1)


r = runner()
r.run()
