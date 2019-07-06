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
# A messenger to handle any calls to children and from parents
class Graphics_Data():
    def __init__(self, simplex, golog, **kwargs):
        self.simplex = simplex
        self.golog = golog
        if simplex.level = 0:
            self.NP = golog.render.attachNewNode(NodePath(simplex.label))
            golog.sphere.instanceTo(self.NP)
            self.messenger = DirectObject() # might let Graphics_Data Inherit from Direct_Object
            self.collision = self.NP.attachNewNode(CollisionNode('sphereColNode'))
            self.collision.node().addSolid(CollisionSphere(0,0,0,1))
            self.messenger_names = {'node':str(id(self.NP))}
            golog.Simplex_to_Graphics[simplex] = self
            golog.Graphics_to_Simplex[self] = simplex

            #detail parents
            self.parents = () #need to give no parents for a unified update function
            if 'pos' in kwargs.keys(): self.NP.setPos(kwargs['pos'])
            self.parent_pos_convolution = lambda *x: golog.render.getPos() # function of parent's [node] positions to detail offset (0-simlex it's just render location)
            #listener for parental updates, pass arguemnts through extraKwargs to detail what kind of update to perform
            for parent in self.parents: self.messenger.accept(self.parents.messenger_names['node'],self.update)

        elif simplex.level = 1:
            self.NP = golog.render.attachNewNode(NodePath(simplex.label))
            golog.cone.instanceTo(self.NP)
            self.messenger = DirectObject()
            self.graphics = Rope()

            golog.Simplex_to_Graphics[simplex] = self
            golog.Graphics_to_Simplex[self] = simplex


            #set up parents
            self.parents = tuple(golog.Simplex_to_Graphics[face] for face in self.simplex.faces)
            self.parent_pos_convolution = lambda x:average(x)




            self.sSet.simplex_to_graphics[simplex] = dict()

            # offset for middlenode




            middlenode.setPos((domNode.getPos()+codomNode.getPos())/2)

            middlenode.setTag('_messengerName', str(id(simplex)))

            #create a middlenode listener for face movements
            ######
            for f in simplex.faces:
                fNode = self.sSet.simplex_to_graphics[f]['node']
                listener.accept(fNode.getTag('_messengerName') + ' moved',self.updateSimp, extraArgs = [middlenode])
            #####

            #create a listener for other events
            #####
            listener.accept('Update' + middlenode.getTag('_messengerName'), self.updateSimp, extraArgs = [middlenode])
            #####

            #set start and endpoint to be the domain and codomain graphics
            rope.setup(3,[(domNode,(0,0,0)),
                        (middlenode,(0,0,0)),
                        (codomNode,(0,0,0))])
            rope.reparentTo(self.render)
            self.sSet.simplex_to_graphics[simplex]['model'] = 'rope' #simplex to Graphics


    #listener calls update with some data
    def update(kwargs):
            if 'pos' in kwargs:
                newpos = self.parent_pos_convolution(tuple(parent.NP.getPos())) + kwargs['pos'] #set a new offset base on parent positions
                self.NP.setPos(newpos)
                self.messenger.send(self.messenger_names['node'], extraArgs = [{pos:self.NP.getPos()}])

    #supress attribute errors
    def __getattr__(self, attr):
        print('graphics_data for '+str(self.simplex.level)+'-simplex has no panda3d object ' + attr)
        return None



#a golog is essentially just a sSet with a bijection from graphics data to simplecies
#Golog = ( sSet, {Graphics_Data}, Simplex_to_Graphics = Graphics_to_Simplex^(-1) )
class golog():
    def __init__(self,base,*args, label = 'golog', **kwargs):
        self.base = base

        #initialize with an empty nodepath and no window
        defaults = {'render':NodePath(label+"_render")}
        for key in defaults:
            if key in kwargs: setattr(self,key,kwargs[key])
            else: setattr(self,key,defaults[key])

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
        self.sphere = base.loader.loadModel("models/misc/sphere")
        self.tetra = base.loader.loadModel(os.path.abspath(os.path.dirname(__file__))+'/models/Tetrahedron.egg')

        #set up collision traverser
        self.cTrav = CollisionTraverser(self.label+'_traverser')

    def createObject(self, *args, **kwargs):
        #create a 0-simplex in the simplicial set
        simplex = self.sSet.add(0,*args, **kwargs)
        self.sSet.simplex_to_graphics[simplex] = dict()

        #create an instance of simplex graphics in golog, send to simplex.data['node']
        node = self.render.attachNewNode(simplex.label+" Node")

        #create a direct object to listen for update events (instead of using showbase messenger)
        #this will allow for more fine-tuned control with how a node-path accepts calls
        listener = DirectObject()

        self.sSet.simplex_to_graphics[simplex]['node'] = node #refer to node in attached graphics data from simplex
        self.sSet.simplex_to_graphics[simplex]['listener'] = listener #refer to listener in attached graphics data from simplex
        self.sSet.simplex_to_graphics[simplex]['model'] = 'sphere'
        self.NPtoSimplex[node] = simplex #refer to simplex from node

        #attach sphere graphics and sphere collision node to node
        self.sphere.instanceTo(node)
        collisionNode = node.attachNewNode(CollisionNode('sphereColNode'))
        collisionNode.node().addSolid(CollisionSphere(0,0,0,1))

        #reference name for node events is the memory identity of the simplex
        #(**) this might be an issue if multiple gologs share a simplex, but since golog instanciation is done with a fresh sSet, this probably won't happen
        node.setTag('_messengerName', str(id(simplex)))

        defaults = {'setPos':(0,0,0)}
        for key in defaults.keys():
            if key in kwargs.keys(): getattr(node, key)(kwargs[key])
            else: getattr(node, key)(defaults[key])

        #accept other calls
        listener.accept('Update' + node.getTag('_messengerName'), self.updateSimp, extraArgs = [node])

        return simplex

    def updateSimp(self,node,kwargs = dict()):
        simp = self.NPtoSimplex[node]
        if 'pos' in kwargs:
            #update morphism to be average position of it's faces nodes + some offset passed through kwargs['pos']
            pos = kwargs['pos']
            n = len(simp.faces)
            for simplex in simp.faces: pos = pos + self.sSet.simplex_to_graphics[simplex]['node'].getPos()/n #transform offset pos to offset from average of faces
            self.sSet.simplex_to_graphics[simp]['node'].setPos(pos)
            base.messenger.send(node.getTag('_messengerName')+' moved', [{'pos':Point3(0,0,0)}]) #sending (0,0,0) just updates the child nodes by default

    def createMorphism(self, faces, *args, **kwargs):
        dom = faces[1]; codom = faces[0]
        simplex = self.sSet.add(faces,*args,**kwargs)
        self.sSet.simplex_to_graphics[simplex] = dict()

        domNode = self.sSet.simplex_to_graphics[dom]['node']
        codomNode = self.sSet.simplex_to_graphics[codom]['node']


        # offset for middlenode



        rope = Rope()
        middlenode = self.render.attachNewNode(simplex.label+" middle_node")
        self.tetra.instanceTo(middlenode)
        listener = DirectObject()
        self.sSet.simplex_to_graphics[simplex]['listener'] = listener
        self.sSet.simplex_to_graphics[simplex]['node'] = middlenode
        self.NPtoSimplex[middlenode] = simplex #graphics to simplex
        middlenode.setPos((domNode.getPos()+codomNode.getPos())/2)

        middlenode.setTag('_messengerName', str(id(simplex)))

        #create a middlenode listener for face movements
        ######
        for f in simplex.faces:
            fNode = self.sSet.simplex_to_graphics[f]['node']
            listener.accept(fNode.getTag('_messengerName') + ' moved',self.updateSimp, extraArgs = [middlenode])
        #####

        #create a listener for other events
        #####
        listener.accept('Update' + middlenode.getTag('_messengerName'), self.updateSimp, extraArgs = [middlenode])
        #####

        #set start and endpoint to be the domain and codomain graphics
        rope.setup(3,[(domNode,(0,0,0)),
                    (middlenode,(0,0,0)),
                    (codomNode,(0,0,0))])
        rope.reparentTo(self.render)
        self.sSet.simplex_to_graphics[simplex]['model'] = 'rope' #simplex to Graphics



        return simplex
