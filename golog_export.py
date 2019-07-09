import pickle
import os, sys
from hcat import simpSet, Math_Data
from hcat_funcs import *
import golog as Golog
sSet = None


class export_data():
    def __init__(self,golog, old_simplex):
        #if math_data is a golog, gexport it
        if old_simplex.math_data.type == 'golog':
            self.exported_math_data = Math_Data(type = 'exported golog', math_data = golog_to_sSet(old_simplex.math_data()))
        else: self.exported_math_data = old_simplex.math_data

        self.graphics_kwargs = golog.Simplex_to_Graphics[old_simplex].graphics_kwargs

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

    def setupSimplex(simplex):
        #check if faces are in golog
        for face in simplex.faces:
            if face not in golog.sSet.rawSimps:
                setupSimplex(face)
        simp = golog.add(simplex, label = simplex.label, math_data = simplex.math_data().transform(base),**simplex.math_data().graphics_kwargs)
    for simplex in sSet.rawSimps:
        setupSimplex(simplex)
    return golog

def gimport(base, location_string):
    with open(location_string,'rb') as file:
        sSet = pickle.load(file)
    return sSet_to_golog(base,sSet)



#
# if __name__ == "__main__":
#     from direct.showbase.ShowBase import ShowBase
#     class runner(ShowBase):
#         def __init__(self):
#             ShowBase.__init__(self)
#             self.disable_mouse()
#
#
#             # need to migrate into gologToWindow
#             base.accept("f5",sys.exit)
#             base.accept("f6",sys.exit)
#             G = Golog.golog(self)
#             a = G.add(0,label = 'a',pos = (0,0,5))
#             b = G.add(0,label = 'b')
#             f = G.add((b,a),label = 'f')
#
#             gexport(G,'save/testnew.golog')
#             G = gimport(self, 'save/testnew.golog')
#             controllable_golog = mode_head(self,G,save_location = 'save/testnew.golog')
#             modeHeadToWindow(self, controllable_golog)
#
#     runner().run()
