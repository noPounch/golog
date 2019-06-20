import pickle
import os, sys
from hcat import simpSet

def gexport(golog):
    sSet = simpSet(label = golog.label+"_save")
    render = golog.render

    rundiags(sSet)

def gimport(gologProjection,base):
    pass



################# DIAGNOSTICS FOR EXPORT MODULE ###################
def rundiags(sSet):
    print(sSet.label)
