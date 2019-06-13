import sys
import random

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, PandaNode, WindowProperties

rs = 1920-6
ts = 60
ws = 200
Camera_Distance = 100


class Base(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()
        wp = WindowProperties()
        wp.setOrigin(rs-ws,ts)
        wp.setSize(ws,ws)
        self.win.requestProperties(wp)
        self.camera.setPos(0,-100,0)
        sphere = self.loader.loadModel("models/misc/sphere")
        sphere1 = self.render.attachNewNode("sphere1")
        sphere.instanceTo(sphere1)

        print(self.camera)


if __name__ == '__main__':
    app = Base()
app.run()
