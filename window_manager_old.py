import sys
import gc
from math import cos, sin
from direct.task import Task
from panda3d.core import WindowProperties
from panda3d.core import NodePath, MouseWatcher, ButtonThrower, MouseAndKeyboard, Camera
from direct.showbase.DirectObject import DirectObject

rs = 1920-6 #side minus some padding
bs = 1080-30 #bottom minus toolbar
ts = 30
grid_size = [4 , 3] #number of columns , rows of windows
grid_to_screen_pos = lambda i,j: [round(i/grid_size[0]*rs),round(j/grid_size[1]*(bs))+ts]
occupied = [[False for j in range(grid_size[1])] for i in range(grid_size[0])] #create an array of "unoccupied" slots
ws = [round(rs/grid_size[0]), round(bs/grid_size[1])-ts] #set window size
buttons = {'f5':sys.exit,'f6':sys.exit}
listener = DirectObject()
win_to_windict = dict()

def modeHeadToWindow(base, mode_head, windict = None):

    i = len(base.winList)
    if not windict:
        windict = windowMaker(base, "win{}".format(i))

    win = windict['win']; mw = windict['mw']; bt = windict['bt']; mk = windict['mk']

    win.getDisplayRegion(1).setCamera(mode_head.golog.camera) #set window to view golog's 3d camera
    win.getDisplayRegion(2).setCamera(mode_head.camera2D)
    # print([dr.getCamera() for dr in win.getDisplayRegions()])
    windict['mode_head'] = mode_head
    # golog.windicts.append(windict) #set golog.mouseWatcherNode to window's mousewatcher node
    for button in mode_head.buttons.keys():
        mode_head.listener.accept(bt.prefix+button, mode_head.buttons[button], extraArgs = [mw]) #golog accepts window's events and sends them to specified handler function
    for button in buttons:
        listener.accept(bt.prefix+button,buttons[button])
    for window_task in mode_head.window_tasks:
        base.taskMgr.add(window_task, 'window_task_name', extraArgs = [mw], appendTask = True)
    return win


def windowMaker(base,label):
    # find an open slot, if none, return false

    grid = None
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            if occupied[i][j] == False:
                grid = (i,j)
                occupied[i][j] = True
                break
        else: continue
        break
    if not grid: return False
    position = grid_to_screen_pos(*grid)
    newwin = base.openWindow(name = label)
    newwin.setWindowEvent(label+"-event")
    listener.accept(newwin.getWindowEvent(),windowEvent)
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
    #create a displayRegion for 2d
    dr2d = newwin.makeDisplayRegion()
    dr2d.setSort(2)

    windict =  {'win':newwin, 'mw':mw, 'bt':bt,'mk':mk,'label':label,'grid':grid}
    win_to_windict[newwin] = windict

    return windict

def windowEvent(win):
    windict = win_to_windict[win]
    if win.closed:
        windowCloseCleaner(windict)
        return

def windowCloseCleaner(windict):
    if 'mode_head' in windict:
        golog = windict['mode_head'].golog
        mode_head = windict['mode_head']
        del windict['mode_head']
        mode_head.reset()
        mode_head.clean()
    occupied[windict['grid'][0]][windict['grid'][1]] = False
    listener.ignore(windict['win'].getWindowEvent())
    del win_to_windict[windict['win']]
    del windict
