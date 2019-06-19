from math import pi, sin, cos, floor

import sys
import hcat
import tkinter
from direct.showutil.Rope import Rope
from direct.task import Task
from panda3d.core import NodePath, Camera
from panda3d.core import Vec3, Point3, LPoint3f, Plane
from panda3d.core import CollisionPlane, CollisionRay, CollisionSphere
from panda3d.core import CollisionNode, CollisionTraverser, CollisionHandlerQueue


#golog is an extension to a simplicial set that provides graphics functionality via the panda3d library
#explicitly: a golog is a panda scene graph and an hcat sSet with a mapping from Panda Nodes to Simplecies

Camera_Distance = 100

class golog():
    def __init__(self,base ,*args, label = 'golog', **kwargs):
        #initialize with an empty nodepath and no window
        defaults = {'render':NodePath(label+"_render")}
        for key in defaults:
            if key in kwargs: setattr(self,key,kwargs[key])
            else: setattr(self,key,defaults[key])

        # set up camera
        self.camNode = Camera(label+"camNode")
        self.camera = self.render.attachNewNode(self.camNode)
        self.camera.setPos(0,-Camera_Distance,0)


        # Initialize simplicial set
        self.label = label
        self.sSet = hcat.simpSet(self.label, data = {'node':self.render})
        self.NPtoSimplex = dict()


        # Load Models
        self.sphere = base.loader.loadModel("models/misc/sphere")

        #set up collision traverser
        self.cTrav = CollisionTraverser(self.label+'_traverser')


    def createObject(self, *args, **kwargs):
        #create a simplex in the simplicial set
        simplex = self.sSet.add(0,*args, **kwargs)

        #create an instance of simplex graphics in golog, send to simplex.data['node']
        simplexGr = self.render.attachNewNode(simplex.label+" Node")
        simplex.data['node'] = simplexGr #refer to node from simplex
        self.NPtoSimplex[simplexGr] = simplex #refer to simplex from node

        #attach sphere graphics and sphere collision node to node
        self.sphere.instanceTo(simplexGr)
        collisionNode = simplexGr.attachNewNode(CollisionNode('sphereColNode'))
        collisionNode.node().addSolid(CollisionSphere(0,0,0,1))

        #create a messenger name for simplex (for now just rawSimps index)
        simplex.data['_messengerName'] = 'simp' + str(self.sSet.rawSimps.index(simplex))

        defaults = {'setPos':(0,0,0)}
        for key in defaults.keys():
            if key in kwargs.keys(): getattr(simplexGr,key)(kwargs[key])
            else: getattr(simplexGr,key)(defaults[key])

        #accept other calls
        base.accept('Update' + simplex.data['_messengerName'], self.updateSimp, extraArgs = [simplex])

        return simplex

    def updateSimp(self,simp,kwargs = dict()):
        if 'pos' in kwargs:
            #update morphism to be average position of it's faces nodes + some offset passed through kwargs['pos']
            pos = kwargs['pos']
            n = len(simp.faces)
            for f in simp.faces: pos = pos + f.data['node'].getPos()/n #transform offset pos to offset from average of faces
            simp.data['node'].setPos(pos)
            base.messenger.send( simp.data['_messengerName']+' moved', extraArgs = [{'pos':Point3(0,0,0)}]) #sending (0,0,0) just updates the child nodes by default

    def createMorphism(self, faces, *args, **kwargs):
        dom = faces[1]; codom = faces[0]
        simplex = self.sSet.add(faces,*args,**kwargs)
        simplex.data['_messengerName'] = 'simp' + str(self.sSet.rawSimps.index(simplex))
        # offset for middlenode



        rope = Rope()
        middlenode = self.render.attachNewNode("middlenode")
        simplex.data['node'] = middlenode
        middlenode.setPos((dom.data['node'].getPos()+codom.data['node'].getPos())/2)


        #create a middlenode listener for face movements
        ######
        for f in simplex.faces: base.accept(f.data['_messengerName'] + ' moved',self.updateSimp,extraArgs = [simplex])
        #####

        #create a listener for other events
        #####
        base.accept('Update' + simplex.data['_messengerName'],self.updateSimp,extraArgs = [simplex])
        #####

        #set start and endpoint to be the domain and codomain graphics
        rope.setup(3,[(dom.data['node'],(0,0,0)),
                    (simplex.data['node'],(0,0,0)),
                    (codom.data['node'],(0,0,0))])
        rope.reparentTo(self.render)
        simplex.data['graphics'] = rope #simplex to Graphics
        self.NPtoSimplex[rope] = simplex #graphics to simplex


        return simplex
