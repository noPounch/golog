import pickle
import os, sys
from hcat import simpSet, Math_Data, Simplex, stripsSet
# from hcat_funcs import *
import golog as Golog
sSet = None

#? move this to only be in run.py
export_version = '1.0.0'

# meta data for exporting math and graphics data
# math_data is transformed into seralizable format in __init__ and can be transformed back in transform
# graphics initialization data can be stored in graphics_kwargs (to create a Graphics_data in golog)
class export_data():
    def __init__(self, old_simplex, **kwargs):
        #if math_data is a golog, transform it to an sSet for exporting
        if old_simplex.math_data.type == 'golog':
            export_golog = golog_to_sSet(old_simplex.math_data()['golog'])
            golog_dict = {'golog':export_golog, 'folder_path' : old_simplex.math_data()['folder_path']}
            self.exported_math_data = Math_Data(type = 'exported golog', math_data = golog_dict)
        else: self.exported_math_data = old_simplex.math_data

        #
        for key in kwargs.keys():setattr(self,key,kwargs[key])

    #on import, if export_data's math_data is an exported golog, transform it to a golog(base) and return it
    #otherwise, return the original math_data
    def transform(self, base,**kwargs):
        if self.exported_math_data.type == 'exported golog':
            golog_dict ={'golog':sSet_to_golog(base,self.exported_math_data()['golog']),'folder_path':self.exported_math_data()['folder_path']}
            return Math_Data(type = 'golog', math_data = golog_dict)
        else: return self.exported_math_data

    def __getattr__(self,attr):
        ### some salty pickle problems dude, who knows
        if attr.startswith('__'):
            raise AttributeError
        ###
        #if simplex has no graphics kwargs, return a list
        if attr == 'graphics_kwargs': return []
        else: return None

#function which encodes the graphics data from a golog entirely into it's underlying simplicial set
# creates an export data that houses graphics information and math_data, and recursively packages math_data if math_data is a golog
def golog_to_sSet(golog):
    old_to_new = stripsSet(golog.sSet)
    for simp in old_to_new.dom.rawSimps:
        # exported_data = export_data(golog, simp, graphics_kwargs = golog.Simplex_to_Graphics[simp].graphics_kwargs) #create some pickleable export_data
        exported_data = export_data( simp, graphics_kwargs = golog.Simplex_to_Graphics[simp].graphics_kwargs) #create some pickleable export_data
        old_to_new(simp).math_data = Math_Data(type = 'export_data',math_data = exported_data) #set math_data of new simplex to export_data
    return old_to_new.codom


#strip golog's graphics and math_data
#export math data and graphics_kwargs
#pickle to file_location
def gexport(golog,location_string):
    ''' takes a golog and a absolute path, and exports it to that path '''
    #check if location exists
    golog_folder = os.path.join(location_string, golog.label)
    if os.path.exists(golog_folder): print('MAY OVERRIDE GOLOG OF SAME NAME')
    export_sSet = golog_to_sSet(golog) # create pickle-able sSet
    export_simplex = Simplex(0,math_data = Math_Data(type = 'exported golog', math_data = export_sSet)) #create a simplex from the export_sSet
    export_meta = export_data(export_simplex, export_version = export_version) # create meta_data in the form of export_data

    #pickle it to location
    with open(location_string,'wb') as file:
        pickle.dump(export_meta,file)
    return location_string

#transform a packed up golog from it's export_sSet back into it's original golog, which is attached to a given showbase
def sSet_to_golog(base, sSet,**kwargs):
    golog = Golog.golog(base, label = sSet.label,**kwargs)
    old_to_new = dict()

    def setupSimplex(simplex):
        #check if simplex has been processed, return it's transformed simplex
        if simplex in old_to_new.keys(): return old_to_new[simplex]
        #check if faces are in golog
        newfaces = tuple([setupSimplex(face) for face in simplex.faces])
        ## need to make sure I can add 0-simpleces by passing ob = ()
        newsimp = golog.add(newfaces, label = simplex.label, math_data = simplex.math_data().transform(base),**simplex.math_data().graphics_kwargs)
        #props:           #^faces     #^label               #^tranformed math data from export               #^graphics setup from export
        old_to_new[simplex] = newsimp
        return newsimp

    for simplex in sSet.rawSimps:
        setupSimplex(simplex)
    return golog


#import an export_sSet and transform it to a golog, updating it if necessary.
def gimport(base, path,**kwargs):
    with open(path,'rb') as file:
        export_meta = pickle.load(file)
    # if export_meta.export_version < export_version:
    #     gupdate(export_meta)
    sSet = export_meta.exported_math_data()
    return sSet_to_golog(base,sSet,**kwargs)



if __name__ == '__main__':
    from direct.showbase.ShowBase import ShowBase
    base = ShowBase(windowType = 'none')
    G = gimport(base, os.path.abspath('./user_files/save/daily_ontologies/Dec_05_2019/daily_golog/daily_golog.golog'),model_path = './misc_data/models/')
