import sys
from direct.showbase.ShowBase import ShowBase
from golog import golog

Camera_Distance = 30

class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.camera.setPos(0,-Camera_Distance,0)
        self.disableMouse()
        self.accept('f5', sys.exit)
        self.accept('f6', sys.exit)
        g = golog(self)


r = runner()
r.run()
