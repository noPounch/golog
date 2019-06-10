import sys
from math import cos, sin
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties, NodePath
from golog import golog

Camera_Distance = 100

class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.camera.setPos(0,-Camera_Distance,0)
        self.disableMouse()

        win1 = self.winList[0]
        wp1 = WindowProperties()
        wp1.setSize(500,500)
        wp1.setOrigin(0,0)
        cam1 = self.camList[0]

        self.winList[0].requestProperties(wp1)
        wp2 = WindowProperties()
        wp2.setSize(500,500)
        wp2.setOrigin(1920-500,0)
        win2 = self.openWindow(wp2)
        cam2 = self.camList[1]
        print(type(cam2))

        render1 = self.render
        render2 = NodePath("render 2")
        cam2.reparentTo(render2)
        # win2.setCamera(cam2)

        self.accept('f5', sys.exit)
        self.accept('f6', sys.exit)
        g1 = golog(self,label = "golog 1", render = self.render, camNode = cam1)
        # print(self.render.ls())

        # g2 = golog(self,label = "golog 2", render = render2, camNode = cam2)

        #in order to create multiple nodes, we must pass new render nodes and camera nodes
        #g2 = golog(self,label = "golog2 ")
        # self.taskMgr.add(self.gologWiggler, 'wiggle', extraArgs = [g], appendTask=True)
        # self.taskMgr.add(self.add,'curve',extraArgs = [g], appendTask = True)


    def add(self,g,task):
        t = task.time
        g.createObject(setPos = (3*(t-10),0,3*sin(t)))
        return task.cont


    def gologWiggler(self, g, task):
        t = task.time
        g.gologNode.setPos(cos(20*t),0,cos(20*t))
        return task.cont

r = runner()
r.run()
