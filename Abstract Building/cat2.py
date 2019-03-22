#Category Defs
class object:
    def __init__(self,label = None):
        self.label = label
        self.identity = morphism(self,self,"Id_"+ label)
        self.index = None

class morphism:
    def __init__(self,dom,codom,label = None):
        self.domain = dom
        self.codomain = codom
        self.label = label
        self.pprint = label + ":"+self.domain.label +" -> "+self.codomain.label

class commDiag:
    #f = [f_1,...], g = [g_1,...]. A commDiag formally asserts that f_n o...o f_1 = g_m o ... o g_1
    def __init__(self,fList,gList):
        self.fList = fList;
        self.gList = gList;
        #self.pprint = []

class category:
    def __init__(self):
        self.objects = []
        self.morphisms = []
        self.commDiags = []
        self.Hom = []

    def addObject(self,label = None):
        o = object(label)
        #add object
        self.objects.append(o)
        #get index of object in cat.objects
        o.index = self.objects.index(o)

        #add identity morphism
        self.morphisms.append(o.identity)

        #Add a new Hom(o,-) list
        self.Hom.append([])




        #for all A create Hom(o,A) and Hom(o,A) excluding Hom(o,o)
        for A in self.objects[:-1]:
            self.Hom[o.index].append([]) #Hom(o,A) = Hom[o.index][A.index]
            self.Hom[A.index].append([]) #Hom(A,o) = Hom[A.index][o.index]

        #Create Hom(o,o) with identity already in it
        self.Hom[o.index].append([o.identity])

        #for all A create



        return o

    def addMorphism(self,domain,codomain,label = None):
        if domain in self.objects and codomain in self.objects:
            f = morphism(domain,codomain, label)
            self.morphisms.append(f)

            #add identity commDiags
            self.addCommDiag([f,f.domain.identity],[f])
            self.addCommDiag([f.codomain.identity,f],[f])
            self.Hom[domain.index][codomain.index].append(f)

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

    def hom(self,A,B):
        #1) Check A, B are objects of Cat
        if A not in self.objects or B not in self.object:
            raise Exception("On of the objects is not in category")
            return

        return Hom[A.index][B.index]





        #2) Get index of A, B

        #3) Return HOM[i_A,i_B]

    def compose(self,fList):

        #0) Check if morphisms are in C.Morphisms
        if not set(fList) <= set(self.morphisms):
            raise Exception("One of the morphisms is not in the Category")
            return

        #1) Check if composition has been defined, return if so
        for comm in self.commDiags:
            if fList == comm.fList:
                if len(comm.gList) == 1:
                    return comm.gList[0]
            elif fList == comm.gList:
                if len(comm.flist) == 1:
                    return comm.flist[0]
        #2) If not, formally compose, add to commDiags and return
            else:
                complabel = " o ".join([f.label for f in fList]) #formal label
                compf = self.addMorphism(fList[-1].domain, fList[0].codomain, complabel) #formal composition
                self.addCommDiag(fList,[compf]) #add to commDiags



#completes composition in category.
def completeCat(C):
    if not isinstance(C, Category):
        raise Exception("Input must be a category")
        return
    #1) Generate Chains in C.morphisms
    ###### PROBLEM : NO UPPER LIMIT TO CHAINS ######
    #Bad Solution: Set upper limits
    #Good Solution: Keep compositions in abstraction
    #2) Check if Chain is part of a commDiag with

#Functor
class functor:
    def __init__(domain, codomain):
        pass
    #1) Define function on Objects
    #2) Define function on Morphisms
    #3) check commutativity.

########### TESTING #############
C = category()
o = C.addObject("o")
b = C.addObject("b")
f = C.addMorphism(o,b,"f")
g = C.addMorphism(b,o,"g")
