import sys, os, json
import tkinter as tk
from golog_export import *
from direct.showbase.ShowBase import ShowBase
from golog import golog as Golog
from window_manager import *
from mode_head import *
from tk_funcs import save_load_new, unique_path


version = '1.0.0'



def bootstrap_config():
    path_dict = {
    'root' : os.path.abspath('.'),
    'user_path' : os.path.abspath('./user_files'),
    'configs_path' : os.path.abspath('./user_files/configs'),
    'save_path' : os.path.abspath('./user_files/save')
    }
    for path_name in path_dict.keys():
        if not os.path.exists(path_dict[path_name]): os.mkdir(path_dict[path_name])

    path_dict = {**path_dict,'config_file':os.path.join(path_dict['configs_path'],'config.json')}

    if not os.path.exists(path_dict['config_file']):
        with open(os.path.join(path_dict['configs_path'],'config.json'),'w') as file:
            config_dict = {'path_dict':path_dict}
            json.dump(config_dict,file)

    with open(os.path.join(path_dict['configs_path'],'config.json'),'r') as file:
        config_dict = json.load(file)
    return config_dict





def new_golog(base, folder_path,golog_file):
    print('new golog saved in: ', folder_path)
    golog = Golog(base, label = golog_file.split('.golog')[0])
    golog_folder = os.path.join(folder_path, *unique_path(folder_path,[golog.label]))
    if not os.path.exists(golog_folder): os.mkdir(golog_folder)
    save_location = os.path.join(golog_folder,golog.label+'.golog')


    gexport(golog, save_location)
    controllable_golog = mode_head(base,golog, folder_path = golog_folder)
    modeHeadToWindow(base, controllable_golog)
    return controllable_golog, save_location

def load_golog(base, folder_path, save_location):
    print('golog loaded from: ', folder_path)
    golog = gimport(base,save_location)
    controllable_golog = mode_head(base,golog, folder_path = folder_path)
    modeHeadToWindow(base, controllable_golog)
    return controllable_golog


class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType = 'none')
        self.disable_mouse()
        self.obdict = {'gologs':[], 'mode_heads':[], 'window_managers':[]}

        #get or create config dictionary
        config_dict = bootstrap_config()
        #check for a recent ontology
        if 'recent_path' in config_dict['path_dict'].keys():
            recent_path = config_dict['path_dict']['recent_path']
            if not os.path.exists(config_dict['path_dict']['recent_path']):
                del config_dict['path_dict']['recent_path']
                print('del')
                recent_path = None
        else: recent_path = None





        # need to migrate into gologToWindow
        base.accept("f5", sys.exit)
        base.accept("f6", sys.exit)

        (newv, save_location) = save_load_new(config_dict['path_dict']['save_path'], recent_path)
        (folder_path, golog_file) = os.path.split(save_location)


        if newv: self.cg, save_location = new_golog(self,folder_path, golog_file)

        elif not newv: self.cg = load_golog(self, folder_path,save_location)

        # ########
        # sSet = self.cg.golog.sSet
        # print([self.cg.golog.Simplex_to_Graphics[simp].NP for simp in sSet.rawSimps])
        # for simp in sSet.rawSimps:
        #     self.cg.multi_select(self.cg.golog.Simplex_to_Graphics[simp].NP)
        # ##########

        #update config_dict with new recent golog
        config_dict['path_dict']['recent_path'] = save_location
        with open(config_dict['path_dict']['config_file'],'w') as file:
            json.dump(config_dict, file)

    def run(self):
        try:
            super(runner, self).run()
        except:
            self.error_reset()

    def error_reset(self):
        print(sys.exc_info()[0])
        self.run()



r = runner()
r.run()
