import sys
from math import cos, sin
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties
from panda3d.core import NodePath, MouseWatcher, ButtonThrower, MouseAndKeyboard, Camera
from golog import golog as Golog

rs = 1920-6
ts = 60
ws = 200


class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()
        #setup main window
        wp = WindowProperties()
        wp.setOrigin(rs-ws,ts)
        wp.setSize(ws,ws)
        # self.win.requestProperties(wp)
        golog = Golog(self)
        windict = {'win':self.win,'mw':self.mouseWatcher,'bt':self.buttonThrowers[0].node()}
        self.gologToWindow(golog,windict)
        print(self.win.getDisplayRegion(0).getCamera() == golog.camera)
        print(self.win.getDisplayRegion(0).getCamera())
        print(golog.camera.getHpr())

        s = golog.render.attachNewNode("sphere")
        self.sphere = base.loader.loadModel("models/misc/sphere")

        self.sphere.instanceTo(s)

    def gologToWindow(self, golog, windict = None):
        if not windict:
            windict = self.windowMaker(golog.label)
        win = windict['win']; mw = windict['mw']; bt = windict['bt']
        win.getDisplayRegion(0).setCamera(golog.camera) #set window to view camera
        golog.mouseWatcherNode = mw.node() #set golog.mouseWatcherNode to window's mousewatcher node
        bt.setPrefix(golog.label+"_")


    def windowMaker(self, label):
        #Create Window, Display Region, mouseAndKeyboard control, mouse watcher and button thrower
        #button thrower throws "label_event" (e.g. win2_mouse1)
        i = len(self.winList)
        newwin = self.openWindow()
        displayRegion = newwin.getDisplayRegion(0)
        mouseAndKeyboardNode = MouseAndKeyboard(newwin,0,label+"_keyboard_mouse")
        mouseAndKeyboard = self.dataRoot.attachNewNode(mouseAndKeyboardNode)
        mouseWatcherNode = MouseWatcher(label)
        mouseWatcherNode.setDisplayRegion(displayRegion)
        mouseWatcher = mouseAndKeyboard.attachNewNode(mouseWatcherNode)
        buttonThrower = ButtonThrower(label+"_button_thrower")
        buttonThrower.setPrefix(label+"_")
        mouseWatcher.attachNewNode(buttonThrower)
        #format window
        wp = WindowProperties()
        wp.setOrigin(rs-ws,ts+(ws+32)*i)
        wp.setSize(ws,ws)
        newwin.requestProperties(wp)

        return {'win':newwin, 'mw':mouseWatcher, 'bt':buttonThrower}



r = runner()
r.run()
