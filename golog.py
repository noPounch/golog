from math import pi, sin, cos, floor

import hcat
import tkinter
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class golog(ShowBase):
    def __init__(self,*args, **kwargs):
        ShowBase.__init__(self)
        self.disableMouse()
        self.camera.setPos(0,-100,0)
        self.metadata = {'tfloor', }

        #create a golog, a dummy node represents the golog as a "universe"
        #all simplecies should be child nodes of gologNode
        self.gologNode = self.render.attachNewNode("golog")
        self.sSet = hcat.simpSet(label = "golog", data = {'node':self.gologNode})

        self.sphere = self.loader.loadModel("models/misc/sphere")
        #self.sphere.reparentTo(self.gologNode)

        a = self.createNewSimplex(0, setPos = (2,0,2),label = 'a')
        b = self.createNewSimplex(0, label = 'b')
        f = self.createNewSimplex((b,a), label = 'f')
        self.taskMgr.add(lambda t: self.moverTask(self.sphere,t), "camera task")
        self.sphere.ls()

    def createNewSimplex(self, *args, **kwargs):
        numsimps = len(self.sSet.rawSimps)

        #create a simplex in the simplicial set
        simplex = self.sSet.add(*args, **kwargs)

        #create an instance of simplex graphics in golog, send to simplex.data['gr']
        simplexGr = self.render.attachNewNode(simplex.label+" Node")
        simplex.data['gr'] = simplexGr
        self.sphere.instanceTo(simplexGr)

        defaults = {'setPos':(2*numsimps,0,0)}
        for key in defaults.keys():
            if key in kwargs.keys(): getattr(simplexGr,key)(kwargs[key])
            else: getattr(simplexGr,key)(defaults[key])
        simplexGr.ls()
        return simplex

    def moverTask(self,ob,task):
        t = task.time
        curve = lambda t: Point3(sin(10*t),0,0)
        ob.setPos(curve(t))
        return task.cont

    def cameraTask(self, task):
        t = task.time
        self.camera.setPos(50*cos(t),50*sin(t),0)
        self.camera.lookAt(self.sSet.rawSimps[0].data['gr'])
        return task.cont

app = golog()
app.run()
