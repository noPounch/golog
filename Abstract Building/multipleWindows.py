import sys
from math import cos, sin
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, NodePath, MouseWatcher



Camera_Distance = 100

class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()


        ###### WINDOW 1
        wp1 = WindowProperties()
        wp1.setSize(500,500)
        wp1.setOrigin(0,0)
        win1 = self.winList[0]
        cam1 = self.camList[0]
        win1.requestProperties(wp1)

        render1 = self.render
        mouseWatcher1 = self.mouseWatcherNode


        ####### END WINDOW 1

        ####### WINDOW 2
        wp2 = WindowProperties()
        wp2.setSize(500,500)
        wp2.setOrigin(1920-500,0)
        win2 = self.openWindow(wp2)

        # create new camera and bind it to window 2
        cam2 = self.camList[1]
        win2.getDisplayRegion(0).setCamera(cam2)

        #create a new render and point the camera in it
        render2 = NodePath("render 2")
        cam2.reparentTo(render2)

        # create a new mouseWatcher, make it watch window 2
        mouseWatcher2 = MouseWatcher()
        mouseWatcher2.setDisplayRegion(win2.getDisplayRegion(0))




        ######### END WINDOW 2


        ###### TEST
        cam1.setPos(0,-100,0)
        cam2.setPos(0,-100,0)
        sphere = self.loader.loadModel("models/misc/sphere")
        sphere1 = render1.attachNewNode("sphere1")
        sphere1.setPos(0,0,20)
        sphere2 = render2.attachNewNode("sphere2")
        sphere.instanceTo(sphere1)
        sphere.instanceTo(sphere2)
        self.accept('f5', sys.exit)
        self.accept('f6', sys.exit)
        self.accept('mouse1',self.mousePrint, extraArgs = ['yo'])

        # self.taskMgr.add()


        def mouseprint(self,mouseNode,task):
            if mouseNode.hasMouse(): print(mouseNode.getDisplayRegion())

r = runner()
r.run()
