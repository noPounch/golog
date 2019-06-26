import pickle
import os, sys
from hcat import simpSet
from hcat_funcs import *
import golog as Golog
sSet = None


#from a golog, create a simplicial set that can be unpacked into antoher golog via an importer, or pickled into a file
def golog_to_sSet(golog):

    def create_export_data(simplex):

        export_simplex = old_to_new_functor(simplex)
        if export_simplex.data['exported'] == True: return export_simplex #if simplex has already been exported, return it's finished export simplex

        graphics = golog_sSet.simplex_to_graphics[simplex]
        print(export_simplex.label + " is handling {}\'s data:".format(simplex.label),simplex.data)
        data = simplex.data
        export_simplex.data['export_data'] = dict()
        export_simplex.data['export_data']['pos'] = tuple(graphics['node'].getPos())


        print(export_simplex.label + " is handling {}\'s mathData:".format(simplex.label),simplex.mathData)
        mathData = simplex.mathData
        if isinstance(mathData, Golog.golog):
            print(export_simplex.label+"\'s mathData is a golog!")
            export_simplex.mathData = golog_to_sSet(mathData)
        else:
            export_simplex.mathData = mathData
        export_simplex.data['exported'] = True
        return export_simplex

    def rundiags(old_to_new_functor):
        (golog_sSet, export_sSet, old_to_new_lambda) = (old_to_new_functor.dom,old_to_new_functor.codom, old_to_new_functor.F)
        print("done handling "+golog_sSet.label+"\'s data")
        print("---------------------")
        for s in export_sSet.rawSimps: print(s.label+"\'s exported mathData:\n", s.mathData,"\n")
        print("---------------------")


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
        print('attempted to export unhandled sSet')
        return
    if not sSet.export_tag == 'golog':
        print('this exporter function is for gologs')
        return

    with open(location_string,'wb') as file:
        pickle.dump(sSet,file)
    return location_string
    #prompt user for save location

def gexport(golog, location_string):
    return picklesSet(golog_to_sSet(golog), location_string)


def unpicklesSet(location_string):
    with open(location_string,'rb') as file:
        import_sSet = pickle.load(file)
    if not isinstance(import_sSet,simpSet):
        print('imported object not a simplicial set')
    if not hasattr(import_sSet,'export_tag'):
        print('imported object has no export tag')
        return
    if not import_sSet.export_tag == 'golog':
        print('imported simplex does not represent a golog')
        return
    return import_sSet
    #check if upickled thing is actually an sSet representing a golog



def sSet_to_golog(base, import_sSet):

    def setupSimplex(simplex):
        if simplex.data['imported'] == True: return import_simplex_to_golog_simplex[simplex]
        if simplex.level == 0:
            # set up panda3d object
            golog_simplex = golog.createObject(setPos = simplex.data['export_data']['pos'], label = simplex.label)
            #store simplex in a mapping (to prevent double computing)
            import_simplex_to_golog_simplex[simplex] = golog_simplex

            #if imported simplex has mathData and it is tagged handle it
            if hasattr(simplex.mathData,'export_tag'):
                #if simplex.mathData had export_tag golog, then import it as a golog
                if simplex.mathData.export_tag == 'golog': golog_simplex.mathData = sSet_to_golog(base, simplex.mathData)
                #else import mathData normally
                else: golog_simplex.mathData = simplex.mathData
                return import_simplex_to_golog_simplex[simplex]

                if simplex.level == 1:
                    #return the already setup simplecies, or if they aren't yet set up, set them up
                    faces = (setupSimplex(face) for face in simplex.faces)
                    golog_simplex = golog.createMorphism(label = simplex.label)
                    import_simplex_to_golog_simplex[simplex] = golog_simplex


    golog = Golog.golog(base, label = import_sSet.label)
    import_simplex_to_golog_simplex = dict()
    for simplex in import_sSet.rawSimps:simplex.data['imported'] = False
    for simplex in import_sSet.rawSimps: setupSimplex(simplex)
    return golog

def gimport(base, location_string):
    return sSet_to_golog(base, unpicklesSet(location_string))
