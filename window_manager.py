import sys, os, platform
import gc
from math import cos, sin
from direct.task import Task
from panda3d.core import WindowProperties, PGTop
from panda3d.core import NodePath, MouseWatcher, ButtonThrower, MouseAndKeyboard, Camera, OrthographicLens
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectFrame,DirectLabel,DirectButton



rs = 1920-6 #side minus some padding
bs = 1080-30 #bottom minus toolbar
ts = 30
grid_size = [2 , 2] #number of columns , rows of windows
grid_to_screen_pos = lambda i,j: [round(i/grid_size[0]*rs),round(j/grid_size[1]*(bs))+ts]
occupied = [[False for j in range(grid_size[1])] for i in range(grid_size[0])] #create an array of "unoccupied" slots
ws = [round(rs/grid_size[0]), round(bs/grid_size[1])-ts] #set window size
buttons = {'f5':sys.exit,'f6':sys.exit}
listener = DirectObject()
win_to_windict = dict()

def modeHeadToWindow(base, mode_head):

    #? if modeHead is open in another window, just focus that window
    i = len(base.winList)
    if mode_head.has_window == True:
        wp = WindowProperties()
        wp.setForeground(True)
        mode_head.windict['win'].requestProperties(wp)
        return #focus window
    windict = windowMaker(base, "win{}".format(i))

    win = windict['win']; mw = windict['mw']; bt = windict['bt']; mk = windict['mk']

    windict['render_dr'].setCamera(mode_head.golog.camera) #set window to view golog's 3d camera
    windict['mode_head'] = mode_head

    #set up window_events in mode_head (if this is the first time, this will change mode_head.bt/.mw)
    mode_head.selection_and_creation(windict)
    def text_preview():
        mode_head.bools['textboxes'] = not mode_head.bools['textboxes']
        mode_head.golog.text_preview_set(mode_head.bools['textboxes'])

    #if mode_head has a parent, create a button to open it
    if mode_head.parent:
        createButton(base, windict['gui_frame'], .4, "Open Parent", bt.prefix+"parent")
        windict['guibuttons']['Parent'] = bt.prefix+"parent" #assign messenger call


    mode_dict = {'Preview':text_preview,"Parent": lambda *x: modeHeadToWindow(base, mode_head.parent)}
    #do something with guibuttons
    for button in windict['guibuttons'].keys():
        base.accept(windict['guibuttons'][button],mode_dict[button]) #set messenger call

    #? make accept f5/f6
    # for button in buttons.keys():
    #     base.accept(button, )
    return windict

#send a golog to some display region
def gologToDr(base, mode_head, drdict = None):
    if drdict == None: modeHeadToWindow(base, mode_head, None)
    #? else set display region's camera to the mode_head.golog's camera

#find a place for the window, and then make the window
# and return a dict with all it's display regions, and interaction tools (bt,mw,etc.)
def windowMaker(base,label):
    # find an open slot, if none, return false
    windict = dict()
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
    windict['grid'] = grid
    position = grid_to_screen_pos(*grid)

    #open window
    newwin = base.openWindow(name = label)
    newwin.setWindowEvent(label+"-event")
    listener.accept(newwin.getWindowEvent(),windowEvent)
    windict['win'] = newwin

    #format window
    wp = WindowProperties()
    wp.setOrigin(*position)
    wp.setSize(*ws)
    newwin.requestProperties(wp)

    #make 3d-mousewatcher display region
    displayRegion = newwin.getDisplayRegion(0)
    displayRegion.setDimensions(.3,1,0,1)
    mkNode = MouseAndKeyboard(newwin,0,label+"_keyboard_mouse")
    mk = base.dataRoot.attachNewNode(mkNode)
    windict['mk'] = mk
    mwNode = MouseWatcher(label)
    mwNode.setDisplayRegion(displayRegion)
    mw = mk.attachNewNode(mwNode)
    windict['mw'] = mw
    bt = ButtonThrower(label+"_button_thrower")
    windict['bt'] = bt
    bt.setPrefix(label+"_")
    mw.attachNewNode(bt)
    #listen for default button events
    for button in buttons:
        listener.accept(bt.prefix+button,buttons[button])

    #format render display region
    render_dr = newwin.getDisplayRegion(1)
    windict['render_dr'] = render_dr
    render_dr.setDimensions(.3,1,0,1)

    #create a display region for Gui Elements
    gui_dr = newwin.makeDisplayRegion(0,.3,.3,1)
    # gui_dr.setSort(20)
    mwNodegui = MouseWatcher(label+"gui")
    mwNodegui.setDisplayRegion(gui_dr)
    mwgui = mk.attachNewNode(mwNodegui)

    #create a 2d render/aspect for gui
    rendergui = NodePath('render2d')
    rendergui.setDepthWrite(0)
    rendergui.setMaterialOff(1)
    rendergui.setTwoSided(1)
    #set up aspect2d
    aspectgui = rendergui.attachNewNode(PGTop('aspectgui'))
    aspectgui.node().setMouseWatcher(mwgui.node())
    #set up camera
    camNodegui = Camera("camNode2d")
    cameragui = rendergui.attachNewNode(camNodegui)
    cameragui.setPos(0,0,0)
    cameragui.setDepthTest(False)
    cameragui.setDepthWrite(False)
    lens = OrthographicLens()
    lens.setFilmSize(2, 2)
    lens.setNearFar(-1000, 1000)
    cameragui.node().setLens(lens)
    gui_dr.setCamera(cameragui)
    #make frame for gui
    frame = DirectFrame(frameSize = (-1,1,-1,1), frameColor = (.5,.5,.5,1), relief = 'ridge')
    frame.reparentTo(aspectgui)
    frame.setTransparency(0)
    windict['gui_frame'] = frame

    #create Gui elements
    guibuttons = dict()
    # guibuttons['Create'] = label+"_mode_create"
    guibuttons['Preview'] = label+"_preview"
    # createButton(base, frame, .7, "Create", label+"_mode_create")
    createButton(base, frame, .7, "Preview", label+"_preview")
    windict['guibuttons'] = guibuttons


    #create a display region for math data preview
    preview_dr = newwin.makeDisplayRegion(0,.3,0,.3)
    windict['preview_dr'] = preview_dr
    # preview_label = label+"_preview"
    # preview_mwNode = MouseWatcher(preview_label)
    # preview_mwNode.setDisplayRegion(preview_dr)
    # preview_mw = mk.attachNewNode(preview_mwNode)
    # preview_bt = ButtonThrower(preview_label+"_button_thrower")
    # preview_bt.setPrefix(preview_label+"_")
    # preview_mw.attachNewNode(preview_bt)
    # preview_dr.setSort(30)

    win_to_windict[newwin] = windict

    return windict

#create a button in a given frame (usually windict['gui_frame'])
def createButton(base, frame, verticlePos, Text, event):

    btn = DirectButton(text = Text, scale = 0.2, command = base.messenger.send, pressEffect = 1, extraArgs = [event])
    btn.setPos(0, 0, verticlePos)

    btn.reparentTo(frame)

#event to call when window closes
def windowEvent(win):
    windict = win_to_windict[win]
    if win.closed:
        windowCloseCleaner(windict)
        return

# function to clean up references when a window closes
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
