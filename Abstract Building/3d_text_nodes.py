import sys
from math import cos
from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode




class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()
        self.camera.setPos(0,-100,0)

        text = TextNode('test')
        text.setText('test label')
        text.setCardDecal(True)
        text.setCardColor(1, 1, 1, 1)
        text.setCardAsMargin(0, 0, 0, 0)
        text.setTextColor(0,0,0,1)
        self.textNP = self.render.attachNewNode(text)



        # need to migrate into gologToWindow
        base.accept("f5", sys.exit)
        base.accept("f6", sys.exit)

        base.taskMgr.add(self.text_move,'text_move')

    def text_move(self, task):
        t = task.time
        pos = (0,10*cos(t), 0)
        self.textNP.setPos(*pos)
        return task.cont





r = runner()
r.run()
