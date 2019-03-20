import catFuncs
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

#Category Defs
class object:
    def __init__(self,label = None):
        object.label = label
        object.identity = morphism(self,self,"Id_"+ label)

class morphism:
    def __init__(self,dom,codom,label = None):
        self.domain = dom
        self.codomain = codom
        self.label = label

class commDiag:
    #f = [f_1,...], g = [g_1,...]. A commDiag formally asserts that f_n o...o f_1 = g_m o ... o g_1
    def __init__(self,fList,gList):
        self.fList = fList;
        self.gList = gList;

class category:
    def __init__(self):
        self.objects = []
        self.morphisms = []
        self.commDiags = []

    def addObject(self,label = None):
        o = object(label)
        #add object
        self.objects.append(o)
        #add identity morphism
        self.morphisms.append(o.identity)
        return o

    def addMorphism(self,domain,codomain,label = None):
        if domain in self.objects and codomain in self.objects:
            f = morphism(domain,codomain, label)
            self.morphisms.append(f)

            #add identity commDiags
            self.addCommDiag([f,f.domain.identity],[f])
            self.addCommDiag([f.codomain.identity,f],[f])

            return f
        elif domain not in self.objects:
            raise Exception("domain not in category")
        elif codomain not in self.objects:
            raise Exception("codomain not in category")

    def addCommDiag(self,fList,gList):
        #Inputs fList,gList must be lists of morphisms
        #fList = [f_1,...,f_n] but compostion is f_n o ... o f_1
        #1) check if morphisms are in category
        for f in fList:
            if f not in self.morphisms:
                raise Exception("Morphism" + f.label + "not in category")
                return
        for g in gList:
            if g not in self.morphisms:
                raise Exception("Morphism" + g.label + "not in category")
                return
        #2) check if intermediate co/domains are equal
        fdoms = [f.codomain for f in fList[1:]]
        fcodoms = [f.domain for f in fList[:-1]]
        if fdoms != fcodoms:
            raise Exception("f Morphisms do not compose")
            return

        gdoms = [g.codomain for g in gList[1:]]
        gcodoms = [g.domain for g in gList[:-1]]
        if gdoms != gcodoms:
            raise Exception("g Morphisms do not compose")
            return

        #3) check if co/terminal co/domains are equal
        if fList[0].codomain != gList[0].codomain:
            raise Exception("terminal codomains are unequal")
            return

        if fList[-1].domain != gList[-1].domain:
            raise Exception("initial domains are unequal")
            return

        #4) Set commDiag
        self.commDiags.append(commDiag(fList,gList))


#Functor
class functor:
    def __init__(domain, codomain)
    #1) Define function on Objects
    #2) Define function on Morphisms
    #3) check commutativity.

########### TESTING #############
C = category()
o = C.addObject("yo")
f = C.addMorphism(o,o,"f")
for c in C.commDiags:
    print([f.label for f in c.fList])
    print([g.label for g in c.gList])
