## File for testing Collision Detection on Glog objects
from math import pi, sin, cos, floor
import sys
import tkinter
from direct.showutil.Rope import Rope
from direct.task import Task
from panda3d.core import Vec3, Point3, LPoint3f, Plane, NodePath
from panda3d.core import CollisionPlane, CollisionRay, CollisionSphere
from panda3d.core import CollisionNode, CollisionTraverser, CollisionHandlerQueue

Camera_Distance = 30
dragging = False

class test():
    def __init__(self,base):


        #set up traverser and handler
        self.cTrav = CollisionTraverser('main traverser')
        self.queue = CollisionHandlerQueue()
        self.selected = []

        #set up ray picker
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = base.camera.attachNewNode(self.pickerNode)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)

        #traverser sends ray collisions to handler
        self.cTrav.addCollider(self.pickerNP,self.queue)


        # self.accept("mouse1",self.selectTest)
        base.accept("mouse1",self.mouse1down)
        base.accept("mouse1-up",self.mouse1up)




        self.planeNode = base.render.attachNewNode("plane")
        self.planeFromObject = self.planeNode.attachNewNode(CollisionNode("planeColNode"))
        self.planeFromObject.node().addSolid(CollisionPlane(Plane(Vec3(0,-1,0),Point3(0,0,0))))

        #load model
        self.sphereModel = base.loader.loadModel("models/misc/sphere")
        self.sphereModel.setColor(1,1,1,1) #white

    def projectMouseToPlane():
        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode,mpos.getX(),mpos.getY())
        self.cTrav.traverse(base.render)
        #return intersection of ray with plane
        #return entry.getSurfacePoint(entry.getIntoNodePath())


    def mouse1down(self):
        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode,mpos.getX(),mpos.getY())
        self.cTrav.traverse(base.render)


        self.queue.sortEntries()
        entry = self.queue.getEntry(0)

        if entry.getIntoNodePath().getParent() == self.planeNode:
            for node in self.selected: node.setColorScale(1,1,1,1) #turn white
            self.selected = []
            self.createObject(entry)
        else:
            self.selected.append(entry.getIntoNodePath().getParent())
            entry.getIntoNodePath().getParent().setColorScale(1,0,0,0) #turn red
        print(self.selected)

        #dragging code
        dragging = True


    def mouse1up(self):
        print("yo")

    def createObject(self,entry):
        node = base.render.attachNewNode("sphere")
        node.setPos(entry.getSurfacePoint(entry.getIntoNodePath()))
        self.sphereModel.instanceTo(node)
        collisionNode = node.attachNewNode(CollisionNode('sphereColNode'))
        collisionNode.node().addSolid(CollisionSphere(0,0,0,1))
        return node
