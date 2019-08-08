import sys, os
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
# from direct.showbase.InputStateGlobal import inputState


version = '1.0.0'


class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()
        self.camera.setPos(0,-100,0)


        self.sphere = self.loader.loadModel('./models/sphere.egg.pz')
        self.queue = CollisionHandlerQueue()
        self.selected = [[],[]] #tracking previously selected nodes of each level

        # set up mouse picker
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.camera.attachNewNode(self.pickerNode) #attach collision node to camera
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.pickerNode.set_into_collide_mask(0) #so that collision rays don't collide into each other if there are two mode_heads
        self.cTrav = CollisionTraverser('traverser')
        self.cTrav.addCollider(self.pickerNP,self.queue) #send collisions to self.queue
        # set up plane for picking
        self.planeNode = self.render.attachNewNode("plane")
        self.planeNode.setTag("mode_node", 'plane')

        self.planeFromObject = self.planeNode.attachNewNode(CollisionNode("planeColNode"))
        self.planeFromObject.node().addSolid(CollisionPlane(Plane(Vec3(0,-1,0),Point3(0,0,0))))
        self.grabbed_node = None

        self.NP = self.render.attachNewNode('object')
        self.NP.setTag('mode_node','object')
        self.sphere.instanceTo(self.NP)
        self.collision = self.NP.attachNewNode(CollisionNode('sphereColNode'))
        self.collision.node().addSolid(CollisionSphere(0,0,0,1))

        def grab(mw):
            if not mw.node().hasMouse(): return
            mpos = mw.node().getMouse()
            self.pickerRay.setFromLens(self.camNode,mpos.getX(),mpos.getY()) #mouse ray goes from camera through the 'lens plane' at position of mouse
            self.cTrav.traverse(self.render)
            self.queue.sortEntries()
            if self.queue.getEntry(0).getIntoNodePath().getParent().getTag('mode_node') == 'plane':
                print('teehee, you tickled my plane node :)') #drag camera
            if self.queue.getEntry(0).getIntoNodePath().getParent().getTag('mode_node') == 'object':
                self.grabbed_node = self.queue.getEntry(0).getIntoNodePath().getParent()

            print(self.grabbed_node)


        def drop():
            self.grabbed_node = None

        base.accept('mouse1', lambda *x: grab(self.mouseWatcher))
        base.accept('mouse1-up', lambda *x: drop())




        self.timer = 0
        self.taskMgr.add(self.mouse_watcher, 'mouse_watch', extraArgs = [self.mouseWatcher], appendTask = True)


    def mouse_watcher(self, mw, task):

        if not mw.node().hasMouse: return task.cont
        if self.grabbed_node:
            print(self.grabbed_node)
            if not mw.node().hasMouse(): return task.cont
            mpos = mw.node().getMouse()
            self.pickerRay.setFromLens(self.camNode,mpos.getX(),mpos.getY()) #mouse ray goes from camera through the 'lens plane' at position of mouse
            self.cTrav.traverse(self.render)
            self.queue.sortEntries()
            mouseloc = self.grabbed_node.getPos()
            for e in self.queue.getEntries():
                if e.getIntoNodePath().getParent().getTag("mode_node") == 'plane':
                    mouseloc = e.getSurfacePoint(e.getIntoNodePath())
                    break
            #get location of mouse over plane

            self.grabbed_node.setPos(mouseloc)


        return task.cont








r = runner()
r.run()
