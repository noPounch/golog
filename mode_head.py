#goal of this file is to create:
#1) an export function that returns simplecies
#2) an import function that checks face conditions on simplecies
#--That The faces even exist (raise exception)
#--That they satisfy the face conditions (return in conditions string)
#--That they satisfy degeneracy conditions (return in conditions string)
from sys import exit
from math import sin,cos
from golog_export import gexport
import time
import hcat
import golog
import window_manager
from direct.showbase.DirectObject import DirectObject

from panda3d.core import Vec3, Point3
from panda3d.core import Plane, CollisionPlane, CollisionRay, CollisionNode, CollisionTraverser, CollisionHandlerQueue


class mode_head():
    def __init__(self,base,Golog):
        self.base = base
        self.golog = Golog
        self.buttons = dict()
        self.listener = DirectObject()

        #label modehead uniquely
        # make a dictionary of mode data in modes
        if hasattr(self.golog,'mode_heads'):
            m = 0
            while m in self.golog.mode_heads.keys(): m+=1 #get smallest unused mode_head index
            self.index = m
            self.label = self.golog.label+"_mode_head_"+str(self.index)
            self.golog.mode_heads[self.index] = self

        else:
            self.golog.mode_heads = dict()
            self.index = 0
            self.label = self.golog.label+"_mode_head_"+ str(self.index)
            self.golog.mode_heads[self.index] = self

        self.reset = self.basic_reset

    def basic_reset(self,*args):
        self.buttons = dict()
        self.listener.ignoreAll()

    def clean(self):
        self.reset()
        del self.golog.mode_heads[self.index]
        del self.reset





    def selection_and_creation(self):

        #Collision Handling
        #set up traverser and handler
        self.queue = CollisionHandlerQueue()
        self.selected = []
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.golog.camera.attachNewNode(self.pickerNode)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.pickerNode.set_into_collide_mask(0) #so that collision rays don't collide into each other if there are two mode_heads
        self.golog.cTrav.addCollider(self.pickerNP,self.queue)
        self.planeNode = self.golog.render.attachNewNode("plane")
        self.planeNode.setTag("mode_head",self.label)
        self.planeFromObject = self.planeNode.attachNewNode(CollisionNode("planeColNode"))
        self.planeFromObject.node().addSolid(CollisionPlane(Plane(Vec3(0,-1,0),Point3(0,0,0))))
        ######

        def mouse1(mw):
            mpos = mw.node().getMouse()
            self.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY())
            self.golog.cTrav.traverse(self.golog.render)
            self.queue.sortEntries()
            # entry = self.queue.getEntry(0)

            # get the first relevant node traversed by mouseRay
            # ignore everything with a mode_head tag that is not defined by this mode_head
            for e in self.queue.getEntries():
                if e.getIntoNodePath().getParent().hasTag("mode_head"):
                    if e.getIntoNodePath().getParent().getTag("mode_head") == self.label:
                        entry = e
                        break
                else:
                    entry = e
                    break



            if entry.getIntoNodePath().getParent().getTag("mode_head") == self.label:
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
            self.golog.cTrav.traverse(self.golog.render)
            self.queue.sortEntries()

            # get the first relevant node traversed by mouseRay
            # ignore everything with a mode_head tag that is not defined by this mode_head
            for e in self.queue.getEntries():
                if e.getIntoNodePath().getParent().hasTag("mode_head"):
                    if e.getIntoNodePath().getParent().getTag("mode_head") == self.label:
                        entry = e
                        break
                else:
                    entry = e
                    break

            if entry.getIntoNodePath().getParent() != self.planeNode: simplex = self.golog.NPtoSimplex[entry.getIntoNodePath().getParent()]
            else: return

            if isinstance(simplex,hcat.Simplex):
                if simplex.mathData:
                    print('Simplex has Math Data!')
                    if isinstance(simplex.mathData,golog.golog):
                        print('Math Data is a golog!')
                        #if it has a mode_head, just create a window to view golog (no controls), otherwise create a mode_head in selection_and_creation mode
                        controllable_golog = mode_head(self.base, simplex.mathData)
                        # if not hasattr(simplex.mathData,"mode_heads"):
                        controllable_golog.selection_and_creation()

                        window_manager.modeHeadToWindow(self.base, controllable_golog)

                else:
                    new_golog = golog.golog(self.base, label = self.golog.label+"_subgolog_at_simplex"+simplex.label)
                    controllable_golog = mode_head(self.base, new_golog)
                    controllable_golog.selection_and_creation()
                    window_manager.modeHeadToWindow(self.base, controllable_golog)
                    simplex.mathData = new_golog
            # subgolog =

        def mouse3(mw):

            mpos = mw.node().getMouse()
            self.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY())
            self.golog.cTrav.traverse(self.golog.render)
            self.queue.sortEntries()

            # get the first relevant node traversed by mouseRay
            # ignore everything with a mode_head tag that is not defined by this mode_head
            for e in self.queue.getEntries():
                if e.getIntoNodePath().getParent().hasTag("mode_head"):
                    if e.getIntoNodePath().getParent().getTag("mode_head") == self.label:
                        entry = e
                        break
                else:
                    entry = e
                    break

            if entry.getIntoNodePath().getParent() == self.planeNode:
                for node in self.selected: node.setColorScale(1,1,1,1) #turn white
                self.selected = []
                self.golog.createObject(setPos = entry.getSurfacePoint(entry.getIntoNodePath()),
                                label = str(len(self.golog.sSet.rawSimps)))


        def reset(*args):
            self.golog.cTrav.removeCollider(self.pickerNP)
            del self.queue
            for node in self.selected: node.setColorScale(1,1,1,1)
            del self.selected
            del self.pickerNode
            self.pickerNP.removeNode()
            del self.pickerRay
            self.planeNode.removeNode()
            self.planeFromObject.removeNode()
            self.buttons = dict()
            self.listener.ignoreAll()
            # print(self.label+ " reset")
            self.reset = self.basic_reset

        self.reset = reset
        self.buttons = {'mouse1':mouse1,'mouse3':mouse3, 'space':space, 'escape':self.reset}

    def testing_mode(self):

        #Collision Handling
        #set up traverser and handler
        self.queue = CollisionHandlerQueue()
        self.selected = []
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.golog.camera.attachNewNode(self.pickerNode)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.pickerNode.set_into_collide_mask(0) #so that collision rays don't collide into each other if there are two mode_heads
        self.golog.cTrav.addCollider(self.pickerNP,self.queue)
        self.planeNode = self.golog.render.attachNewNode("plane")
        self.planeNode.setTag("mode_head",self.label)
        self.planeFromObject = self.planeNode.attachNewNode(CollisionNode("planeColNode"))
        self.planeFromObject.node().addSolid(CollisionPlane(Plane(Vec3(0,-1,0),Point3(0,0,0))))
        ######

        def mouse1(mw):
            mpos = mw.node().getMouse()
            self.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY())
            self.golog.cTrav.traverse(self.golog.render)
            self.queue.sortEntries()
            # entry = self.queue.getEntry(0)

            # get the first relevant node traversed by mouseRay
            # ignore everything with a mode_head tag that is not defined by this mode_head
            for e in self.queue.getEntries():
                if e.getIntoNodePath().getParent().hasTag("mode_head"):
                    if e.getIntoNodePath().getParent().getTag("mode_head") == self.label:
                        entry = e
                        break
                else:
                    entry = e
                    break



            if entry.getIntoNodePath().getParent() == self.planeNode:
                for node in self.selected: node.setColorScale(1,1,1,1) #turn white
                self.selected = []
            else:
                if entry.getIntoNodePath().getParent() not in self.selected:
                    self.selected.append(entry.getIntoNodePath().getParent())#.getTag('simplex'))
                print(entry.getIntoNodePath().getParent())
                entry.getIntoNodePath().getParent().setColorScale(1,0,0,0) #turn red
                origpos = entry.getIntoNodePath().getParent().getPos()
                node = entry.getIntoNodePath().getParent()
                base.taskMgr.add(test_moving,'move test',extraArgs = [node,origpos], appendTask=True)


            if len(self.selected) >= 2:
                faces = tuple([self.golog.NPtoSimplex[faceGr] for faceGr in self.selected[-1:-3:-1]])
                self.golog.createMorphism(faces) #reversed selected objects and creates a 1 - simplex from them


        def space(mw):
            if not mw.node().hasMouse(): return
            mpos = mw.node().getMouse()
            self.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY())
            self.golog.cTrav.traverse(self.golog.render)
            self.queue.sortEntries()

            # get the first relevant node traversed by mouseRay
            # ignore everything with a mode_head tag that is not defined by this mode_head
            for e in self.queue.getEntries():
                if e.getIntoNodePath().getParent().hasTag("mode_head"):
                    if e.getIntoNodePath().getParent().getTag("mode_head") == self.label:
                        entry = e
                        break
                else:
                    entry = e
                    break

            if entry.getIntoNodePath().getParent() != self.planeNode: simplex = self.golog.NPtoSimplex[entry.getIntoNodePath().getParent()]
            else: return

            if isinstance(simplex,hcat.Simplex):
                if simplex.mathData:
                    print('Simplex has Math Data of type {}'.format(str(type(simplex.mathData))))
                    if isinstance(simplex.mathData,golog.golog):
                        print('Math Data is a golog!')
                        #if it has a mode_head, just create a window to view golog (no controls), otherwise create a mode_head in selection_and_creation mode
                        controllable_golog = mode_head(self.base, simplex.mathData)
                        # if not hasattr(simplex.mathData,"mode_heads"):
                        controllable_golog.selection_and_creation()

                        window_manager.modeHeadToWindow(self.base, controllable_golog)

                else:
                    new_golog = golog.golog(self.base, label = self.golog.label+"_subgolog_at_simplex"+simplex.label)
                    controllable_golog = mode_head(self.base, new_golog)
                    controllable_golog.selection_and_creation()
                    window_manager.modeHeadToWindow(self.base, controllable_golog)
                    simplex.mathData = new_golog
            # subgolog =

        def mouse3(mw):

            mpos = mw.node().getMouse()
            self.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY())
            self.golog.cTrav.traverse(self.golog.render)
            self.queue.sortEntries()

            # get the first relevant node traversed by mouseRay
            # ignore everything with a mode_head tag that is not defined by this mode_head
            for e in self.queue.getEntries():
                if e.getIntoNodePath().getParent().hasTag("mode_head"):
                    if e.getIntoNodePath().getParent().getTag("mode_head") == self.label:
                        entry = e
                        break
                else:
                    entry = e
                    break

            if entry.getIntoNodePath().getParent() == self.planeNode:
                for node in self.selected: node.setColorScale(1,1,1,1) #turn white
                self.selected = []
                self.golog.createObject(setPos = entry.getSurfacePoint(entry.getIntoNodePath()),
                                label = str(len(self.golog.sSet.rawSimps)))


        def save(mw):
            filename = "test.golog"
            file_location = 'save/'+filename
            gexport(self.golog, file_location)


        def test_moving(node, origpos, task):
            t = task.time
            pos = origpos + Point3(1/3*sin(t*10),0,1/3*cos(t*10))
            self.golog.updateSimp(node, kwargs = {'pos':pos})
            return task.cont


        def reset(*args):
            self.golog.cTrav.removeCollider(self.pickerNP)
            del self.queue
            for node in self.selected: node.setColorScale(1,1,1,1)
            del self.selected
            del self.pickerNode
            self.pickerNP.removeNode()
            del self.pickerRay
            self.planeNode.removeNode()
            self.planeFromObject.removeNode()
            self.buttons = dict()
            self.listener.ignoreAll()
            # print(self.label+ " reset")
            self.reset = self.basic_reset

        self.reset = reset
        self.buttons = {'mouse1':mouse1,'mouse3':mouse3, 'space':space, 'escape':self.reset,'s':save}

    def viewing_mode(self):
        self.reset()
