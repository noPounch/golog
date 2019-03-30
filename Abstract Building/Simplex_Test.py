import tools



#User Defined

#Category Defs
class object:
    def __init__(self,label = ''):
        self.label = label
        self.identity = None
        self.index = None

        #### add category reference to objects
        self.category = None

class morphism:
    def __init__(self,dom,codom,label = ''):
        self.domain = dom
        self.codomain = codom
        self.index = None
        self.label = label
        self.pprint = label + ":"+self.domain.label +" -> "+self.codomain.label

        #### add category reference to morphisms
        self.category = None

class multigraph:
    def __init__(self):
        self.objects = []
        self.morphisms = []
        self.workingPrecategory = None
        self.Hom = []

    def addObject(self,label = ''):
        o = object(label)
        o.multigraph = self
        #add object
        self.objects.append(o)
        #get index of object in cat.objects
        o.index = self.objects.index(o)

        #add identity morphism
        o.identity = self.addMorphism(o,o,"Id_"+ o.label)




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

    def addMorphism(self,domain,codomain,label = ''):
        if domain in self.objects and codomain in self.objects:
            f = morphism(domain,codomain, label)
            f.index = len(self.morphisms)
            self.morphisms.append(f)


            #add identity commDiags
            #self.addCommDiag([f,f.domain.identity],[f])
            #self.addCommDiag([f.codomain.identity,f],[f])
            #self.Hom[domain.index][codomain.index].append(f)

            return f
        elif domain not in self.objects:
            raise Exception("domain not in category")
        elif codomain not in self.objects:
            raise Exception("codomain not in category")

    def hom(self,A,B):
        #1) Check A, B are objects of Cat
        if A not in self.objects or B not in self.object:
            raise Exception("On of the objects is not in category")
            return

        return Hom[A.index][B.index]

    #create free Precategory on multigraph
    def asPrecategory(self):
        return precategory(multigraph = self);

#####create simplex multigraph for formal composition
simplex = multigraph()
for i in range(3): simplex.addObject(str(i)) #three vertices

simplex.addMorphism(simplex.objects[0],simplex.objects[1],"01") #three maps
simplex.addMorphism(simplex.objects[1],simplex.objects[2],"12")
simplex.addMorphism(simplex.objects[0],simplex.objects[2],"02")
#####

####takes multigraph domain and codomain, and lambda function object maps and function maps
#Assertions as below
class graphMap:
    def __init__(self,domain,codomain,obf,morf):
        self.domain = domain #can get objects as list by co/domain.objects or .morphisms
        self.codomain = codomain
        self.obImage = {obf(o) for o in domain.objects}
        self.morImage = {morf(o) for o in domain.morphisms}
        self.label = ""

        #check its actually a map
        assert self.obImage <= set(codomain.objects), "F0 doesnt map into codomain"
        assert self.morImage <= set(codomain.morphisms), "F1 doesnt map into codomain"

        self.objectMap = obf
        self.morphismMap = morf
        self.index = None
        #Check co/dom(morf(f)) = obf(co/dom(f))
        for f in domain.morphisms:
            assert morf(f).domain == obf(f.domain), morf(f).domain.label + " != " + obf(f.domain).label
            assert morf(f).codomain == obf(f.codomain), morf(f).codomain.label + " != "  + obf(f.codomain).label

        #Check if the graphMap is actually a functor between two categories
    def isPreFunctor(self):
                #0) might be able to do the two just by creating a functor (the creation of a functor checks that everything lines up)
                self.asPrefunctor()
                #1) Lift graphMap to a functor
                #2) check if it is functorial (i.e. if it perserves simplecies)


                pass


    #Return graphMap as a Functor between free pre-categories
    def asPrefunctor(self):
        return prefunctor(self.domain.asPrecategory(),self.codomain.asPrecategory(),self.objectMap,self.morphismMap,lambda x:x)





#
# #formally compose by creating a simplex in a precategory C
# def simplicialDiag(codom, objects, morphisms):
#     obf = lambda i:objects[i] #send vertices to given objects
#     morf = lambda i:morphisms[i] #send arrows to given morphisms
#     return graphMap(simplex, codom, obf, morf)

#formally compose by creating a simplex in a precategory C
def simplicialDiag(codom, objects, morphisms):
    morphisms = [o.identity for o in objects] + morphisms #add identities to beginning of simplex list (so that S(Id_i) = Id_ob[i])
    obf = lambda o:objects[o.index] #send vertices to given objects
    morf = lambda o:morphisms[o.index] #sends identity to identities and morphisms to given morphisms
    return graphMap(simplex, codom, obf, morf)

#A multigraph with a class of commutative diagrams, built by simplicies
class precategory:
    def __init__(self, label = ""):
        self.multigraph = multigraph()
        #simplex database by function builder (check Tools) retreive raw list of simplecies by simplecies.listImage()
        self.simplecies = tools.functionBuilder()
        #self.commDiags = tools.functionBuilder()
        self.label = label

    def addObject(self, label = ''): return self.multigraph.addObject(label)
    def addMorphism(self,domain, codomain, label = ''): return self.multigraph.addMorphism(domain, codomain, label)
    def addSimplex(self, f ,g ,gof):
        #Check morphisms are in underlying multigraph
        if not {f,g} <= set(self.multigraph.morphisms):
            raise Exception("morphisms are not in multigraph")
            return

        #Check if morphisms are composable (domains and codomains line up)
        if not f.codomain == g.domain and f.domain == gof.domain and g.codomain == gof.codomain:
            raise Exception("morphisms not composable")
            return


        #Check if simplex already exists: if it does, return it. If it doesn't, create it.
        if (f,g) in self.simplecies.listDomain():
            return self.simplecies.eval((f,g))
        else:
            simp = simplicialDiag(self.multigraph, [f.domain,f.codomain,g.codomain],[f,g,gof])
            simp.index = len(self.simplecies.listImage())
            self.simplecies.addValue((f,g),simp)
            return simp


#Define a prefunctor as an object map F0:ob(C) -> ob(D), F1: mor(C) -> mor(D), F2:simp(C) to simp(D)
#With conditons (in assertions below)
class prefunctor:
    def __init__(self,domain,codomain,F0,F1,F2):
        #Check domain and codomain are even correct functions ob -> ob,...
        self.F0 = F0
        self.F1 = F1
        self.F2 = F2
        self.domain = domain
        self.codomain = codomain

        #check image F0(domain.objects) <= codomain.objects
        assert {self.F0(o) for o in self.domain.multigraph.objects} <= set(self.codomain.multigraph.objects), "F0 doesn't map from domain to codomain"
        assert {self.F1(f) for f in self.domain.multigraph.morphisms} <= set(self.codomain.multigraph.morphisms), "F1 doesn't map from domain to codomain"
        assert {self.F2(simp) for simp in self.domain.simplecies.listImage()} <= set(self.codomain.simplecies.listImage()), "F2 doesn't map from domain to codomain"


        #check if it's a graphMap
        try:
            self.graphMap = graphMap(domain.multigraph,codomain.multigraph,F0,F1)
        except:
            raise Exception("F is not a graphMap")





        #self.graphMap = graphMap(domain.multigraph,codomain.multigraph,F0,F1)
        #check functorial condition on simplicies
        for simp in self.domain.simplecies.listImage():
            for i in range(3):
                #check F0(simp.ob) = F2(simp).ob and F1(simp.mor) = F2(simp).mor
                ####can definitely make this more succinct using mapto
                assert F0(simp.objectMap(simplex.objects[i])) == F2(simp).objectMap(simplex.objects[i]), "Functorality failed: " + F0(simp.objectMap(simplex.objects[i])).label +" != " +F2(simp).objectMap(simplex.objects[i]).label
                assert F1(simp.morphismMap(simplex.morphisms[i])) == F2(simp).morphismMap(simplex.morphisms[i]), "Functorality failed: " + F1(simp.morphismMap(simplex.morphisms[i])).label +" != " +F2(simp).morphismMap(simplex.morphisms[i]).label

#Check if
#subcategory a precategory is a subcategory if the inclusion graphMap is a faithfull prefunctor
def isFaithfull(F):
    if len(F.graphMap.obImage) == len(F.domain.multigraph.objects) and len(F.graphMap.morImage) == len(F.domain.multigraph.morphisms):
        return True
    else:
        return False




################ TESTING
C = precategory(label = "C")
a_C = C.addObject("a_C")
b_C = C.addObject("b_C")
c_C = C.addObject("c_C")
f_C = C.addMorphism(a_C,b_C,"f_C")
g_C = C.addMorphism(b_C,c_C,"g_C")
gof_C = C.addMorphism(a_C,c_C,"gof_C")
simp_C = C.addSimplex(f_C,g_C,gof_C)


D = precategory(label = "D")
a_D = D.addObject("a_D")
b_D = D.addObject("b_D")
c_D = D.addObject("c_D")
f_D = D.addMorphism(a_D,b_D,"f_D")
g_D = D.addMorphism(b_D,c_D,"g_D")
gof_D = D.addMorphism(a_D,c_D,"gof_D")
simp_D = D.addSimplex(f_D,g_D,gof_D)

F0 = lambda o:D.multigraph.objects[o.index]
F1 = lambda f:D.multigraph.morphisms[f.index]
F2 = lambda simp:D.simplecies.listImage()[simp.index]
Id_C = prefunctor(C,C,lambda x:x,lambda x:x,lambda x:x)
print(isFaithfull(Id_C))
F = prefunctor(C,D,F0,F1,F2)
