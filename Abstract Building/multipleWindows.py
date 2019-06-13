import sys
from math import cos, sin
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import NodePath, MouseWatcher, ButtonThrower, MouseAndKeyboard, Camera

rs = 1920-6
ts = 60
ws = 200
Camera_Distance = 100

class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()
        #setup main window
        wp = WindowProperties()
        wp.setOrigin(rs-ws,ts)
        wp.setSize(ws,ws)
        self.win.requestProperties(wp)
        self.buttonThrowers[0].node().setPrefix('win1_')
        self.camera.setPos(0,-100,0)




        #Testing
        render1 = self.render
        render2 = NodePath("render2")
        render3 = NodePath("render3")

        sphere = self.loader.loadModel("models/misc/sphere")
        sphere1 = self.render.attachNewNode("sphere1")
        sphere.instanceTo(sphere1)
        sphere2 = render2.attachNewNode("sphere2")
        sphere.instanceTo(sphere2)
        sphere3 = render3.attachNewNode("sphere3")
        sphere.instanceTo(sphere3)



        self.windowMaker(render2,'win2')
        self.windowMaker(render3,'win3')
        self.accept("win1_mouse1", lambda: self.__on_left_down(1))
        self.accept("win2_mouse1", lambda: self.__on_left_down(2))
        self.accept("win3_mouse1", lambda: self.__on_left_down(3))

    def windowMaker(self, render, label):
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

        #point the camera to given render scene graph
        camNode = Camera(label+"_Camera")
        cam = render.attachNewNode(camNode)
        displayRegion.setCamera(cam)
        cam.setPos(0,-100,0)



        return {'win':newwin,'camera':camera, }

    def __on_left_down(self, window_id):
        print("Left mouse button pressed in window {}!".format(window_id))

r = runner()
r.run()
