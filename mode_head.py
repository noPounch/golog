#goal of this file is to create:
#1) an export function that returns simplecies
#2) an import function that checks face conditions on simplecies
#--That The faces even exist (raise exception)
#--That they satisfy the face conditions (return in conditions string)
#--That they satisfy degeneracy conditions (return in conditions string)
from sys import exit
import os
from math import sin,cos
from golog_export import gexport
import time
import hcat
import golog
import window_manager
import tk_funcs
from direct.showbase.DirectObject import DirectObject
from panda3d.core import TextNode, TextFont
from panda3d.core import Camera, NodePath, OrthographicLens
from panda3d.core import Vec3, Point3
from panda3d.core import Plane, CollisionPlane, CollisionRay, CollisionNode, CollisionTraverser, CollisionHandlerQueue

#functionality for updating a simplex's math_data

def open_math_data(math_data):
    if math_data.type == 'golog':
        base = math_data().base
        controllable_golog = mode_head(base, math_data())
        controllable_golog.selection_and_creation()
        window_manager.modeHeadToWindow(base, controllable_golog)
    if math_data.type == 'file':
        file_name, file_extension = os.path.splitext(math_data())
        print(file_name, file_extension)
        if file_extension == '.txt':
            tk_funcs.edit_txt(math_data())
        else:
            #prompt user to select a program
            tk_funcs.run_program('',math_data())


def update_math_data(simplex, math_data_type, **kwargs):
    if 'label' in kwargs: simplex.label = kwargs['label']

    if math_data_type == 'None':
        simplex.math_data = hcat.Math_Data()

    if math_data_type == 'golog':
        new_golog = golog.golog(kwargs['base'], label = kwargs['label']) #create a new golog
        def newopen(): #create an open function for the golog math data
            controllable_golog = mode_head(kwargs['base'], simplex.math_data())
            controllable_golog.selection_and_creation()
            window_manager.modeHeadToWindow(kwargs['base'], controllable_golog)
        simplex.math_data = hcat.Math_Data(math_data = new_golog, type = 'golog')

    if math_data_type == 'file':
        file_location = tk_funcs.ask_file_location()
        if not file_location: return #if user cancels
        file_name, file_extension = os.path.splitext(file_location)
        simplex.math_data = hcat.Math_Data(math_data = file_location, type = 'file')

        # room for more extensions


    return simplex.math_data



class mode_head():
    def __init__(self,base,Golog, save_location = 'save/test.golog'):
        self.base = base
        self.golog = Golog
        self.buttons = dict()
        self.window_tasks = []
        self.listener = DirectObject()
        self.save_location = save_location

        #create a 2d render
        self.render2d = NodePath('2d render')
        self.camera2D = self.render2d.attachNewNode(Camera('2d Camera'))
        self.camera2D.setDepthTest(False)
        self.camera2D.setDepthWrite(False)
        lens = OrthographicLens()
        lens.setFilmSize(2, 2)
        lens.setNearFar(-1000, 1000)
        self.camera2D.node().setLens(lens)

        #label modehead uniquely
        # make a dictionary of mode_heads in the underlying golog
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

        #if mode_head reset function, should be set at the end of every mode
        self.reset = self.basic_reset

    #basic reset functionality
    def basic_reset(self,*args):
        self.buttons = dict()
        self.window_tasks = dict()
        self.listener.ignoreAll()

    #cleans mode_head to preparte for garbage collecting.
    def clean(self):
        self.reset()
        del self.golog.mode_heads[self.index]
        del self.reset




    #basic mode for selecting and creating simplecies
    #controls
    #mouse_over: display label and mata_data_type
    #left click: select simplex.
    #selecting two 0-simplecies creates a 1-simplex
    #right click: create simplex
    #dialog box pops up prompting for default labels and math_data
    #space with mouse over simplex: open math_data
    #s saves golog to a .golog file (using hcat_funcs.gexport)
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

        #text node for displaying simplex math_data meta data
        self.textNP = self.render2d.attachNewNode(TextNode('text node'))
        self.textNP.setScale(.1)
        self.textNP.setPos(-1+.2,0,-1+.2)

        # ###
        # self.textNP.node().setText('hello')
        # self.textNP.setPos(0,0,0)
        #
        # ###


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
                # if simplex has actual math_data
                if not simplex.math_data():
                    print('simplex has no math data')
                    (label, math_data_type) = tk_funcs.ask_math_type()
                    update_math_data(simplex, math_data_type, base= self.base, label = label)
                    # open_math_data(simplex.math_data)
                    #for future asynchronounisity
                    #self.base.taskMgr.add(open_math_data,'asynch open task', extraArgs = [simplex.math_data])

                else:
                    open_math_data(simplex.math_data)
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
                (label, math_data_type) =  tk_funcs.ask_simplex_data() #ask for simplex data
                simplex = self.golog.createObject(setPos = entry.getSurfacePoint(entry.getIntoNodePath()), label = label) #create a simplex
                update_math_data(simplex, math_data_type, base = self.base, label = label)
                # open_math_data(simplex.math_data)


        def mouse_watch_test(mw,task):

            if not mw.node().hasMouse(): return task.cont
            mpos = mw.node().getMouse()
            self.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY())
            self.golog.cTrav.traverse(self.golog.render)
            if not self.queue.sortEntries: return task.cont # if collision traverser doesn't pick anything up, return
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

            if entry.getIntoNodePath().getParent() != self.planeNode:
                simplex = self.golog.NPtoSimplex[entry.getIntoNodePath().getParent()]
            else:
                self.textNP.hide()
                return task.cont

            self.textNP.show()
            self.textNP.node().setText("label: " +simplex.label+"\n math data type: " + simplex.math_data.type)
            # self.textNP.setPos(mpos.getX(),0,mpos.getY())
            return task.cont

        def save(mw):
            print(os.path.abspath(os.path.dirname(__file__))+'/'+self.save_location)
            save_location = tk_funcs.ask_file_location(initial_dir = os.path.abspath(os.path.dirname(__file__))+'/'+self.save_location)
            gexport(self.golog, save_location)


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
            self.window_tasks = []
            self.listener.ignoreAll()
            # print(self.label+ " reset")
            self.reset = self.basic_reset

        self.reset = reset
        self.buttons = {'mouse1':mouse1,'mouse3':mouse3, 'space':space, 'escape':self.reset, 's':save}
        self.window_tasks = [mouse_watch_test]

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
                # base.taskMgr.add(test_moving,'move test',extraArgs = [node,origpos], appendTask=True)


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
                if simplex.math_data:
                    print('Simplex has Math Data of type {}'.format(str(type(simplex.math_data))))
                    if isinstance(simplex.math_data,golog.golog):
                        print('Math Data is a golog!')
                        #if it has a mode_head, just create a window to view golog (no controls), otherwise create a mode_head in selection_and_creation mode
                        controllable_golog = mode_head(self.base, simplex.math_data)
                        # if not hasattr(simplex.math_data,"mode_heads"):
                        controllable_golog.selection_and_creation()

                        window_manager.modeHeadToWindow(self.base, controllable_golog)

                else:
                    new_golog = golog.golog(self.base, label = self.golog.label+"_subgolog_at_simplex"+simplex.label)
                    controllable_golog = mode_head(self.base, new_golog)
                    controllable_golog.selection_and_creation()
                    window_manager.modeHeadToWindow(self.base, controllable_golog)
                    simplex.math_data = new_golog
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

        def display_info(mw):
            #display high level info about a simplex (e.g. math_data type, label)
            pass



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
