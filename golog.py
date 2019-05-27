from math import pi, sin, cos, floor

import hcat
import tkinter
from direct.showutil.Rope import Rope
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class golog(ShowBase):
    def __init__(self,*args, **kwargs):
        ShowBase.__init__(self)
        self.disableMouse()
        self.camera.setPos(0,-30,0)

        #create a golog, a dummy node represents the golog as a "universe"
        #all simplecies should be child nodes of gologNode
        self.gologNode = self.render.attachNewNode("golog")
        self.sSet = hcat.simpSet(label = "golog", data = {'node':self.gologNode})


        self.sphere = self.loader.loadModel("models/misc/sphere")
        #self.sphere.reparentTo(self.gologNode)

        a = self.createObject(setPos = (0,0,0),label = 'a')
        b = self.createObject(setPos = (5,0,0),label = 'b')
        c = self.createObject(setPos = (5,0,5),label = 'c')
        #
        f = self.createMorphism((b,a),label = 'f')
        g = self.createMorphism((c,b),label = 'g')

        #self.taskMgr.add(lambda t: self.obMoverTask(b,t), "mover task")
        #self.taskMgr.add(lambda t: self.morMoverTask(f,t),"moverTask")
        self.taskMgr.add(self.cameraTask,"camera Task")
        #self.sphere.ls()

    #create a new simplex an bind graphics
    #pass graphics attributes and simplex kwargs
    def createObject(self, *args, **kwargs):
        numsimps = len(self.sSet.rawSimps)

        #create a simplex in the simplicial set
        simplex = self.sSet.add(0,*args, **kwargs)

        #create an instance of simplex graphics in golog, send to simplex.data['gr']
        simplexGr = self.render.attachNewNode(simplex.label+" Node")
        simplex.data['gr'] = simplexGr
        self.sphere.instanceTo(simplexGr)

        defaults = {'setPos':(2*numsimps,0,0)}
        for key in defaults.keys():
            if key in kwargs.keys(): getattr(simplexGr,key)(kwargs[key])
            else: getattr(simplexGr,key)(defaults[key])
        #simplexGr.ls()
        return simplex

    def createMorphism(self, faces, *args, **kwargs):
        dom = faces[1]
        codom = faces[0]
        simplex = self.sSet.add(faces,*args,**kwargs)
        simplexGr = Rope()
        middlenode = simplexGr.attachNewNode("middlenode")
        middlenode.setPos((dom.data['gr'].getPos()+codom.data['gr'].getPos())/2)

        #set start and endpoint to be the domain and codomain graphics

        simplexGr.setup(3,[(dom.data['gr'],(0,0,0)),
                    (middlenode,(0,0,0)),
                    (codom.data['gr'],(0,0,0))])
        simplexGr.reparentTo(self.render)
        simplex.data['gr'] = simplexGr
        print(simplexGr.getPoints(3))
        return simplex


    def obMoverTask(self,ob,task):
        t = task.time
        curve = lambda t: Point3(5+3*sin(10*t),0,3*sin(10*t))
        ob.data['gr'].setPos(curve(t))
        return task.cont

    def morMoverTask(self,mor,task):
        t = task.time
        curve = lambda t: Point3(5+3*sin(10*t),0,3*sin(10*t))
        #get middlenode
        mor.data['gr'].getChild(0).setPos(curve(t))
        return task.cont


    def cameraTask(self, task):
        t = task.time
        self.camera.setPos(50*cos(t),50*sin(t),0)
        self.camera.lookAt(self.sSet.rawSimps[0].data['gr'])
        return task.cont

app = golog()
app.run()
