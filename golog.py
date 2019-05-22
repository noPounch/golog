from math import pi, sin, cos, floor

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.model = self.loader.loadModel("models/box")

        self.model.setPos(0,20,0)
        self.model.setScale(1,1,1)
        self.model.reparentTo(self.render)
        self.camera.setPos(0,-20,0)

        self.spheres = self.render.attachNewNode("boxes")
        #self.boxes.reparentTo(self.render)
        self.sphere = self.loader.loadModel("models/misc/sphere")
        self.sphere.setColor()
        self.box.reparentTo(self.boxes)
        self.taskMgr.add(self.boxMakerMover, "Box Maker Mover Task")


    def boxMakerMover(self,task):
        t = task.time
        curve = lambda t: Point3( t, 0,sin(45*t))
        self.boxes.setPos(curve(t))
        self.box.setPos(-curve(t))
        print(self.box.getX() == self.box.getX(self.boxes))
        return Task.cont




    def boxMaker(self, task):
        t = task.time
        print(t)
        curve = lambda t: Point3( t, 0,sin(45*t))
        model = self.loader.loadModel("models/box")
        model.setPos(curve(t))
        model.reparentTo(self.boxes)
        return Task.cont


    def camera(self, task):
        self.camera.lookAt(self.sphere)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

app = MyApp()
app.run()
