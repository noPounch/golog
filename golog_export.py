import pickle
import os, sys
from hcat import simpSet
sSet = None
def gexport(golog):
    sSet = simpSet(label = golog.label+"_save")
    render = golog.render

    def transform_to_python_and_get_children(node):
        # if node in golog.NPtoSimplex.keys():
        #     data = golog.NPtoSimplex()
        sSet.add(0,label = str(type(node))) #add a 0-simplex with label the node-type
        if node.getNumChildren() > 0:
            for child in node.getChildren():
                transform_to_python_and_get_children(child)

    transform_to_python_and_get_children(render)
    rundiags(sSet)

def gimport(sSet, base = None):
    if base == None:
        sSet = sSet
        return



################# DIAGNOSTICS FOR EXPORT MODULE ###################
def rundiags(sSet):
    print([s.label for s in sSet.rawSimps])
