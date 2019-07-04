from direct.showbase.ShowBase import ShowBase
from math import sin, cos
from panda3d.core import Point3
import sys, os
from panda3d.core import loadPrcFileData
loadPrcFileData("", "want-directtools #t")
loadPrcFileData("", "want-tk #t")

class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()

        # need to migrate into gologToWindow
        base.accept("f5",sys.exit)
        base.accept("f6",sys.exit)

        self.tetra = self.loader.loadModel(os.path.abspath(os.path.dirname(__file__))+'/models/Cone.egg')
        self.sphere = self.loader.loadModel('models/misc/sphere')
        self.uparrow = self.
        self.tetra.setColorScale(1,1,1,1)

        self.arr = self.render.attachNewNode("arrow")
        self.tetra.instanceTo(self.arr)
        # self.tetra.setHpr(1,0,1)
        # print(self.tetra.getHpr())
        # self.node1 = self.render.attachNewNode('node1')
        # self.node1.setPos(10,0,10)
        # self.tetra.lookAt(self.node1.getPos(),(0,0,1))
        # print(self.tetra.getHpr())
        # # self.node2 = self.render.attachNewNode('node2')
        # # self.node2.setPos(-8,0,2)
        # self.sphere.instanceTo(self.node1)
        # # self.sphere.instanceTo(self.node2)
        #
        spheretocart = lambda x,y,z:(1)
        self.camera.setPos(0,-100,0)
        # self.taskMgr.add(lambda task:self.test_moving(self.node2,Point3(-8,0,2),task),'moving')


    def test_moving(self,node, origpos, task):
        t = task.time
        pos = origpos + Point3(10*sin(t),0,10*cos(t))
        self.arr.lookAt(node)
        node.setPos(pos)
        return task.cont


r = runner()
r.run()
