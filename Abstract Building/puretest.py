from direct.showbase.ShowBase import ShowBase
import sys, os
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
Camera_Distance = 100
grid_size = [2 , 2] #number of columns , rows of windows
grid_to_screen_pos = lambda i,j: [round(i/grid_size[0]*rs),round(j/grid_size[1]*(bs))+ts]
occupied = [[False for j in range(grid_size[1])] for i in range(grid_size[0])] #create an array of "unoccupied" slots
ws = [round(rs/grid_size[0]), round(bs/grid_size[1])-ts] #set window size
buttons = {'f5':sys.exit,'f6':sys.exit}
listener = DirectObject()
win_to_windict = dict()

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

    #open window
    newwin = base.openWindow(name = label)
    newwin.setWindowEvent(label+"-event")
    listener.accept(newwin.getWindowEvent(),windowEvent)

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
    mwNode = MouseWatcher(label)
    mwNode.setDisplayRegion(displayRegion)
    mw = mk.attachNewNode(mwNode)
    bt = ButtonThrower(label+"_button_thrower")
    bt.setPrefix(label+"_")
    mw.attachNewNode(bt)

    #format render display region
    render_dr = newwin.getDisplayRegion(1)
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

    #create Gui elements
    createButton(base, frame, .7, "Create", label+"_mode_create")
    createButton(base, frame, .4, "Preview", label+"_mode_preview")


    #create a display region for math data preview
    preview_dr = newwin.makeDisplayRegion(0,.3,0,.3)
    preview_label = label+"_preview"
    preview_mwNode = MouseWatcher(preview_label)
    preview_mwNode.setDisplayRegion(preview_dr)
    preview_mw = mk.attachNewNode(preview_mwNode)
    preview_bt = ButtonThrower(preview_label+"_button_thrower")
    preview_bt.setPrefix(preview_label+"_")
    preview_mw.attachNewNode(preview_bt)
    # preview_dr.setSort(30)


    windict =  {'win':newwin, 'mw':mw, 'bt':bt,'mk':mk,'label':label,'grid':grid,'preview_bt':preview_bt,'preview_mw':preview_mw,'preview_dr':preview_dr}
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


def createButton(base, frame, verticlePos, Text, event):

    btn = DirectButton(text = Text, scale = 0.2, command = base.messenger.send, pressEffect = 1, extraArgs = [event])
    btn.setPos(0, 0, verticlePos)

    btn.reparentTo(frame)
    print(btn.getBounds())


if __name__ == "__main__":

    class runner(ShowBase):
        def __init__(self):
            ShowBase.__init__(self,windowType = 'none')
            self.disable_mouse()

            base.accept("f5",sys.exit)
            base.accept("f6",sys.exit)

            self.sphere = self.loader.loadModel(os.path.abspath('./models/sphere.egg.pz'))
            s = self.render.attachNewNode('sphere')
            self.sphere.instanceTo(s)
            s = self.render.attachNewNode('sphere')
            self.sphere.instanceTo(s)
            s.setPos(0,0,10)
            self.camNode = Camera("camNode")
            self.camera = self.render.attachNewNode(self.camNode)
            self.camera.setPos(0,-Camera_Distance,0)

            windict = windowMaker(self, "window")
            windict['win'].getDisplayRegion(1).setCamera(self.camera)
            windict['preview_dr'].setCamera(self.camera)

            #events
            self.accept(windict['preview_bt'].prefix+'mouse1', lambda *x:print(windict['preview_bt'].prefix))
            # self.accept(windict['bt2d'].prefix+'mouse1', lambda *x:print(windict['bt2d'].getParent(0).getDisplayRegion().getCamera().getParent().ls()))
            self.accept(windict['label']+'_mode_create', lambda *x:print('create'))

    runner().run()
