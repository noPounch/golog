import sys
from math import cos, sin
from direct.task import Task
from panda3d.core import WindowProperties
from panda3d.core import NodePath, MouseWatcher, ButtonThrower, MouseAndKeyboard, Camera
from golog import golog as Golog

rs = 1920-6 #side minus some padding
bs = 1080-30 #bottom minus toolbar
ts = 30
grid_size = [3 , 2] #number of columns , rows of windows
grid_to_screen_pos = lambda i,j: [round(i/grid_size[0]*rs),round(j/grid_size[1]*(bs))+ts]
occupied = [[False for j in range(grid_size[1])] for i in range(grid_size[0])] #create an array of "unoccupied" slots
ws = [round(rs/grid_size[0]), round(bs/grid_size[1])-ts] #set window size
buttons = {'f5':sys.exit,'f6':sys.exit}

def modeHeadToWindow(base, modeHead, windict = None):
    i = len(base.winList)
    if not windict:
        windict = newwindowMaker(base, "win{}".format(i))

    win = windict['win']; mw = windict['mw']; bt = windict['bt']
    win.getDisplayRegion(1).setCamera(modeHead.golog.camera) #set window to view golog camera
    # golog.windicts.append(windict) #set golog.mouseWatcherNode to window's mousewatcher node
    listener = modeHead.listener
    for button in modeHead.buttons.keys():
        modeHead.listener.accept(bt.prefix+button, modeHead.buttons[button], extraArgs = [mw]) #golog accepts window's events and sends them to specified handler function
    for button in buttons:
        base.accept(bt.prefix+button,buttons[button])
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


def newwindowMaker(base,label):
    # find an open slot, if none, return false
    position = None
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            if occupied[i][j] == False:
                print(i,j)
                position = grid_to_screen_pos(i,j)
                occupied[i][j] = True
                break
        else: continue
        break
    if not position: return False
    print(position)
    newwin = base.openWindow()
    displayRegion = newwin.getDisplayRegion(0)
    mkNode = MouseAndKeyboard(newwin,0,label+"_keyboard_mouse")
    mk = base.dataRoot.attachNewNode(mkNode)
    mwNode = MouseWatcher(label)
    mwNode.setDisplayRegion(displayRegion)
    mw = mk.attachNewNode(mwNode)
    bt = ButtonThrower(label+"_button_thrower")
    bt.setPrefix(label+"_")
    mw.attachNewNode(bt)
    #format window
    wp = WindowProperties()
    wp.setOrigin(*position)
    wp.setSize(*ws)
    newwin.requestProperties(wp)

    return {'win':newwin, 'mw':mw, 'bt':bt,'mk':mk}
