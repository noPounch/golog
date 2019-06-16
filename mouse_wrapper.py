#goal of this file is to create:
#1) an export function that returns simplecies
#2) an import function that checks face conditions on simplecies
#--That The faces even exist (raise exception)
#--That they satisfy the face conditions (return in conditions string)
#--That they satisfy degeneracy conditions (return in conditions string)

import hcat
import golog
import window_manager
# from window_manager import *

class mode_manager():
    def __init__(self,base):
        self.base = base

    def reset(golog):
        golog.buttons = dict()



class selection_and_creation_mode():
    def __init__(self, base, golog = None, *args,**kwargs):
        self.base = base

        if not golog:
            self.golog = golog.golog(base,*args,**kwargs)
            print(self.golog.label)
        else: self.golog = golog
        print(self.golog.label + " created in a selection and creation mode")
        # defaults = {'golog':golog(base,*args,**kwargs)}
        # for key in defaults:
        #     if key in kwargs: setattr(self,key,kwargs[key])
        #     else: setattr(self,key,defaults[key])
        self.golog.buttons = {**self.golog.buttons,**{'mouse1':self.mouse1,'mouse3':self.mouse3, 'space':self.space}}
        base.accept(self.golog.label+"_mouse1",self.mouse1) #make
        base.accept(self.golog.label+"_space",self.space)
        base.accept(self.golog.label+"_mouse3",self.mouse3)


    def mouse1(self,mw):
        mpos = mw.node().getMouse()
        self.golog.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY())
        self.golog.cTrav.traverse(self.golog.render)
        self.golog.queue.sortEntries()
        entry = self.golog.queue.getEntry(0)

        if entry.getIntoNodePath().getParent() == self.golog.planeNode:
            for node in self.golog.selected: node.setColorScale(1,1,1,1) #turn white
            self.golog.selected = []
        else:
            if entry.getIntoNodePath().getParent() not in self.golog.selected:
                self.golog.selected.append(entry.getIntoNodePath().getParent())#.getTag('simplex'))
            entry.getIntoNodePath().getParent().setColorScale(1,0,0,0) #turn red

        if len(self.golog.selected) >= 2:
            faces = tuple([self.golog.NPtoSimplex[faceGr] for faceGr in self.golog.selected[-1:-3:-1]])
            self.golog.createMorphism(faces) #reversed selected objects and creates a 1 - simplex from them

    def space(self,mw):
        if not mw.node().hasMouse(): return
        mpos = mw.node().getMouse()
        self.golog.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY())
        self.golog.cTrav.traverse(self.golog.render)
        self.golog.queue.sortEntries()
        entry = self.golog.queue.getEntry(0)#.getIntoNodePath().getParent
        if entry.getIntoNodePath().getParent() != self.golog.planeNode: simplex = self.golog.NPtoSimplex[entry.getIntoNodePath().getParent()]
        if isinstance(simplex,hcat.Simplex):
            if simplex.mathData:
                print('')
                if isinstance(simplex.mathData,golog.golog):
                    print('mathData is a golog!')
            else:
                newgolog = golog.golog(self.base, label = simplex.label+"_subgolog")
                controllable_golog = selection_and_creation_mode(self.base, newgolog)
                window_manager.gologToWindow(self.base, controllable_golog.golog)
        # subgolog =


    def mouse3(self,mw):

        mpos = mw.node().getMouse()
        self.golog.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY())
        self.golog.cTrav.traverse(self.golog.render)
        self.golog.queue.sortEntries()
        entry = self.golog.queue.getEntry(0)
        if entry.getIntoNodePath().getParent() == self.golog.planeNode:
            for node in self.golog.selected: node.setColorScale(1,1,1,1) #turn white
            self.golog.selected = []
            self.golog.createObject(setPos = entry.getSurfacePoint(entry.getIntoNodePath()),
                            label = str(len(self.golog.sSet.rawSimps)))
