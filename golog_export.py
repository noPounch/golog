import pickle
import os, sys
from hcat import simpSet
import golog as Golog
sSet = None
def gexport(golog):

    math_sSet = simpSet(label = golog.label+ "underlying hcat")
    math_sSet.add(golog.sSet) #add all golog.sSet data but cut off the simplex_to_graphics dict
    math_sSet.export_data = dict()
    for simplex in math_sSet.rawSimps:
        handle_data(simplex)
        math_sSet.export_data[simplex] = dict()
        math_sSet.export_data[simplex]['pos'] = golog.sSet.simplex_to_graphics[simplex]['node'].getPos()
    rundiags(golog, math_sSet)
    return math_sSet


def gimport(golog_sSet,math_sSet, base = None):
    #import pure math data and follow instructions to create a scenegraph
    if base == None:
        return sSet


def handle_data(simplex):
    print("handling "+simplex.label+"\'s data:")
    data = simplex.mathData
    if not data:
        print("no data \n")
        return
    elif isinstance(data, Golog.golog):
        print(simplex.label+"\'s data is a golog named " +data.label +"\n")
        simplex.mathData = gexport(data) #transform golog data into a math_sSet as well

    else: print("pickling" + str(type(data))+"\n")


################# DIAGNOSTICS FOR EXPORT MODULE ###################
def rundiags(golog,math_sSet):
    print("done handling "+golog.label+"\'s data")
    print("---------------------")
    for s in math_sSet.rawSimps: print(s.label+"\'s export data:\n", math_sSet.export_data[s],"\n")
    print("---------------------")
