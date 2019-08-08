import sys, os
from direct.showbase.ShowBase import ShowBase
from direct.showutil.Rope import Rope

from panda3d.core import *
# from direct.showbase.InputStateGlobal import inputState


version = '1.0.0'


class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()
        self.camera.setPos(0,-100,0)

        a = self.render.attachNewNode('a')
        b = self.render.attachNewNode('b')
        c = self.render.attachNewNode('c')
        a.setPos(0,0,0)
        b.setPos(3,0,0)
        c.setPos(3,0,3)

        rope1 = Rope()
        rope1.setup(2, [(a,(0,0,0)),(b,(0,0,0))])
        rope1.reparentTo(self.render)
        rope2 = Rope()
        rope2.setup(2, [(b,(0,0,0)),(c,(0,0,0))])
        rope2.reparentTo(self.render)
        # curve = rope.curve
        # print(curve.getVertices())
        # curve.adjustPoint(0,0,0,0)
        # curve.adjustPoint(1,1,0,0)
        # curve.adjustPoint(2,1,0,1)








r = runner()
r.run()
