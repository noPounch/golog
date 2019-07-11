import pickle
import os, sys
from hcat import simpSet, Math_Data
from hcat_funcs import *
import golog as Golog
sSet = None

# meta data for exporting math and graphics data
# math_data is transformed into seralizable format in __init__ and can be transformed back in transform
# graphics initialization data can be stored in graphics_kwargs (to create a Graphics_data in golog)
class export_data():
    def __init__(self,golog, old_simplex):
        #if math_data is a golog, transform it to an sSet for exporting
        if old_simplex.math_data.type == 'golog':
            self.exported_math_data = Math_Data(type = 'exported golog', math_data = golog_to_sSet(old_simplex.math_data()))
        else: self.exported_math_data = old_simplex.math_data

        self.graphics_kwargs = golog.Simplex_to_Graphics[old_simplex].graphics_kwargs

    #on import, if export_data's math_data is an exported golog, transform it to a golog(base) and return it
    #otherwise, return the original math_data
    def transform(self,base):
        if self.exported_math_data.type == 'exported golog':
            return Math_Data(type = 'golog', math_data = sSet_to_golog(base,self.exported_math_data()))
        else: return self.exported_math_data


def golog_to_sSet(golog):
    old_to_new = stripsSet(golog.sSet)
    for simp in old_to_new.dom.rawSimps:
        exported_data = export_data(golog,simp)
        old_to_new(simp).math_data = Math_Data(type = 'export_data',math_data = exported_data)
    return old_to_new.codom
#strip golog's graphics and math_data
#export math data and graphics_kwargs
def gexport(golog,location_string):
    export_sSet = golog_to_sSet(golog)

    with open(location_string,'wb') as file:
        pickle.dump(export_sSet,file)
    return location_string

def sSet_to_golog(base, sSet):
    golog = Golog.golog(base, label = sSet.label)
    old_to_new = dict()

    def setupSimplex(simplex):
        #check if simplex has been processed, return it's transformed simplex
        if simplex in old_to_new.keys(): return old_to_new[simplex]
        #check if faces are in golog
        newfaces = tuple([setupSimplex(face) for face in simplex.faces])
        ## need to make sure I can add 0-simpleces by passing ob = ()
        newsimp = golog.add(newfaces, label = simplex.label, math_data = simplex.math_data().transform(base),**simplex.math_data().graphics_kwargs)
        #props:           #^faces     #^label               #^tranformed math data from export               #^graphics setup from export
        return newsimp

    for simplex in sSet.rawSimps:
        setupSimplex(simplex)
    return golog



def gimport(base, location_string):
    with open(location_string,'rb') as file:
        sSet = pickle.load(file)
    return sSet_to_golog(base,sSet)
