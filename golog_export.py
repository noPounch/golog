import pickle
import os, sys
from hcat import simpSet
from hcat_funcs import *
import golog as Golog
sSet = None
def gexport(golog):
    #create a copy of underlying simplicial set without data
    old_to_new_functor = stripsSet(golog.sSet) #this is a functor, the domain, codomain and lambda function are as below:
    (golog_sSet, export_sSet, old_to_new_lambda) = (old_to_new_functor.dom,old_to_new_functor.codom, old_to_new_functor.F)
    for simplex in export_sSet.rawSimps: simplex.data['exported'] = False #set a tag to keep track of which simplecies have already been exported
    for simplex in golog_sSet.rawSimps: create_export_data(simplex, golog_sSet.simplex_to_graphics[simplex], old_to_new_functor(simplex))

        # export_sSet.export_data[simplex]['pos'] = golog.sSet.simplex_to_graphics[simplex]['node'].getPos()
    rundiags(old_to_new_functor)
    return export_sSet


def gimport(golog_sSet,math_sSet, base = None):
    #import pure math data and follow instructions to create a scenegraph
    if base == None:
        return sSet


def create_export_data(data_simplex, graphics, export_simplex):
    if export_simplex.data['exported'] = True: return export_simplex #if simplex has already been exported, return it's finished export simplex
    print(export_simplex.label + " is handling {}\'s data:".format(data_simplex.label),data_simplex.data)
    print(export_simplex.label + " is handling {}\'s mathData:".format(data_simplex.label),data_simplex.mathData)
    mathData = simplex.mathData
    data = simplex.data
    # graphics = golog_sSet.simplex_to_graphics[simplex]
    model = graphics['model']
    pos = tuple(graphics['node'].getPos())
    #1) create a dictionary for the graphics, place in data['graphics']
    #2) create export for it's simplex.mathData and return it to export_simplex.mathData

    # if not data:
    #     print("no data in {} \n".format(simplex.label))
    #     return
    # elif isinstance(data, Golog.golog):
    #     print(simplex.label+"\'s data is a golog named " +data.label +"\n")
    #     simplex.mathData = gexport(data) #transform golog data into a math_sSet as well
    #
    # else: print("pickling" + str(type(data))+"\n")


################# DIAGNOSTICS FOR EXPORT MODULE ###################
def rundiags(old_to_new_functor):
    (golog_sSet, export_sSet, old_to_new_lambda) = (old_to_new_functor.dom,old_to_new_functor.codom, old_to_new_functor.F)
    print("done handling "+golog_sSet.label+"\'s data")
    print("---------------------")
    for s in export_sSet.rawSimps: print(s.label+"\'s export data:\n", s.data,"\n")
    print("---------------------")
