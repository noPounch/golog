from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, WindowProperties, Camera

rs = 1920-6
ts = 60
ws = 200
Camera_Distance = 100


class Base(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()
        render2 = NodePath('render2')
        cam = Camera('newcam')
        camNP = NodePath(cam)
        camNP.reparentTo(render2)
        camNP.setPos(0,-Camera_Distance,0)
        print(self.win.getActiveDisplayRegions())
        self.win.getDisplayRegion(2).setCamera(camNP)


        self.scenem = self.loader.load_model("environment")
        self.scene = render2.attachNewNode("scene")
        self.scenem.instanceTo(self.scene)
        self.scenem.reparent_to(render2)
        self.scene.set_scale(.25)
        self.scene.set_pos(-8., 42., 0.)

        sphere = self.loader.loadModel("models/misc/sphere")
        sphere1 = self.render.attachNewNode("sphere1")
        sphere.instanceTo(sphere1)
        sphere1.setPos(0,0,0)


        base.accept("mouse1", messyKwargPasser, extraArgs = [ foo, ['hello' ], {'well':'hi there'} ] )

def messyKwargPasser(f, arglist, kwargdict):
    return f(*arglist,**kwargdict)

def foo(*args,**kwargs):
    print("args: ", args)
    print("kwargs: ", kwargs)



if __name__ == '__main__':
    app = Base()
app.run()
