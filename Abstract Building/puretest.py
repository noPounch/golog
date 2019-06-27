import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.closeWindow(self.win)
        self.disable_mouse()

        label = 'win1'
        newwin = base.openWindow(name = label)
        newwin.setWindowEvent(label+"-event")
        displayRegion = newwin.getDisplayRegion(0)
        mkNode = MouseAndKeyboard(newwin,0,label+"_keyboard_mouse")
        mk = base.dataRoot.attachNewNode(mkNode)
        mwNode = MouseWatcher(label)
        mwNode.setDisplayRegion(displayRegion)
        self.mw = mk.attachNewNode(mwNode)
        bt = ButtonThrower(label+"_button_thrower")
        bt.setPrefix(label+"_")
        self.mw.attachNewNode(bt)
        #format window

        #create a displayRegion for 2d
        dr2d = newwin.makeDisplayRegion()
        dr2d.setSort(2)

        base.accept("f5",sys.exit)
        base.accept("f6",sys.exit)
        print([dr.getCamera() for dr in self.win.getDisplayRegions()])


        #create 2d render and set up camera
        render2d = NodePath('2d render')
        camera2D = render2d.attachNewNode(Camera('2d camera'))
        camera2D.setDepthTest(False)
        camera2D.setDepthWrite(False)
        lens = OrthographicLens()
        lens.setFilmSize(2, 2)
        lens.setNearFar(-1000, 1000)
        camera2D.node().setLens(lens)
        dr2d.setCamera(camera2D)

        textNP = render2d.attachNewNode(TextNode('yo'))

        text = textNP.node()
        text.setText('hello')
        textNP.setScale(.05)
        textNP.setPos(0,0,0)
        text.setFrameColor(0, 0, 1, 1)
        text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
        taskMgr.add(self.textAtMouse, "mouse watching",extraArgs = [textNP],appendTask = True)

    def textAtMouse(self,textNP,task):
        if not self.mouseWatcherNode.hasMouse(): return task.cont
        (mx,my) = (self.mouseWatcherNode.getMouseX(),self.mouseWatcherNode.getMouseY())
        textNP.setPos(mx,0,my)
        return task.cont
r = runner()
r.run()
