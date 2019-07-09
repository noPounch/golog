import pickle
import os, sys
from hcat import simpSet, Math_Data
from hcat_funcs import *
import golog as Golog
sSet = None


#from a golog, create a simplicial set that can be unpacked into antoher golog via an importer, or pickled into a file
def golog_to_sSet(golog):

    def create_export_data(simplex):

        export_simplex = old_to_new_functor(simplex)
        if export_simplex.data['exported'] == True: return export_simplex #if simplex has already been exported, return it's finished export simplex

        graphics = golog_sSet.simplex_to_graphics[simplex]
        # print(export_simplex.label + " is handling {}\'s data:".format(simplex.label),simplex.data)
        data = simplex.data
        export_simplex.data['export_data'] = dict()
        export_simplex.data['export_data']['pos'] = tuple(graphics['node'].getPos())


        if simplex.math_data.type == 'golog':
            export_simplex.math_data = Math_Data(math_data = golog_to_sSet(simplex.math_data()),type = 'sSet')
        else: export_simplex.math_data = simplex.math_data
        export_simplex.data['exported'] = True
        return export_simplex

        # print(export_simplex.label + " is handling {}\'s math_data:".format(simplex.label),simplex.math_data)
        # math_data = simplex.math_data
        # if isinstance(math_data, Golog.golog):
        #     # print(export_simplex.label+"\'s math_data is a golog!")
        #     export_simplex.math_data = golog_to_sSet(math_data)
        # else:
        #     export_simplex.math_data = math_data
        # export_simplex.data['exported'] = True
        # return export_simplex

    def rundiags(old_to_new_functor):
        (golog_sSet, export_sSet, old_to_new_lambda) = (old_to_new_functor.dom,old_to_new_functor.codom, old_to_new_functor.F)
        # # print("done handling "+golog_sSet.label+"\'s data")
        # # print("---------------------")
        # for s in export_sSet.rawSimps: print(s.label+"\'s exported math_data:\n", s.math_data,"\n")
        # print("---------------------")


    old_to_new_functor = stripsSet(golog.sSet) #this is a functor, the domain, codomain and lambda function are as below:
    (golog_sSet, export_sSet, old_to_new_lambda) = (old_to_new_functor.dom,old_to_new_functor.codom, old_to_new_functor.F)
    export_sSet.export_tag = 'golog' #tell importer that the data in the simplicial set should be read as golog data
    for simplex in export_sSet.rawSimps: simplex.data['exported'] = False #set a tag to keep track of which simplecies have already been exported
    for simplex in golog_sSet.rawSimps: create_export_data(simplex)
    rundiags(old_to_new_functor)
    return export_sSet

def picklesSet(sSet, location_string):
    #first check if sSet is an exported golog
    if not hasattr(sSet,'export_tag'):
        # print('attempted to export unhandled sSet')
        return
    if not sSet.export_tag == 'golog':
        # print('this exporter function is for gologs')
        return

    with open(location_string,'wb') as file:
        pickle.dump(sSet,file)
    return location_string
    #prompt user for save location

def gexport(golog, location_string):
    print('saved to {}'.format(location_string))
    return picklesSet(golog_to_sSet(golog), location_string)


def unpicklesSet(location_string):

    print('loading from to {}'.format(location_string))
    with open(location_string,'rb') as file:
        import_sSet = pickle.load(file)
    if not isinstance(import_sSet,simpSet):
        return
    if not hasattr(import_sSet,'export_tag'):
        return
    if not import_sSet.export_tag == 'golog':
        return
    return import_sSet
    #check if upickled thing is actually an sSet representing a golog



def sSet_to_golog(base, import_sSet):
    if not (hasattr(import_sSet,'export_tag') and import_sSet.export_tag== 'golog'): return #full sSet should have a golog export_tag
    def setupSimplex(simplex):
        if simplex.data['imported'] == True: return import_simplex_to_golog_simplex[simplex]
        if simplex.level == 0:
            # set up panda3d object
            golog_simplex = golog.add(0, pos = simplex.data['export_data']['pos'], label = simplex.label)
            #store simplex in a mapping (to prevent double computing)
            import_simplex_to_golog_simplex[simplex] = golog_simplex

            #if imported simplex is a sSet with a golog export_tag handle it with a gimport as well
            if hasattr(simplex.math_data(),'export_tag'):
                #if simplex.math_data had export_tag golog, then import it as a golog
                if simplex.math_data().export_tag == 'golog':
                    golog_simplex.math_data = Math_Data(math_data = sSet_to_golog(base, simplex.math_data()),type = 'golog')
            #else import math_data normally
            else: golog_simplex.math_data = simplex.math_data
            simplex.data['imported'] = True
            return import_simplex_to_golog_simplex[simplex]

        if simplex.level == 1:
            #return the already setup simplecies, or if they aren't yet set up, set them up
            faces = tuple(setupSimplex(face) for face in simplex.faces)
            golog_simplex = golog.add(faces, label = simplex.label)
            import_simplex_to_golog_simplex[simplex] = golog_simplex
            simplex.data['imported'] = True
            return import_simplex_to_golog_simplex[simplex]


    golog = Golog.golog(base, label = import_sSet.label)

    import_simplex_to_golog_simplex = dict()
    for simplex in import_sSet.rawSimps:simplex.data['imported'] = False
    for simplex in import_sSet.rawSimps: setupSimplex(simplex)
    return golog

def gimport(base, location_string):
    return sSet_to_golog(base, unpicklesSet(location_string))
