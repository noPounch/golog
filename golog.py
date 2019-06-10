from math import pi, sin, cos, floor

import sys
import hcat
import tkinter
from direct.showutil.Rope import Rope
from direct.task import Task
from panda3d.core import Vec3, Point3, LPoint3f, Plane
from panda3d.core import CollisionPlane, CollisionRay, CollisionSphere
from panda3d.core import CollisionNode, CollisionTraverser, CollisionHandlerQueue

class golog():
    def __init__(self,base ,*args, label = 'golog', **kwargs):
        #set up showbase and debugging options
        defaults = {'render':base.render, 'camera':base.camera,'camNode':base.camNode,'loader':base.loader}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,defaults[key])



        # Initialize simplicial set
        self.gologNode = self.render.attachNewNode(label)
        self.sSet = hcat.simpSet(label = "golog", data = {'node':self.gologNode})

        # Load Models
        self.sphere = self.loader.loadModel("models/misc/sphere")

        #Collision Handling
        #set up traverser and handler
        self.cTrav = CollisionTraverser('main traverser')
        self.queue = CollisionHandlerQueue()
        self.selected = []

        #set up ray picker
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.camNode.attachNewNode(self.pickerNode)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)

        #traverser sends ray collisions to handler
        self.cTrav.addCollider(self.pickerNP,self.queue)

        #set up CollisionPlane
        self.planeNode = self.gologNode.attachNewNode("plane")
        self.planeFromObject = self.planeNode.attachNewNode(CollisionNode("planeColNode"))
        self.planeFromObject.node().addSolid(CollisionPlane(Plane(Vec3(0,-1,0),Point3(0,0,0))))

        self.graphicsToSimplex = dict()



        base.accept("mouse1",self.mouse1)
        base.accept("mouse3",self.mouse3)



    def mouse1(self):
        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode,mpos.getX(),mpos.getY())
        self.cTrav.traverse(base.render)
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


    def mouse3(self):
        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode,mpos.getX(),mpos.getY())
        self.cTrav.traverse(base.render)
        self.queue.sortEntries()
        entry = self.queue.getEntry(0)
        if entry.getIntoNodePath().getParent() == self.planeNode:
            for node in self.selected: node.setColorScale(1,1,1,1) #turn white
            self.selected = []

            self.createObject(setPos = entry.getSurfacePoint(entry.getIntoNodePath()),
                            label = str(len(self.sSet.rawSimps)))


    def createObject(self, *args, **kwargs):
        #create a simplex in the simplicial set
        simplex = self.sSet.add(0,*args, **kwargs)

        #create an instance of simplex graphics in golog, send to simplex.data['node']
        simplexGr = self.gologNode.attachNewNode(simplex.label+" Node")
        simplex.data['node'] = simplexGr #refer to node from simplex
        self.graphicsToSimplex[simplexGr] = simplex #refer to simplex from node

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
        middlenode = self.gologNode.attachNewNode("middlenode")
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
        rope.reparentTo(self.gologNode)
        simplex.data['graphics'] = rope #simplex to Graphics
        self.graphicsToSimplex[rope] = simplex #graphics to simplex


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
