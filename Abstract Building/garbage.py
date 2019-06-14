from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import NodePath, MouseWatcher, ButtonThrower, MouseAndKeyboard, Camera, VBase4

class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()
        a = Actor('panda.egg', {'walk' : 'panda-walk.egg'})
        a.pose('walk', 0)
        a.reparentTo(render)
        self.camera.setPosHpr(-41, -23, 18, -61, -15, 0)



        cam = self.makeNewDr()
        self.splitScreen(self.cam,cam)

    def makeNewDr(self):
        dr2 = base.win.makeDisplayRegion(0.1, 0.4, 0.2, 0.6)
        dr2.setClearColor(VBase4(0, 0, 0, 1))
        dr2.setClearColorActive(True)
        dr2.setClearDepthActive(True)

        render2 = NodePath('render2')
        cam2 = render2.attachNewNode(Camera('cam2'))
        dr2.setCamera(cam2)

        env = loader.loadModel('environment.egg')
        env.reparentTo(render2)

        cam2.setPos(-22.5, -387.3, 58.1999)
        return cam2

    def splitScreen(self, cam, cam2):
        dr = cam.node().getDisplayRegion(0)
        dr2 = cam2.node().getDisplayRegion(0)

        dr.setDimensions(0, 0.5, 0, 1)
        dr2.setDimensions(0.5, 1, 0, 1)

        cam.node().getLens().setAspectRatio(float(dr.getPixelWidth()) / float(dr.getPixelHeight()))
        cam2.node().getLens().setAspectRatio(float(dr2.getPixelWidth()) / float(dr2.getPixelHeight()))







# a = Actor('panda.egg', {'walk' : 'panda-walk.egg'})
# a.pose('walk', 0)
#
# a.reparentTo(render)
#
# dlight = NodePath(DirectionalLight('dlight'))
# dlight.reparentTo(base.cam)
# render.setLight(dlight)
#
# base.disableMouse()
# camera.setPosHpr(-41, -23, 18, -61, -15, 0)


r = runner()
r.run()
