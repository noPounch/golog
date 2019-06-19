import sys
from math import cos, sin
from direct.task import Task
from panda3d.core import WindowProperties
from panda3d.core import NodePath, MouseWatcher, ButtonThrower, MouseAndKeyboard, Camera
from golog import golog as Golog

rs = 1920-6
ts = 60
ws = 500

def modeHeadToWindow(base, modeHead, windict = None):
    i = len(base.winList)
    if not windict:
        windict = windowMaker(base, "win{}".format(i))
    win = windict['win']; mw = windict['mw']; bt = windict['bt']
    win.getDisplayRegion(1).setCamera(modeHead.golog.camera) #set window to view golog camera
    # golog.windicts.append(windict) #set golog.mouseWatcherNode to window's mousewatcher node
    for button in modeHead.buttons.keys():
        base.accept(bt.prefix+button, modeHead.buttons[button], extraArgs = [mw]) #golog accepts window's events and sends them to specified handler function
    return win


def windowMaker(base, label):
    #Create Window, Display Region, mouseAndKeyboard control, mouse watcher and button thrower
    #button thrower throws "label_event" (e.g. win2_mouse1)
    i = len(base.winList)
    newwin = base.openWindow()
    displayRegion = newwin.getDisplayRegion(0)
    mouseAndKeyboardNode = MouseAndKeyboard(newwin,0,label+"_keyboard_mouse")
    mouseAndKeyboard = base.dataRoot.attachNewNode(mouseAndKeyboardNode)
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
