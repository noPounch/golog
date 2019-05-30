from math import pi, sin, cos, floor

import sys
import hcat
import tkinter
from direct.showutil.Rope import Rope
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, LPoint3f
from pandac.PandaModules import *

#globals
Camera_Distance = 30



class golog(ShowBase):
    def __init__(self,*args, **kwargs):
        ShowBase.__init__(self)
        self.disableMouse()
        self.camera.setPos(0,-Camera_Distance,0)
        #create a golog, a dummy node represents the golog as a "universe"
        #all simplecies should be child nodes of gologNode
        self.gologNode = self.render.attachNewNode("golog")
        self.sSet = hcat.simpSet(label = "golog", data = {'node':self.gologNode})
        self.sphere = self.loader.loadModel("models/misc/sphere")

        self.accept('f5', sys.exit)
        self.accept('f6', sys.exit)
        self.accept("mouse1",self.mouse1handler)


        #self.sphere.reparentTo(self.gologNode)

        a = self.createObject(setPos = (0,0,0),label = 'a')
        b = self.createObject(setPos = (5,0,0),label = 'b')
        c = self.createObject(setPos = (5,0,5),label = 'c')
        #
        f = self.createMorphism((b,a),label = 'f')
        g = self.createMorphism((c,b),label = 'g')
        #self.taskMgr.add()
        #self.taskMgr.add(self.simpMoverTask, "mover task", extraArgs = [b,b.data['node'].getPos()], appendTask = True)
        #self.taskMgr.add(self.simpMoverTask, "mover task", extraArgs = [a,a.data['node'].getPos()], appendTask = True)

        #self.taskMgr.add(lambda t: self.morMoverTask(f,t),"moverTask")
        #self.taskMgr.add(self.cameraTask,"camera Task")
        #self.sphere.ls()


    def mouse1handler(self):
        x=self.mouseWatcherNode.getMouseX()
        z=self.mouseWatcherNode.getMouseY()
        print(x,z)
        s = self.createObject(setPos = LPoint3f(x*(Camera_Distance+1),0,z*(Camera_Distance+1))/3.14)
        self.taskMgr.add(self.simpMoverTask, "mover task", extraArgs = [s,s.data['node'].getPos()], appendTask = True)
    #create a new simplex an bind graphics
    #pass graphics attributes and simplex kwargs
    def createObject(self, *args, **kwargs):
        #create a simplex in the simplicial set
        simplex = self.sSet.add(0,*args, **kwargs)

        #create an instance of simplex graphics in golog, send to simplex.data['node']
        simplexGr = self.render.attachNewNode(simplex.label+" Node")
        simplex.data['node'] = simplexGr
        self.sphere.instanceTo(simplexGr)

        #create a messenger name for simplex (for now just rawSimps index)
        simplex.data['_messengerName'] = 'simp' + str(self.sSet.rawSimps.index(simplex))

        defaults = {'setPos':(0,0,0)}
        for key in defaults.keys():
            if key in kwargs.keys(): getattr(simplexGr,key)(kwargs[key])
            else: getattr(simplexGr,key)(defaults[key])
        #simplexGr.ls()
        print(simplexGr.getPos())
        #accept other calls
        ####
        self.accept('Update' + simplex.data['_messengerName'],self.updateSimp,[simplex])
        ####

        return simplex

    def updateSimp(self,simp,kwargs = dict()):
        #since the task manager doesn't let you pass kwargs, you have to pass a number and index by that number

        ####TODO: Make this method accept either kwargs or multiple args with some index

        # kwargs = dict()
        # for n in range(len(ntypes)): kwargs = kwargs + {inttokey[i]:}
        #
        #
        # kwargs = [{inttokey[i],} for i in ntypes]

        if 'pos' in kwargs:
            #update morphism to be average position of it's faces nodes + some offset passed through kwargs['pos']
            pos = kwargs['pos']
            n = len(simp.faces)
            for f in simp.faces: pos = pos + f.data['node'].getPos()/n #transform offset pos to offset from average of faces
            simp.data['node'].setPos(pos)
            self.messenger.send( simp.data['_messengerName']+' moved', [{'pos':Point3(0,0,0)}]) #sending (0,0,0) just updates the child nodes by default
            if simp.level > 0: print("yoyoyoyoyoy")

    def createMorphism(self, faces, *args, **kwargs):
        dom = faces[1]
        codom = faces[0]
        simplex = self.sSet.add(faces,*args,**kwargs)
        simplex.data['_messengerName'] = 'simp' + str(self.sSet.rawSimps.index(simplex))
        # offset for middlenode



        rope = Rope()
        middlenode = self.gologNode.attachNewNode("middlenode")
        simplex.data['node'] = middlenode
        middlenode.setPos((dom.data['node'].getPos()+codom.data['node'].getPos())/2)


        #create a middlenode listener for face movements
        ######
        for f in simplex.faces: self.accept(f.data['_messengerName'] + ' moved',self.updateSimp,[simplex])
        #####

        #create a listener for other events
        #####
        self.accept('Update' + simplex.data['_messengerName'],self.updateSimp,[simplex])
        #####

        #set start and endpoint to be the domain and codomain graphics
        rope.setup(3,[(dom.data['node'],(0,0,0)),
                    (simplex.data['node'],(0,0,0)),
                    (codom.data['node'],(0,0,0))])
        rope.reparentTo(self.gologNode)
        simplex.data['graphics'] = rope


        return simplex

    def simpMoverTask(self,simp,orig,task):
        t = task.time
        curve = lambda t: Point3(sin(10*t),sin(10*t),sin(10*t))
        self.updateSimp(simp, {'pos' : orig + curve(t)})
        return task.cont


    # def cameraTask(self, task):
    #     t = task.time
    #     self.camera.setPos(50*cos(t),50*sin(t),50*sin(t))
    #     self.camera.lookAt(self.sSet.rawSimps[0].data['graphics'])
    #     return task.cont

app = golog()
app.run()
