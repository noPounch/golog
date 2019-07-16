from sys import exit
import os
from math import sin,cos
from golog_export import gexport
import time
import hcat
import golog
import window_manager
import tk_funcs
from direct.showbase.DirectObject import DirectObject
from panda3d.core import TextNode, TextFont
from panda3d.core import Camera, NodePath, OrthographicLens
from panda3d.core import Vec3, Point3
from panda3d.core import Plane, CollisionPlane, CollisionRay, CollisionNode, CollisionTraverser, CollisionHandlerQueue

########### ??? Quest Log ??? ###########
# - Fix latex folder creation issues (check under open_math_data)

#functionality for updating a simplex's math_data

def open_math_data(math_data):
    if math_data.type == 'golog':
        base = math_data().base
        controllable_golog = mode_head(base, math_data())
        controllable_golog.selection_and_creation()
        window_manager.modeHeadToWindow(base, controllable_golog)
    if math_data.type == 'file':
        file_name, file_extension = os.path.splitext(math_data())
        print(file_name, file_extension)
        if file_extension == '.txt':
            tk_funcs.edit_txt(math_data())
        else:
            #prompt user to select a program
            tk_funcs.run_program('',math_data())
    if math_data.type == 'latex':
        #??? Quest Log ???
        #? allow creating of folder in selection panel
        #? select actual folder
        #? relabel simplex by selected folder name

        pdf_file = None; tex_file = None
        if os.path.exists(math_data()['folder']+'/'+math_data()['name']+'.pdf'): pdf_file = math_data()['folder']+'/'+math_data()['name']+'.pdf'
        if os.path.exists(math_data()['folder']+'/'+math_data()['name']+'.tex'): tex_file = math_data()['folder']+'/'+math_data()['name']+'.tex'
        #make a tk box with two buttons which are enabled iff file exists
        tk_funcs.pdf_or_tex(pdf_file,tex_file)



def update_math_data(simplex, math_data_type, **kwargs):
    if 'label' in kwargs: simplex.label = kwargs['label']

    if math_data_type == 'None':
        simplex.math_data = hcat.Math_Data(type = 'None')

    if math_data_type == 'golog':
        new_golog = golog.golog(kwargs['base'], label = kwargs['label']) #create a new golog
        def newopen(): #create an open function for the golog math data
            controllable_golog = mode_head(kwargs['base'], simplex.math_data())
            controllable_golog.selection_and_creation()
            window_manager.modeHeadToWindow(kwargs['base'], controllable_golog)
        simplex.math_data = hcat.Math_Data(math_data = new_golog, type = 'golog')

    if math_data_type == 'file':
        file_location = tk_funcs.ask_file_location()
        if not file_location: return #if user cancels
        file_name, file_extension = os.path.splitext(file_location)
        simplex.math_data = hcat.Math_Data(math_data = file_location, type = 'file')
        #? add handler for if user exits text editor
        #? make asynchronous

    if math_data_type == 'latex':
        #??? Quest Log ???
        # - choose a folder
        # -- allow for creation of folder
        # - if there is a tex document or pdf under correct name, just inherit it

        folder_location = os.path.join(tk_funcs.ask_folder_location(initial_dir = os.path.abspath('./save')),simplex.label)
        #ensure folder exists
        if not os.path.exists(folder_location):
            os.mkdir(folder_location)
        #ensure tex file exists
        if not os.path.exists(os.path.join(folder_location,simplex.label+'.tex')):
            open(os.path.join(folder_location,simplex.label+'.tex'),'w').close()

        file_dict = {'name':simplex.label, 'folder':folder_location}
        simplex.math_data = hcat.Math_Data(math_data = file_dict, type = 'latex')


    return simplex.math_data



class mode_head():
    def __init__(self,base,Golog, save_location = 'save/test.golog'):
        # Set up basic attributes
        self.base = base
        self.golog = Golog
        self.buttons = dict()
        self.window_tasks = []
        self.listener = DirectObject()
        self.save_location = save_location
        ######

        #create a 2d render
        self.render2d = NodePath('2d render')
        self.camera2D = self.render2d.attachNewNode(Camera('2d Camera'))
        self.camera2D.setDepthTest(False)
        self.camera2D.setDepthWrite(False)
        lens = OrthographicLens()
        lens.setFilmSize(2, 2)
        lens.setNearFar(-1000, 1000)
        self.camera2D.node().setLens(lens)
        ######


        # make a dictionary of mode_heads in the underlying golog
        if hasattr(self.golog,'mode_heads'):
            m = 0
            while m in self.golog.mode_heads.keys(): m+=1 #get smallest unused mode_head index
            self.index = m
            self.label = self.golog.label+"_mode_head_"+str(self.index)
            self.golog.mode_heads[self.index] = self

        else:
            self.golog.mode_heads = dict()
            self.index = 0
            self.label = self.golog.label+"_mode_head_"+ str(self.index)
            self.golog.mode_heads[self.index] = self
        ##########


        # set up a reset function
        #if mode_head reset function, should be set at the end of every mode
        self.reset = self.basic_reset

    #basic reset functionality
    def basic_reset(self,*args):
        self.buttons = dict()
        self.window_tasks = dict()
        self.listener.ignoreAll()

    #cleans mode_head to preparte for garbage collecting.
    def clean(self):
        self.reset()
        del self.golog.mode_heads[self.index]
        del self.reset


    def get_relevant_entries(self, mw):
        # get list of entries by distance
        if not mw.node().hasMouse(): return
        mpos = mw.node().getMouse()
        self.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY()) #mouse ray goes from camera through the 'lens plane' at position of mouse
        self.golog.cTrav.traverse(self.golog.render)
        self.queue.sortEntries()

        # get the first relevant node traversed by mouseRay
        #### ignore everything with a mode_head tag that is not defined by this mode_head
        for e in self.queue.getEntries():
            if e.getIntoNodePath().getParent().hasTag("mode_head"):
                if e.getIntoNodePath().getParent().getTag("mode_head") == self.label:
                    return (e.getIntoNodePath().getParent(), e.getIntoNodePath().getParent().getTag("mode_node"),e.getSurfacePoint(e.getIntoNodePath()))
                    break
            else:
                entry = e
                break
        #############

        #return node selected in the golog
        entryNP = entry.getIntoNodePath().getParent()
        if entryNP.hasTag('level'): return (entryNP, entryNP.getTag('level'),entryNP.getPos())




    #basic mode for selecting and creating simplecies
    ################ CONTROLS #########################################
    #   mouse_over: display label and mata_data_type                  #
    #   left click: select simplex.                                   #
    #   selecting two 0-simplecies creates a 1-simplex                #
    #   right click: create simplex                                   #
    #   dialog box pops up prompting for default labels and math_data #
    #   space with mouse over simplex: open math_data                 #
    #   u with mouse over simplex: update meta_data                   #
    #   s saves golog to a .golog file (using hcat_funcs.gexport)     #
    ###################################################################

    def selection_and_creation(self):

        #Collision Handling
        #set up traverser and handler
        self.queue = CollisionHandlerQueue()
        self.selected = [[],[]] #tracking previously selected nodes of each level

        # set up mouse picker
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.golog.camera.attachNewNode(self.pickerNode) #attach collision node to camera
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.pickerNode.set_into_collide_mask(0) #so that collision rays don't collide into each other if there are two mode_heads
        self.golog.cTrav.addCollider(self.pickerNP,self.queue) #send collisions to self.queue
        # set up plane for picking
        self.planeNode = self.golog.render.attachNewNode("plane")
        self.planeNode.setTag("mode_head",self.label) # tag to say it belongs to this mode_head
        self.planeNode.setTag("mode_node", 'plane')

        self.planeFromObject = self.planeNode.attachNewNode(CollisionNode("planeColNode"))
        self.planeFromObject.node().addSolid(CollisionPlane(Plane(Vec3(0,-1,0),Point3(0,0,0))))

        #2d Text
        self.textNP = self.render2d.attachNewNode(TextNode('text node'))
        self.textNP.setScale(.1)
        self.textNP.setPos(-1+.2,0,-1+.2)






        def mouse1(mw):
            (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)

            if node_type == 'plane':
                for node in self.selected[0]: node.setColorScale(1,1,1,1) #turn white
                self.selected = [[],[]]
            elif node_type == '0':
                if entryNP not in self.selected[0]:
                    #?  don't just append, re-sort
                    self.selected[0].append(entryNP)
                entryNP.setColorScale(1,0,0,0) #turn red

            if len(self.selected[0]) == 2:
                # NP -> graphics -> simplex
                faces = tuple([self.golog.Graphics_to_Simplex[self.golog.NP_to_Graphics[faceNP]] for faceNP in self.selected[0][-1:-3:-1]])
                asked_list = tk_funcs.ask_math_data('1-simplex')
                if not asked_list: #[label, math_data_type,]
                    return
                simplex = self.golog.add(faces, label = asked_list[0]) #reversed selected objects and creates a 1 - simplex from them
                update_math_data(simplex, asked_list[1], base = self.base, label = asked_list[0])
                for node in self.selected[0]: node.setColorScale(1,1,1,1)
                self.selected[0] = [] #reset selected


            #?  do something with selected 1 simplecies (i.e. selected[1])
        def space(mw):
            (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)

            # if spaced on a 0 simplex, open it's math data, or create it
            if node_type in ['0','1']:
                simplex = self.golog.Graphics_to_Simplex[self.golog.NP_to_Graphics[entryNP]]
                if not simplex.math_data():
                    asked_list = tk_funcs.ask_math_data(simplex.label)
                    if not asked_list:
                        return
                    update_math_data(simplex, math_data_type = asked_list[1], base = self.base, label = asked_list[0])
                    # open_math_data(simplex.math_data)
                    #? for future asynchronounisity
                    #self.base.taskMgr.add(open_math_data,'asynch open task', extraArgs = [simplex.math_data])

                else:
                    open_math_data(simplex.math_data)

        def u(mw):
            (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)
            if node_type in ['0','1']:
                simplex = self.golog.Graphics_to_Simplex[self.golog.NP_to_Graphics[entryNP]]
                asked_list = tk_funcs.ask_math_data(simplex.label)
                if not asked_list:
                    return
                update_math_data(simplex, math_data_type = asked_list[1], base = self.base, label = asked_list[0])

        def mouse3(mw):

            (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)

            if node_type == 'plane':
                for node in self.selected[0]: node.setColorScale(1,1,1,1) #turn white
                self.selected = [[],[]]
                asked_list = tk_funcs.ask_math_data('0-Simplex')
                if not asked_list:
                    return #if canceled, do not create a simplex
                simplex = self.golog.add(0, pos = entry_pos, label = asked_list[0]) #create a simplex
                update_math_data(simplex, math_data_type = asked_list[1], base = self.base, label = asked_list[0])
                # open_math_data(simplex.math_data)




        def mouse_watch_test(mw,task):
            if not mw.node().hasMouse():return task.cont
            (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)

            if node_type == '0':
                simplex =  self.golog.Graphics_to_Simplex[self.golog.NP_to_Graphics[entryNP]]
            elif node_type == '1':
                #? again consider what needs to be shown with 1-simplecies
                simplex =  self.golog.Graphics_to_Simplex[self.golog.NP_to_Graphics[entryNP]]
            else:
                self.textNP.hide()
                return task.cont

            self.textNP.show()
            self.textNP.node().setText("label: " +simplex.label+"\n math data type: " + simplex.math_data.type)
            # self.textNP.setPos(mpos.getX(),0,mpos.getY())
            return task.cont

        def save(mw):
            # print(os.path.abspath(os.path.dirname(__file__))+'/'+self.save_location)
            save_location = tk_funcs.ask_file_location(initial_dir = os.path.abspath(os.path.dirname(__file__))+'/'+self.save_location)
            print('saving to:\n'+save_location)
            gexport(self.golog, save_location)


        def reset(*args):
            self.golog.cTrav.removeCollider(self.pickerNP)
            del self.queue
            for node in self.selected: node.setColorScale(1,1,1,1)
            del self.selected
            del self.pickerNode
            self.pickerNP.removeNode()
            del self.pickerRay
            self.planeNode.removeNode()
            self.planeFromObject.removeNode()
            self.buttons = dict()
            self.window_tasks = []
            self.listener.ignoreAll()
            # print(self.label+ " reset")
            self.reset = self.basic_reset

        self.reset = reset
        self.buttons = {'mouse1':mouse1,'mouse3':mouse3, 'space':space, 'escape':self.reset, 's':save, 'u':u}
        self.window_tasks = [mouse_watch_test]
