#goal of this file is to create:
#1) an export function that returns simplecies
#2) an import function that checks face conditions on simplecies
#--That The faces even exist (raise exception)
#--That they satisfy the face conditions (return in conditions string)
#--That they satisfy degeneracy conditions (return in conditions string)

import os, sys
sys.path.append(os.path.abspath('..'))
from root.hcat import *

def export(sSet):
    return sSet.simplecies
