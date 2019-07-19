from math import pi, sin, cos, floor

import sys, os
import hcat
import tkinter
from direct.showutil.Rope import Rope
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath, Camera
from panda3d.core import Vec3, Point3, LPoint3f, Plane
from panda3d.core import CollisionPlane, CollisionRay, CollisionSphere
from panda3d.core import CollisionNode, CollisionTraverser, CollisionHandlerQueue


#golog is an extension to a simplicial set that provides graphics functionality via the panda3d library
#The main object is a Graphics_Data, A graphics data is a subset of a panda3d scenegraph with some messenger functionality
#explicitly: a golog is a panda scene graph and an hcat sSet with a mapping from Graphics Data to Simplecies

Camera_Distance = 100

#A Graphics Data Houses panda3d information for a simplex
# Any Nodes the simplex might have
# Any Extra graphics objects (for example ropes for 1-simplecies or planes for 2-simplecies)
# Lists of children and parents
# A messenger to handle any calls to children and from parent
# keeps a list of graphics_kwargs to recreate itself (used in gexport)
class Graphics_Data():
    def __init__(self, golog, simplex, **kwargs):
        self.simplex = simplex
        self.golog = golog
        self.messenger = self.golog.base.messenger
        self.listener = DirectObject() # might let Graphics_Data Inherit from Direct_Object
        self.graphics_kwargs = dict() # keeping track of information needed to re-create graphics_data

        if simplex.level == 0:
            self.NP = golog.render.attachNewNode(simplex.label)
            self.NP.setTag('level','0') # to tell mode_heads what type of simplex this is
            golog.sphere.instanceTo(self.NP)
            self.collision = self.NP.attachNewNode(CollisionNode('sphereColNode'))
            self.collision.node().addSolid(CollisionSphere(0,0,0,1))
            self.messenger_names = {'node':str(id(self.NP))}
            golog.Simplex_to_Graphics[simplex] = self
            golog.Graphics_to_Simplex[self] = simplex
            golog.NP_to_Graphics[self.NP] = self


            #detail parents
            self.parents = () #need to give no parents for a unified update function

            self.parent_pos_convolution = lambda *x: golog.render.getPos() # function of parent's [node] positions to detail offset (0-simlex it's just render location)
            #listener for parental updates, pass arguemnts through extraKwargs to detail what kind of update to perform
            for parent in self.parents: self.listener.accept(self.parents.messenger_names['node'],self.update)
            if 'pos' in kwargs.keys():
                # print(kwargs)
                self.update({'pos':kwargs['pos']})

        elif simplex.level == 1:
            self.NP = golog.render.attachNewNode(simplex.label)
            self.NP.setTag('level','1')
            golog.cone.instanceTo(self.NP)
            self.collision = self.NP.attachNewNode(CollisionNode('coneColNode'))
            self.collision.node().addSolid(CollisionSphere(0,0,0,1))
            self.messenger_names = {'node':str(id(simplex))}
            self.graphics = Rope()

            golog.Simplex_to_Graphics[simplex] = self
            golog.Graphics_to_Simplex[self] = simplex
            golog.NP_to_Graphics[self.NP] = self


            #set up parents
            self.parents = tuple(golog.Simplex_to_Graphics[face] for face in self.simplex.faces)
            def tuple_avg(tuples):
                b = LPoint3f(0,0,0)
                for a in tuples:
                    # print(a)
                    b = b+a
                return b/len(tuples)
            self.parent_pos_convolution = tuple_avg
            for parent in self.parents: self.listener.accept(parent.messenger_names['node'],self.update)
            if 'pos' in kwargs.keys(): pos = kwargs['pos']
            else: pos = (0,0,0)
            self.update({'pos':pos})

            #set up rope graphics
            self.graphics.setup(3,[(self.parents[1].NP,(0,0,0)), (self.NP,(0,0,0)), (self.parents[0].NP,(0,0,0))])
            self.graphics.reparentTo(golog.render)
            # print([self.parents[1].NP.getPos(), self.NP.getPos(), self.parents[0].NP.getPos()])


    #listener calls update with some data
    def update(self,kwargs):
            if 'pos' in kwargs:
                self.graphics_kwargs['pos'] = kwargs['pos']
                poslist = tuple(parent.NP.getPos() for parent in self.parents)
                # print(poslist)
                newpos = self.parent_pos_convolution(poslist) + kwargs['pos'] #set a new offset base on parent positions
                # print(newpos)
                self.NP.setPos(newpos)
                self.messenger.send(self.messenger_names['node'], [{'pos':self.NP.getPos()}])

    #supress attribute errors
    def __getattr__(self, attr):
        # print('graphics_data for '+str(self.simplex.level)+'-simplex has no panda3d object ' + attr)
        return None



#a golog is essentially just a sSet with a bijection from graphics data to simplecies
#Golog = ( sSet, {Graphics_Data}, Simplex_to_Graphics = Graphics_to_Simplex^(-1) )
class golog():
    def __init__(self,base,*args, label = 'golog', **kwargs):
        self.base = base

        #initialize with an empty nodepath and no window
        #initialize a golog with no relative path (shouldn't be able to open files without one though)
        defaults = {'render':'NodePath(label+\"_render\")','abs_path':'None'}
        for key in defaults:
            if key in kwargs: setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

        self.Simplex_to_Graphics = dict()
        self.Graphics_to_Simplex = dict()
        self.NP_to_Graphics = dict()
        # Initialize simplicial set
        self.label = label
        self.sSet = hcat.simpSet(label = self.label, data = {'node':self.render})
        self.sSet.simplex_to_graphics = dict()
        self.sSet.data['export_tag'] = 'golog'

        self.NPtoSimplex = dict()


        # set up camera
        self.camNode = Camera(label+"camNode")
        self.camera = self.render.attachNewNode(self.camNode)
        self.camera.setPos(0,-Camera_Distance,0)





        # Load Models
        self.sphere = base.loader.loadModel("./models/sphere.egg.pz")
        self.cone = base.loader.loadModel('./models/Cone.egg')
        self.cone.setScale(.6)

        #set up collision traverser
        self.cTrav = CollisionTraverser(self.label+'_traverser')

    def add(self, ob ,*args, **kwargs):
        #add a simplex to the underlying simplicial set
        #see hcat for reference
        #ob = 0, create 0-simplex
        #ob = faces, create n-simplex (with faces)
        simplex = self.sSet.add(ob, *args, **kwargs)
        Graphics_Data(self, simplex,*args, **kwargs)

        return simplex

if __name__ == "__main__":
    from direct.showbase.ShowBase import ShowBase
    class runner(ShowBase):
        def __init__(self):
            ShowBase.__init__(self)
            self.disable_mouse()


            # need to migrate into gologToWindow
            base.accept("f5",sys.exit)
            base.accept("f6",sys.exit)


            G = golog(base, label = 'run')
            self.win.getDisplayRegion(1).setCamera(G.camera)
            a = G.add(0,label = '1')
            b = G.add(0,label = '2',pos = (0,0,10))
            G.add((b,a), label = '(1,2)')
            # print([s.label for s in G.sSet.rawSimps])
    runner().run()
