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

#Golog is a wrapper for a panda scenegraph and a hcat, it can be placed into a window by
#win.getDisplayRegion(0).setCamera(golog.camera)

Camera_Distance = 100

class golog():
    def __init__(self,base ,*args, label = 'golog', **kwargs):
        #initialize with an empty nodepath and no window
        defaults = {'render':NodePath(label+"_render")}
        for key in defaults:
            if key in kwargs: setattr(self,key,kwargs[key])
            else: setattr(self,key,defaults[key])

        #window stuff
        # self.render = NodePath(label+"_render")
        self.windicts = []
        self.buttons = dict()
        # self.buttons = {'mouse1':self.mouse1,'mouse3':self.mouse3}
        self.camNode = Camera(label+"camNode")
        self.camera = self.render.attachNewNode(self.camNode)
        self.camera.setPos(0,-Camera_Distance,0)

        # Initialize simplicial set
        self.label = label
        self.sSet = hcat.simpSet(self.label, data = {'node':self.render})
        # Load Models
        self.sphere = base.loader.loadModel("models/misc/sphere")

        #Collision Handling
        #set up traverser and handler
        self.cTrav = CollisionTraverser('main traverser')
        self.queue = CollisionHandlerQueue()
        self.selected = []

        #set up ray picker
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.camera.attachNewNode(self.pickerNode)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)

        #traverser sends ray collisions to handler
        self.cTrav.addCollider(self.pickerNP,self.queue)

        #set up CollisionPlane
        self.planeNode = self.render.attachNewNode("plane")
        self.planeFromObject = self.planeNode.attachNewNode(CollisionNode("planeColNode"))
        self.planeFromObject.node().addSolid(CollisionPlane(Plane(Vec3(0,-1,0),Point3(0,0,0))))

        self.NPtoSimplex = dict()


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
        #simplexGr.ls()
        #accept other calls
        ####
        base.accept('Update' + simplex.data['_messengerName'],self.updateSimp,[simplex])
        ####
        return simplex

    def updateSimp(self,simp,kwargs = dict()):
        if 'pos' in kwargs:
            #update morphism to be average position of it's faces nodes + some offset passed through kwargs['pos']
            pos = kwargs['pos']
            n = len(simp.faces)
            for f in simp.faces: pos = pos + f.data['node'].getPos()/n #transform offset pos to offset from average of faces
            simp.data['node'].setPos(pos)
            base.messenger.send( simp.data['_messengerName']+' moved', [{'pos':Point3(0,0,0)}]) #sending (0,0,0) just updates the child nodes by default

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
        for f in simplex.faces: base.accept(f.data['_messengerName'] + ' moved',self.updateSimp,[simplex])
        #####

        #create a listener for other events
        #####
        base.accept('Update' + simplex.data['_messengerName'],self.updateSimp,[simplex])
        #####

        #set start and endpoint to be the domain and codomain graphics
        rope.setup(3,[(dom.data['node'],(0,0,0)),
                    (simplex.data['node'],(0,0,0)),
                    (codom.data['node'],(0,0,0))])
        rope.reparentTo(self.render)
        simplex.data['graphics'] = rope #simplex to Graphics
        self.NPtoSimplex[rope] = simplex #graphics to simplex


        return simplex

    def simpMoverTask(self,simp,orig,task):
        t = task.time
        curve = lambda t: Point3(sin(10*t),sin(10*t),sin(10*t))
        self.updateSimp(simp, {'pos' : orig + curve(t)})
        return task.cont


    # def cameraTask(self, task):
    #     t = task.time
    #     base.camera.setPos(50*cos(t),50*sin(t),50*sin(t))
    #     base.camera.lookAt(self.sSet.rawSimps[0].data['graphics'])
    #     return task.cont
