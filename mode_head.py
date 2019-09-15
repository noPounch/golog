from sys import exit
import os
from math import sin,cos
from webbrowser import open_new_tab
from golog_export import gexport
from shutil import copyfile
import time, hcat, golog, window_manager, tk_funcs
#panda imports
from direct.showbase.DirectObject import DirectObject
# from direct.showbase.InputStateGlobal import inputState
from panda3d.core import TextNode, TextFont
from panda3d.core import Camera, NodePath, OrthographicLens
from panda3d.core import Vec3, Point3
from panda3d.core import Plane, CollisionPlane, CollisionRay, CollisionNode, CollisionTraverser, CollisionHandlerQueue

#### Quests ####
#?  add a None option for folder_path
autosave = True



class mode_head():
    def __init__(self,base,Golog, folder_path, parent = None):
        # Set up basic attributes
        self.base = base
        self.golog = Golog
        self.bools = {'textboxes':True}
        self.buttons = dict()
        self.window_tasks = dict()
        self.bt = None
        self.mw = None
        self.listener = DirectObject()
        self.folder_path = folder_path
        self.file_path = os.path.abspath(self.folder_path + '/' + self.golog.label+ '.golog')
        self.has_window = False
        self.parent = parent #for autosaving up to original golog
        self.reset = self.basic_reset
        self.garbage = [] #list of deleted math_data/graphics_data etc.


        #create a 2d rende
        self.render2d = NodePath('2d render')
        self.camera2D = self.render2d.attachNewNode(Camera('2d Camera'))
        self.camera2D.setDepthTest(False)
        self.camera2D.setDepthWrite(False)
        lens = OrthographicLens()
        lens.setFilmSize(2, 2)
        lens.setNearFar(-1000, 1000)
        self.camera2D.node().setLens(lens)


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

        ### set up collision handling ###
        self.queue = CollisionHandlerQueue()

        ### set up selection tools
        self.create_list = [[],[]] #select nodes and add to create_list in order to create higher simplecies
        self.bools = {'selecter':False,'textboxes':True,'shift_clicked':False} #some bools that will be usefull


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
        ###
        # set up preview text
        self.textNP = self.render2d.attachNewNode(TextNode('text node'))
        self.textNP.setScale(.2)
        self.textNP.setPos(-1,0,0)
        self.textNP.show()
        #set up dragging info
        self.grabbed_dict = dict()
        self.drag_dict = dict() #a mapping from selected nodes to their original positions for dragging
        self.mouse_down_loc = (0,0,0)
        self.lowest_level = 3

    def open_math_data(self,math_data):
        if math_data.type == 'golog':
            golog_dict = math_data() #calls the mathdata (which is a golog_dict)
            subgolog = golog_dict['golog']
            subfolder_path = golog_dict['folder_path']

            #### just to be safe, but probably not needed
            subgolog_folder_path = os.path.join(self.folder_path,'subgologs')
            if not os.path.exists(subgolog_folder_path): os.mkdir(subgolog_folder_path)
            ####
            folder_path = os.path.join(self.folder_path, *golog_dict['folder_path'])
            controllable_golog = mode_head(self.base, subgolog, folder_path = folder_path, parent = self)
            window_manager.modeHeadToWindow(self.base, controllable_golog)

        if math_data.type == 'file':
            file_name, file_extension = os.path.splitext(math_data()[-1])
            # if file_extension == '.txt':
            #     tk_funcs.edit_txt(os.path.join(self.folder_path,*math_data()))
            # else:
                #prompt user to select a program
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

        if math_data.type == 'weblink':
            open_new_tab(math_data())

    def update_math_data(self,simplex, math_data_type, **kwargs):


        if autosave == True: self.save()

        if 'label' in kwargs: simplex.label = kwargs['label']
        self.golog.Simplex_to_Graphics[simplex].textNP.node().setText(simplex.label)
        self.golog.text_preview_set(self.bools['textboxes'])

        if simplex.math_data.type != 'None':
            answer = tk_funcs.are_you_sure('are you sure you want to delete the current math_data?')
            if answer == 'yes':
                self.delete_math_data(simplex)
            else: return
        if math_data_type == 'None':
            simplex.math_data = hcat.Math_Data(type = 'None')

        if math_data_type == 'golog':

            #create a path for all subgologs, if it doesn't already exist
            subgolog_folder_path = os.path.join(self.folder_path,'subgologs')
            if not os.path.exists(subgolog_folder_path): os.mkdir(subgolog_folder_path)




            new_golog = golog.golog(self.base, label = kwargs['label']) #create a new golog

            #create a unique folder path list in subgolog_folder_path
            unique_path = tk_funcs.unique_path(subgolog_folder_path,[kwargs['label']])
            new_folder_path = ['subgologs', *unique_path]
            os.mkdir(os.path.join(self.folder_path , *new_folder_path)) #make the directory as above
            #create a new golog save at new_folder_path/label.golog
            new_save_location = os.path.join(self.folder_path, *new_folder_path, kwargs['label']+'.golog')

            #new_save_location should be a subfolder of subgologs
            gexport(new_golog, new_save_location)

            #math data is a dictionary of the physical golog and it's relative save path list
            golog_dict = {'golog':new_golog, 'folder_path':new_folder_path}
            simplex.math_data = hcat.Math_Data(math_data = golog_dict, type = 'golog')

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
            os.mkdir(os.path.join(self.folder_path, *tex_folder_path))
            #create a tex file in tex folder
            tex_file_path = [*tex_folder_path, simplex.label+'.tex']
            # ask if want new or to load one
            location = tk_funcs.load_tex(self.folder_path)
            # if new, returns True and copies template tex file
            # if load, returns a path and copies the path into tex_file_path
            true_path = os.path.join(self.folder_path,*tex_file_path)
            if location == True: copyfile(os.path.abspath('./misc_data/config_files/template.tex'), true_path)

                #
                # open(   true_path  , 'w').close()
            if isinstance(location, str): copyfile(location, true_path)

            # make a file dictionary with just tex file in it
            file_dict = {'tex':tex_file_path, 'folder':tex_folder_path}
            simplex.math_data = hcat.Math_Data(math_data = file_dict, type = 'latex')

        if math_data_type == 'weblink':
            weblink = tk_funcs.ask_weblink()
            simplex.math_data = hcat.Math_Data(math_data = weblink, type = 'weblink')


        if math_data_type == 'text':
            #create a text file
            if not os.path.exists(os.path.join(self.folder_path,'files')): os.mkdir(os.path.join(self.folder_path,'files'))
            file_folder_path = ['files']
            file_path = tk_funcs.unique_path(root = self.folder_path, path = ['files',simplex.label+'.txt' ])
            with open(os.path.join(self.folder_path, *file_path),'w') as file: pass
            #create a math_data for it
            simplex.math_data = hcat.Math_Data(math_data = file_path, type = 'file')



        #save golog
        if autosave == True: self.save()
        return simplex.math_data

    def delete_math_data(self,simplex,**kwargs):
        simplex.math_data.delete(self.folder_path)
        simplex.math_data = hcat.Math_Data(type = 'None')

    def setup_window(self, windict):
        self.windict = windict
        for button in self.buttons.keys():
            self.listener.accept(self.windict['bt'].prefix+button, self.buttons[button], extraArgs = [self.windict['mw']])
        for window_task in self.window_tasks.keys():
            base.taskMgr.add(self.window_tasks[window_task], window_task, extraArgs = [self.windict['mw']], appendTask = True)
        self.has_window = True

    def save(self, *ask):
        #if has a parent, save the parent. If not, save itself
        if not self.parent: #if doesn't have a parent mode_head, save parent
        #if we pass something to ask it will ask (this includes mousewatchers)
            if ask:
                save_location = tk_funcs.ask_file_location(initial_dir = self.folder_path)
                if not save_location: return #if user cancels
                print('saving to:\n'+save_location)
                gexport(self.golog,  self.folder_path)
            else:
                gexport(self.golog,  self.file_path)

        else: self.parent.save()# if parent has no mode_head, save itself

    #basic reset function which shuts off the listener and removes button bindings. Should only be called if no "reset" function exists
    def basic_reset(self,*args):
        self.buttons = dict()
        self.window_tasks = dict()
        self.listener.ignoreAll()

    #function to call before deleting the mode_head, for example when closing a window
    def clean(self):
        self.reset()

        #close window
        if self.has_window == True:
            if hasattr(mode_head,'windict'):
                if 'win' in mode_head.windict.keys():
                    self.base.closeWindow(mode_head.windict['win'], keepCamera = True, removeWindow = True)
            self.has_window = False
        del self.golog.mode_heads[self.index]
        del self.reset

    # function to return the only the relevant collision data from the mouseRay
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

        #return node create_list in the golog
        entryNP = entry.getIntoNodePath().getParent()
        if entryNP.hasTag('level'): return (entryNP, entryNP.getTag('level'),entryNP.getPos())

    #function to 'pick up' a node by adding it to the dragged dictionary
    def pickup(self, mw):
        if not mw.node().hasMouse(): return
        (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)


        ### get position on plane for mouseloc
        mpos = mw.node().getMouse()
        self.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY()) #mouse ray goes from camera through the 'lens plane' at position of mouse
        self.golog.cTrav.traverse(self.golog.render)
        self.queue.sortEntries()
        for e in self.queue.getEntries():
            if e.getIntoNodePath().getParent().hasTag("mode_head"):
                if e.getIntoNodePath().getParent().getTag("mode_head") == self.label:
                    if e.getIntoNodePath().getParent().getTag("mode_node") == 'plane':
                        self.mouse_down_loc = e.getSurfacePoint(e.getIntoNodePath())
                        break


        #if selected node is in the drag_dict, use it to set a mouse location
        # if entryNP in self.drag_dict.keys(): self.mouse_down_loc = entryNP.getPos()

        if node_type in ['0','1']:
            self.grabbed_dict = {'graphics': self.golog.NP_to_Graphics[entryNP],'dragged':False,
                                                        'orig_pos': entryNP.getPos()}
        if node_type == 'plane':
            for node in self.create_list[0]: node.setColorScale(1,1,1,1) #turn white
            self.create_list = [[],[]]
            for node in self.drag_dict.keys():  node.setColorScale(1,1,1,1)
            self.drag_dict = dict()
            self.lowest_level = 3



    #function to 'put down' a node, returns true if it's dragged something
    def putdown(self, mw):
        for node in self.drag_dict.keys():
            self.drag_dict[node] = self.golog.NP_to_Graphics[node].graphics_kwargs['pos']
            self.lowest_level = min(self.lowest_level, int(node.getTag('level')))

        if 'dragged' in self.grabbed_dict.keys():
            if self.grabbed_dict['dragged'] == True:
                self.grabbed_dict = dict()
                return True
            self.grabbed_dict = dict()
    #function to select a node and add a 1-simplex between 2 create_list 0-simplecies
    def select_for_creation(self, mw):
        if not mw.node().hasMouse(): return
        #remove selected
        for node in self.drag_dict.keys():
            node.setColorScale(1,1,1,1)
        self.drag_dict = dict()
        self.lowest_level = 3

        ### selection ###
        (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)
        if node_type == '0':# and set(create_list[1:]) = {[]}:
            if entryNP not in self.create_list[0]:
                #?  don't just append, re-sort
                self.create_list[0].append(entryNP)
            entryNP.setColorScale(1,0,0,0) #turn red

        if len(self.create_list[0]) == 2:
            # NP -> graphics -> simplex
            faces = tuple([self.golog.Graphics_to_Simplex[self.golog.NP_to_Graphics[faceNP]] for faceNP in self.create_list[0][-1:-3:-1]])
            asked_list = tk_funcs.ask_math_data('1-Simplex')
            if not asked_list: #[label, math_data_type,]
                return
            simplex = self.golog.add(faces, label = asked_list[0]) #reversed create_list objects and creates a 1 - simplex from them
            self.update_math_data(simplex, asked_list[1], label = asked_list[0])
            for node in self.create_list[0]: node.setColorScale(1,1,1,1)
            self.create_list[0] = [] #reset create_list

    #open math_data of simplex under mouse
    def mouse_open(self, mw):
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

    # delete a simplex, prompt to delete the math_data and (recursively) it's supported simplecies
    def delete(self,mw):
        (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)
        if node_type in ['0','1']:
            #warning about deleting supported simplecies

            graphics = self.golog.NP_to_Graphics[entryNP]
            simplex = self.golog.Graphics_to_Simplex[graphics]

            if simplex.supports:
                answer = tk_funcs.are_you_sure(simplex.label+' still supports other simplecies. Are you sure you wish to delete?')
                if answer != 'yes': return

            self.delete_math_data(simplex)
            graphics._remove()

    #update the math_data of a simplex under the mouse
    def mouse_update(self, mw):
        (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)
        if node_type in ['0','1']:
            simplex = self.golog.Graphics_to_Simplex[self.golog.NP_to_Graphics[entryNP]]
            asked_list = tk_funcs.ask_math_data(simplex.label)
            if not asked_list:
                return
            self.update_math_data(simplex, math_data_type = asked_list[1], label = asked_list[0])

    #create a simplex given a mouse position
    def create(self, mw):
        (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)

        if node_type == 'plane':
            for node in self.create_list[0]: node.setColorScale(1,1,1,1) #turn white
            self.create_list = [[],[]]
            asked_list = tk_funcs.ask_math_data('0-Simplex')
            if not asked_list:
                return #if canceled, do not create a simplex
            simplex = self.golog.add(0, pos = entry_pos, label = asked_list[0]) #create a simplex
            self.update_math_data(simplex, math_data_type = asked_list[1], label = asked_list[0])

    #function which checks the drag dictionary and drags stuff
    def drag(self, mw):
        if self.grabbed_dict:


            #get mouse_loc
            mpos = mw.node().getMouse()
            self.pickerRay.setFromLens(self.golog.camNode,mpos.getX(),mpos.getY()) #mouse ray goes from camera through the 'lens plane' at position of mouse
            self.golog.cTrav.traverse(self.golog.render)
            self.queue.sortEntries()
            mouseloc = None
            for e in self.queue.getEntries():
                if e.getIntoNodePath().getParent().getTag("mode_node") == 'plane':
                    mouseloc = e.getSurfacePoint(e.getIntoNodePath())
                    break
            if not mouseloc:return

            self.bools['dragging'] = True


            #if nothing is selected, drag the thing below you
            if not self.drag_dict:
                offset = mouseloc - self.grabbed_dict['graphics'].parent_pos_convolution()
                delta = offset - self.grabbed_dict['orig_pos']
                norm = delta.getX()**2 +delta.getY()**2 +delta.getZ()**2
                if self.grabbed_dict['dragged'] == True or norm > 1:
                    self.grabbed_dict['dragged'] = True
                #if offset magnitude is greater than 1 or dragged == true, actually drag it
                if self.grabbed_dict['dragged'] == True: self.grabbed_dict['graphics'].update({'pos':offset})

            # if there is something in the drag dict:
            if self.drag_dict:
                self.grabbed_dict['dragged'] = True
                #only drag lowest dim simplecies
                for node in self.drag_dict.keys():
                    if int(node.getTag('level')) == self.lowest_level: self.golog.NP_to_Graphics[node].update({'pos':self.drag_dict[node]+mouseloc-self.mouse_down_loc})


    #send preview of math_data of simplex under the mouse
    def preview(self, mw):
        (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)

        if node_type == '0':
            simplex =  self.golog.Graphics_to_Simplex[self.golog.NP_to_Graphics[entryNP]]
        elif node_type == '1':
            #? again consider what needs to be shown with 1-simplecies
            simplex =  self.golog.Graphics_to_Simplex[self.golog.NP_to_Graphics[entryNP]]
        else: return

        # set preview up
        if self.has_window:
            if simplex.math_data.type == 'golog':
                self.windict['preview_dr'].setCamera(simplex.math_data()['golog'].camera)
            else:
                self.windict['preview_dr'].setCamera(self.camera2D)
                self.textNP.node().setText("label:\n" +simplex.label+"\n\n math data type:\n" + simplex.math_data.type)
        return

    #tool for selecting multiple simplecies
    def multi_select(self,mw):
        (entryNP, node_type, entry_pos) = self.get_relevant_entries(mw)
        #reset select and create
        if node_type in ['0','1']:
            if entryNP in self.drag_dict.keys():
                del self.drag_dict[entryNP]
                entryNP.setColorScale(1,1,1,1)
                self.lowest_level = min([int(node.getTag('level')) for node in self.drag_dict.keys()])
            else:
                self.drag_dict[entryNP] = self.golog.NP_to_Graphics[entryNP].graphics_kwargs['pos']
                entryNP.setColorScale(.5,.5,0,1)
                self.lowest_level = min(self.lowest_level, int(entryNP.getTag('level')))


    ########## BEGIN DEFINING MODES ##########

    #selection and creation mode
    def selection_and_creation(self, windict):
        def mouse1(mw):
            if not mw: return
            self.bools['shift_clicked'] = False
            self.pickup(mw)

        def shift_mouse1(mw):
            if not mw: return
            self.multi_select(mw)
            self.bools['shift_clicked'] = True

        def mouse1_up(mw):
            dropped_bool = self.putdown(mw)
            if self.bools['shift_clicked'] or dropped_bool:
                self.bools['shift_clicked'] = False
            else:
                self.select_for_creation(mw)




        def space(mw):
            if not mw: return
            self.mouse_open(mw)

        def u(mw):
            if not mw: return
            #?  do a change not just update
            self.mouse_update(mw)

        def mouse3(mw):
            if not mw: return
            self.create(mw)

        def backspace(mw):
            if not mw: return
            self.delete(mw)

        def mouse_watch_task(mw,task):
            if not mw: return task.cont
            if not mw.node().hasMouse(): return task.cont
            self.drag(mw)
            self.preview(mw)
            return task.cont

        def reset(*args):
            self.buttons = dict()
            self.window_task = dict()
            self.reset = self.basic_reset
        self.reset = reset

        self.buttons = {'mouse1':mouse1, 'mouse1-up':mouse1_up, 'mouse3':mouse3,
        'space':space, 'escape':self.reset, 's':self.save, 'u':u,'backspace':backspace,
        'shift-mouse1':shift_mouse1}
        self.window_tasks = {'mouse_watch_task':mouse_watch_task}
        self.setup_window(windict)
