from math import pi, sin, cos, floor

import sys
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
#explicitly: a golog is a panda scene graph and an hcat sSet with a mapping from Panda Nodes to Simplecies

Camera_Distance = 100

# messenger = DirectObject()

class golog():
    def __init__(self,base,*args, label = 'golog', **kwargs):
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
        self.sphere = loader.loadModel("models/misc/sphere")

        #set up collision traverser
        self.cTrav = CollisionTraverser(self.label+'_traverser')


    def createObject(self, *args, **kwargs):
        #create a simplex in the simplicial set
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
