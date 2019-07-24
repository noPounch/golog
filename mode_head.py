from sys import exit
import os
from math import sin,cos
from golog_export import gexport
from shutil import copyfile
import time, hcat, golog, window_manager, tk_funcs
#panda imports
from direct.showbase.DirectObject import DirectObject
from panda3d.core import TextNode, TextFont
from panda3d.core import Camera, NodePath, OrthographicLens
from panda3d.core import Vec3, Point3
from panda3d.core import Plane, CollisionPlane, CollisionRay, CollisionNode, CollisionTraverser, CollisionHandlerQueue

########### ??? Quest Log ??? ###########
# - Fix latex folder creation issues (check under open_math_data)

#functionality for updating a simplex's math_data




class mode_head():
    def __init__(self,base,Golog, folder_path):
        # Set up basic attributes
        self.base = base
        self.golog = Golog
        self.buttons = dict()
        self.window_tasks = dict()
        self.bt = None
        self.mw = None
        self.listener = DirectObject()
        self.folder_path = folder_path
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

    def open_math_data(self,math_data):
        if math_data.type == 'golog':

            subgolog_folder_path = os.path.join(self.folder_path,'subgologs')
            if not os.path.exists(subgolog_folder_path): os.mkdir(subgolog_folder_path)
            controllable_golog = mode_head(self.base, simplex.math_data(), subgolog_folder_path)
            controllable_golog.selection_and_creation()
            window_manager.modeHeadToWindow(self.base, controllable_golog)

        if math_data.type == 'file':
            file_name, file_extension = os.path.splitext(math_data()[-1])
            print(file_name, file_extension)
            if file_extension == '.txt':
                tk_funcs.edit_txt(os.path.join(self.folder_path,*math_data()))
            else:
                #prompt user to select a program
                print(math_data())
                print(os.path.join(self.folder_path,*math_data()))
                tk_funcs.run_program('',os.path.join(self.folder_path,*math_data()))
        if math_data.type == 'latex':
            file_dict = math_data()
            tex_folder = os.path.join(os.path.abspath(self.folder_path),*file_dict['folder'])
            tex_file = os.path.join(os.path.abspath(self.folder_path),*file_dict['tex'])




            if 'pdf' in file_dict.keys():
                pdf_file = os.path.join(self.folder_path, *file_dict['pdf'])
            elif os.path.exists(tex_file.split('.tex')[0]+'.pdf'): #if there is a pdf in the folder with the same name
                file_dict['pdf'] = file_dict['tex']
                file_dict['pdf'][-1] = file_dict['pdf'][-1].split('.tex')[0]+'.pdf' #change extension to .pdf
                pdf_file = os.path.join(self.folder_path, *file_dict['pdf'])
            else: pdf_file = None


            tk_funcs.pdf_or_tex(pdf_file, tex_file)





    def update_math_data(self,simplex, math_data_type, **kwargs):
        if 'label' in kwargs: simplex.label = kwargs['label']

        if math_data_type == 'None':
            simplex.math_data = hcat.Math_Data(type = 'None')

        if math_data_type == 'golog':
            new_golog = golog.golog(self.base, label = kwargs['label']) #create a new golog
            simplex.math_data = hcat.Math_Data(math_data = new_golog, type = 'golog')

        if math_data_type == 'file':
            if not os.path.exists(os.path.join(self.folder_path,'files')): os.mkdir(os.path.join(self.folder_path,'files'))
            file_folder_path = ['files']

            file_location = tk_funcs.ask_file_location()
            if not file_location: return #if user cancels
            file_name = os.path.split(file_location)[1] #file name with extension
            file_path = tk_funcs.unique_path(os.path.join(self.folder_path),[*file_folder_path, file_name]) #get a unique file path starting from the file_folder
            copyfile(file_location, os.path.join(self.folder_path,*file_path))
            simplex.math_data = hcat.Math_Data(math_data = file_path, type = 'file')
            #? add handler for if user exits text editor
            #? make asynchronous

        if math_data_type == 'latex':
            #ensure latex folder exists
            if not os.path.exists(os.path.join(self.folder_path,'latex')): os.mkdir(os.path.join(self.folder_path,'latex'))

            # create a uniquely named folder in self.folder_path/latex/ based on simplex.label
            tex_folder_path = tk_funcs.unique_path(root = self.folder_path, path = ['latex',simplex.label])
            print(tex_folder_path)
            os.mkdir(os.path.join(self.folder_path, *tex_folder_path))
            #create a tex file in tex folder
            tex_file_path = [*tex_folder_path, simplex.label+'.tex']
            # ask if want new or to load one
            location = tk_funcs.load_tex(self.folder_path)
            # if new, returns True and makes a new tex file below
            # if load, returns a path and copies the path into tex_file_path
            true_path = os.path.join(self.folder_path,*tex_file_path)
            if location == True: open(   true_path  , 'w').close()
            if isinstance(location, str): copyfile(location, true_path)

            # make a file dictionary with just tex file in it
            file_dict = {'tex':tex_file_path, 'folder':tex_folder_path}
            simplex.math_data = hcat.Math_Data(math_data = file_dict, type = 'latex')


        return simplex.math_data

    def setup_window_events(self,bt=None,mw=None):
        if bt: self.bt = bt
        if mw: self.mw = mw
        if not self.bt: return
        if not self.mw: return
        self.listener.ignoreAll()
        for button in self.buttons.keys():
            self.listener.accept(bt.prefix+button, self.buttons[button], extraArgs = [self.mw])

    def setup_window_tasks(self,mw = None):
        if mw: self.mw = mw
        if not self.mw: return
        for window_task in self.window_tasks.keys():
            base.taskMgr.add(self.window_tasks[window_task], window_task, extraArgs = [self.mw], appendTask = True)
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
            elif node_type == '0':# and set(selected[1:]) = {[]}:
                if entryNP not in self.selected[0]:
                    #?  don't just append, re-sort
                    self.selected[0].append(entryNP)
                entryNP.setColorScale(1,0,0,0) #turn red

            if len(self.selected[0]) == 2:
                # NP -> graphics -> simplex
                faces = tuple([self.golog.Graphics_to_Simplex[self.golog.NP_to_Graphics[faceNP]] for faceNP in self.selected[0][-1:-3:-1]])
                asked_list = tk_funcs.ask_math_data('1-Simplex')
                if not asked_list: #[label, math_data_type,]
                    return
                simplex = self.golog.add(faces, label = asked_list[0]) #reversed selected objects and creates a 1 - simplex from them
                self.update_math_data(simplex, asked_list[1], label = asked_list[0])
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
                    self.update_math_data(simplex, math_data_type = asked_list[1], label = asked_list[0])
                    #? make asynchronous


                else:
                    self.open_math_data(simplex.math_data)

        def u(mw):
            (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)
            if node_type in ['0','1']:
                simplex = self.golog.Graphics_to_Simplex[self.golog.NP_to_Graphics[entryNP]]
                asked_list = tk_funcs.ask_math_data(simplex.label)
                if not asked_list:
                    return
                self.update_math_data(simplex, math_data_type = asked_list[1], label = asked_list[0])

        def mouse3(mw):

            (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)

            if node_type == 'plane':
                for node in self.selected[0]: node.setColorScale(1,1,1,1) #turn white
                self.selected = [[],[]]
                asked_list = tk_funcs.ask_math_data('0-Simplex')
                if not asked_list:
                    return #if canceled, do not create a simplex
                simplex = self.golog.add(0, pos = entry_pos, label = asked_list[0]) #create a simplex
                self.update_math_data(simplex, math_data_type = asked_list[1], label = asked_list[0])


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
            save_location = tk_funcs.ask_file_location(initial_dir = self.folder_path)
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
            self.reset = self.basic_reset

        self.reset = reset
        self.buttons = {'mouse1':mouse1,'mouse3':mouse3, 'space':space, 'escape':self.reset, 's':save, 'u':u}
        self.setup_window_events()

        self.window_tasks = {'mouse_watch_test':mouse_watch_test}
        self.setup_window_tasks()
