#goal of this file is to create:
#1) an export function that returns simplecies
#2) an import function that checks face conditions on simplecies
#--That The faces even exist (raise exception)
#--That they satisfy the face conditions (return in conditions string)
#--That they satisfy degeneracy conditions (return in conditions string)

import hcat
import golog
import window_manager
from panda3d.core import NodePath, Camera
from panda3d.core import Vec3, Point3, LPoint3f, Plane
from panda3d.core import CollisionPlane, CollisionRay, CollisionSphere
from panda3d.core import CollisionNode, CollisionTraverser, CollisionHandlerQueue


class mode_head():
    def __init__(self,base,Golog):
        self.base = base
        self.golog = Golog
        self.label = self.golog.label+ "_mode_head"

        #label modehead uniquely
        #make a dictionary of mode data in modes
        # if hasattr(self.golog,'modes'):
        #     self.label = self.golog.label+"_mode_head_"+len(self.golog.modeData.keys())
        #     self.golog.modeData[self.label] = dict()
        # else:
        #     self.label = self.golog.label+"_mode_head_"+"0"
        #     self.golog.modeData = dict()
        #     self.golog.modeData[self.label] = dict

    def reset(self, golog):
        golog.buttons = dict()

    def selection_and_creation(self):
        resetList = []

        #Collision Handling
        #set up traverser and handler
        self.cTrav = CollisionTraverser('main traverser')
        self.queue = CollisionHandlerQueue()
        self.selected = []
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.golog.camera.attachNewNode(self.pickerNode)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.cTrav.addCollider(self.pickerNP,self.queue)
        self.planeNode = self.golog.render.attachNewNode("plane")
        self.planeFromObject = self.planeNode.attachNewNode(CollisionNode("planeColNode"))
        self.planeFromObject.node().addSolid(CollisionPlane(Plane(Vec3(0,-1,0),Point3(0,0,0))))
        ######

        def mouse1(mw):
            mpos = mw.node().getMouse()
            self.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY())
            self.cTrav.traverse(self.golog.render)
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
                faces = tuple([self.golog.NPtoSimplex[faceGr] for faceGr in self.selected[-1:-3:-1]])
                self.golog.createMorphism(faces) #reversed selected objects and creates a 1 - simplex from them

        def space(mw):
            if not mw.node().hasMouse(): return
            mpos = mw.node().getMouse()
            self.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY())
            self.cTrav.traverse(self.golog.render)
            self.queue.sortEntries()
            entry = self.queue.getEntry(0)#.getIntoNodePath().getParent

            if entry.getIntoNodePath().getParent() != self.planeNode: simplex = self.golog.NPtoSimplex[entry.getIntoNodePath().getParent()]
            else: return

            if isinstance(simplex,hcat.Simplex):
                if simplex.mathData:
                    print('Simplex has Math Data!')
                    if isinstance(simplex.mathData,golog.golog):
                        print('Math Data is a golog!')
                else:
                    newgolog = golog.golog(self.base, label = simplex.label+"_subgolog")
                    controllable_golog = mode_head(self.base, newgolog)
                    window_manager.gologToWindow(self.base, controllable_golog.golog)
            # subgolog =

        def mouse3(mw):

            mpos = mw.node().getMouse()
            self.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY())
            self.cTrav.traverse(self.golog.render)
            self.queue.sortEntries()
            entry = self.queue.getEntry(0)
            if entry.getIntoNodePath().getParent() == self.planeNode:
                for node in self.selected: node.setColorScale(1,1,1,1) #turn white
                self.selected = []
                self.golog.createObject(setPos = entry.getSurfacePoint(entry.getIntoNodePath()),
                                label = str(len(self.golog.sSet.rawSimps)))

        self.buttons = {'mouse1':mouse1,'mouse3':mouse3, 'space':space}
        # base.accept(self.golog.label+"_mouse1",self.mouse1) #make
        # base.accept(self.golog.label+"_space",self.space)
        # base.accept(self.golog.label+"_mouse3",self.mouse3)



class selection_and_creation_mode():
    def __init__(self, base, golog = None, *args,**kwargs):
        self.base = base
        self.buttons = {'mouse1':self.mouse1,'mouse3':self.mouse3, 'space':self.space}


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
        else: return

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
