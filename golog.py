from math import pi, sin, cos, floor

import sys, os
import hcat
import tkinter
from direct.showutil.Rope import Rope
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath, Camera, TextNode, Filename
from panda3d.core import Vec3, Point3, LPoint3f, Plane
from panda3d.core import CollisionPlane, CollisionRay, CollisionSphere
from panda3d.core import CollisionNode, CollisionTraverser, CollisionHandlerQueue


#golog is an extension to a simplicial set that provides graphics functionality via the panda3d library
#The main object is a Graphics_Data, A graphics data is a subset of a panda3d scenegraph with some messenger functionality
#explicitly: a golog is a panda scene graph and an hcat sSet with a mapping from Graphics Data to Simplecies

Camera_Distance = 100

#A Graphics Data Houses panda3d information for a simplex
# Any Nodes the simplex might have
# Any Extra graphics objects (for example ropes for 1-simplecies or planes for 2-simplecies)
# Lists of children and parents
# A messenger to handle any calls to children and from parent
# keeps a list of graphics_kwargs to recreate itself (used in gexport)
class Graphics_Data():
    def __init__(self, golog, simplex, **kwargs):
        self.simplex = simplex
        self.golog = golog
        self.messenger = self.golog.base.messenger
        self.listener = DirectObject() # might let Graphics_Data Inherit from Direct_Object
        self.graphics_kwargs = dict() # keeping track of information needed to re-create graphics_data

        #things to clean self for deletion:
        self.node_list = []
        self.listeners = [self.listener]

        if simplex.level == 0:
            self.NP = golog.render.attachNewNode(simplex.label)
            self.node_list.append(self.NP)
            self.NP.setTag('level','0') # to tell mode_heads what type of simplex this is
            golog.sphere.instanceTo(self.NP)
            self.collision = self.NP.attachNewNode(CollisionNode('sphereColNode'))
            self.collision.node().addSolid(CollisionSphere(0,0,0,1))
            self.messenger_names = {'node':str(id(self.NP))}


            #detail parents
            self.parents = () #need to give no parents for a unified update function

            self.parent_pos_convolution = lambda *x: golog.render.getPos() # function of parent's [node] positions to detail offset (0-simlex it's just render location)
            #listener for parental updates, pass arguemnts through extraKwargs to detail what kind of update to perform
            for parent in self.parents: self.listener.accept(self.parents.messenger_names['node'],self.update)
            
            #set position
            if 'pos' in kwargs.keys():self.update({'pos':kwargs['pos']})
            else: self.update({'pos':LPoint3f(0,0,0)})

        elif simplex.level == 1:
            self.NP = golog.render.attachNewNode(simplex.label)
            self.node_list.append(self.NP)
            self.NP.setTag('level','1')
            self.golog.cone.instanceTo(self.NP)
            self.collision = self.NP.attachNewNode(CollisionNode('coneColNode'))
            self.collision.node().addSolid(CollisionSphere(0,0,0,1))
            self.messenger_names = {'node':str(id(simplex))}
            self.graphics = (Rope(),Rope()) #two ropes :)
            for rope in self.graphics: self.node_list.append(rope)




            #set up parents
            self.parents = tuple(golog.Simplex_to_Graphics[face] for face in self.simplex.faces)
            def tuple_avg(tuples):
                b = LPoint3f(0,0,0)
                for a in tuples:
                    b = b+a
                return b/len(tuples)
            self.parent_pos_convolution = lambda *x: tuple_avg(tuple(parent.NP.getPos() for parent in self.parents))
            for parent in self.parents: self.listener.accept(parent.messenger_names['node'],self.update)


            if 'pos' in kwargs.keys():
                if isinstance(kwargs['pos'],tuple): pos = LPoint3f(*kwargs['pos'])
                else: pos = kwargs['pos']
            else: pos = LPoint3f(0,0,0)
            self.graphics_kwargs['pos'] = pos

            #create shitty control nodes for rope module (I know, this is not pretty)
            self.control_nodes = (self.golog.render.attachNewNode(simplex.label+'_control_node0'),self.golog.render.attachNewNode(simplex.label+'_control_node1'))
            for node in self.control_nodes: self.node_list.append(node)
            control_listener = DirectObject()
            self.listeners.append(control_listener)

            def control_updator(*x):
                for i in [0,1]:
                    self.control_nodes[i].setPos(self.graphics_kwargs['pos']+self.parents[i].NP.getPos())
            control_updator()
            control_listener.accept(self.messenger_names['node'], control_updator)

            self.update({'pos':None})

            #set up rope graphics
            self.graphics[0].setup(3,[ (self.NP,(0,0,0)),(self.control_nodes[0],(0,0,0)), (self.parents[0].NP,(0,0,0)) ])
            self.graphics[1].setup(3,[ (self.parents[1].NP,(0,0,0)),(self.control_nodes[1],(0,0,0)), (self.NP,(0,0,0)) ])
            for rope in self.graphics: rope.reparentTo(golog.render)

        #set up dictionary references
        self.golog.Simplex_to_Graphics[simplex] = self
        self.golog.Graphics_to_Simplex[self] = simplex
        self.golog.NP_to_Graphics[self.NP] = self
        #create an invisible textNode that can be shown if called
        text = TextNode(self.simplex.label+'_text_node')
        #? make this wrap if too long
        text.setText(self.simplex.label)
        text.setCardDecal(True)
        text.setCardColor(.5, 1, .5, 1)
        text.setCardAsMargin(0, 0, 0, 0)
        text.setTextColor(0,0,0,1)
        self.textNP = self.NP.attachNewNode(text)
        #? make this update to always be in front of camera
        # - Either get it into 2d plane, or make a z axis that always faces the camera and attach to that
        self.textNP.setPos(0,-1,0)
        self.textNP.show()
        self.node_list.append(self.textNP)

    #function that cleans up references and listeners for deletion
    #!!! THIS SHOULD NOT BE CALLED UNLESS DELETING UNDERLYING SIMPLEX AS WELL !!!#
    def _remove(self):
        #first should clean the nodes it supports (done through hcat)
        simplex = self.simplex
        supports = [*simplex.supports]
        for simp in supports:
            self.golog.Simplex_to_Graphics[simp]._remove()

        #delete listeners
        for listener in self.listeners:
            listener.ignoreAll()
            del listener

        #delete relevant nodes
        for node in self.node_list:
            node.removeNode()

        #delete dictionary references
        del self.golog.Simplex_to_Graphics[simplex]
        del self.golog.Graphics_to_Simplex[self]
        del self.golog.NP_to_Graphics[self.NP]

        #remove simplex from sSet
        self.golog.sSet.remove(simplex)







    #listener calls update with some data
    def update(self,kwargs):
            if 'pos' in kwargs:
                #if an offset is provided, change the graphics_kwargs, if not, leave them
                if kwargs['pos']: self.graphics_kwargs['pos'] = kwargs['pos']
                newpos = self.parent_pos_convolution() + self.graphics_kwargs['pos'] #set a new offset base on parent positions
                self.NP.setPos(newpos)
                self.messenger.send(self.messenger_names['node'], [{'pos':None}])


    #supress attribute errors
    def __getattr__(self, attr):
        return None



#a golog is essentially just a sSet with a bijection from graphics data to simplecies
#Golog = ( sSet, {Graphics_Data}, Simplex_to_Graphics = Graphics_to_Simplex^(-1) )
class golog():
    def __init__(self,base,*args, label = 'golog', model_path = os.path.abspath('./misc_data/models/'),  **kwargs):
        self.base = base

        #initialize with an empty nodepath and no window
        #initialize a golog with no relative path (shouldn't be able to open files without one though)
        defaults = {'render':'NodePath(label+\"_render\")'}
        for key in defaults:
            if key in kwargs: setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

        self.Simplex_to_Graphics = dict()
        self.Graphics_to_Simplex = dict()
        self.NP_to_Graphics = dict()
        
        # Initialize simplicial set
        self.label = label
        self.sSet = hcat.simpSet(label = self.label, data = {'node':self.render})
        self.sSet.simplex_to_graphics = dict()
        self.sSet.data['export_tag'] = 'golog'

        self.NPtoSimplex = dict()


        # set up camera
        self.camNode = Camera(label+"camNode")
        self.camera = self.render.attachNewNode(self.camNode)
        self.camera.setPos(0,-Camera_Distance,0)




        # Load Models
        self.sphere = self.base.loader.loadModel( Filename.fromOsSpecific(os.path.join(model_path,"sphere.egg.pz")))
        self.cone = self.base.loader.loadModel( Filename.fromOsSpecific(os.path.join(model_path,"sphere.egg.pz")))
        self.cone.setScale(.6)

        #set up collision traverser
        #? move to mode_head?
        self.cTrav = CollisionTraverser(self.label+'_traverser')

    def text_preview_set(self, bool):
        if bool == True:
            for simplex in self.sSet.rawSimps:
                if simplex in self.Simplex_to_Graphics.keys():
                    self.Simplex_to_Graphics[simplex].textNP.show()

        elif bool == False :
            for simplex in self.sSet.rawSimps:
                if simplex in self.Simplex_to_Graphics.keys():
                    self.Simplex_to_Graphics[simplex].textNP.hide()

    def add(self, ob ,*args, **kwargs):
        #add a simplex to the underlying simplicial set
        #see hcat for reference
        # can be :
        #integer:   create n-simplex
        #tuple:     create n-simplex (with faces)
        #see hcat.sSet.add for more
        simplex = self.sSet.add(ob, *args, **kwargs)
        Graphics_Data(self, simplex,*args, **kwargs)

        return simplex

if __name__ == "__main__":
    from direct.showbase.ShowBase import ShowBase
    class runner(ShowBase):
        def __init__(self):
            ShowBase.__init__(self)
            self.disable_mouse()


            # need to migrate into gologToWindow
            base.accept("f5",sys.exit)
            base.accept("f6",sys.exit)


            G = golog(base, label = 'run')
            self.win.getDisplayRegion(1).setCamera(G.camera)
            a = G.add(0,label = '1')
            b = G.add(0,label = '2',pos = LPoint3f(0,0,10))
            f1 = G.add((b,a), label = '(1,2)1', pos = LPoint3f(-2,0,0))
            f2 = G.add((b,a), label = '(1,2)2', pos = LPoint3f(-1,0,0))
            f3 = G.add((b,a), label = '(1,2)3', pos = LPoint3f(1,0,0))
            f4 = G.add((b,a), label = '(1,2)4', pos = LPoint3f(2,0,0))
            self.G = G
            self.list = [a,b,f1]


   



    r = runner()
    meta_golog = r.consolidate(r.list, r.G)

