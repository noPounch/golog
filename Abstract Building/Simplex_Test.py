import tools



#User Defined

#Category Defs
class object:
    def __init__(self,label = ''):
        self.label = label
        self.identity = None
        self.index = None

class morphism:
    def __init__(self,dom,codom,label = ''):
        self.domain = dom
        self.codomain = codom
        self.index = None
        self.label = label
        self.pprint = label + ":"+self.domain.label +" -> "+self.codomain.label

class multigraph:
    def __init__(self):
        self.objects = []
        self.morphisms = []
        self.Hom = []

    def addObject(self,label = ''):
        o = object(label)
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


#####create simplex multigraph for formal composition
simplex = multigraph()
for i in range(3): simplex.addObject() #three vertices

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
        self.objectMap = obf
        self.morphismMap = morf
        self.index = None
        #for f in domain.morphisms:
        #    assert morf(f).domain == obf(f.domain) and morf(f).codomain == obf(f.codomain)



#formally compose by creating a simplex in a precategory C
def simplicialDiag(codom, objects, morphisms):
    obf = lambda i:objects[i] #send vertices to given objects
    morf = lambda i:morphisms[i] #send arrows to given morphisms
    return graphMap(simplex, codom, obf, morf)

#A multigraph with a class of commutative diagrams, built by simplicies
class precategory:
    def __init__(self):
        self.multigraph = multigraph()
        #simplex database by function builder (check Tools) retreive raw list of simplecies by simplecies.list()
        self.simplecies = tools.functionBuilder()
        #

        self.commDiags = tools.functionBuilder()



    def addObject(self, label = ''): return self.multigraph.addObject(label)
    def addMorphism(self,domain, codomain, label = ''): return self.multigraph.addMorphism(domain, codomain, label)

    def addSimplex(self, f ,g ,gof):
        #0.1) Check morphisms are in underlying multigraph
        if not {f,g} <= set(self.multigraph.morphisms):
            raise Exception("morphisms are not in multigraph")
            return

        #0.2) Check if morphisms are composable (domains and codomains line up)
        if not f.codomain == g.domain and f.domain == gof.domain and g.codomain == gof.codomain:
            raise Exception("morphisms not composable")
            return


        #0.3) Check if simplex already exists (if it doesn't it will raise an error)
        try:
            simp = self.simplecies.eval((f,g))
            #Alert us to what composition is already defined to be.
            #raise Exception("composition" f.label)
        #if gof isn't defined, catch error to create formal simplex (f,g,gof)
        except:
            simp = simplicialDiag(self, [f.domain,f.codomain,g.codomain],[f,g,gof])
            simp.index = len(self.simplecies.list())
            self.simplecies.addValue((f,g),simp)
            return simp


#Define a prefunctor as an object map F0:ob(C) -> ob(D), F1: mor(C) -> mor(D), F2:simp(C) to simp(D)
#With conditons (in assertions below)
class prefunctor:
    def __init__(self,domain,codomain,F0,F1,F2):
        self.domain = domain
        self.codomain = codomain
        self.F0 = F0
        self.F1 = F1
        self.F2 = F2
        #self.graphMap = graphMap(domain.multigraph,codomain.multigraph,F0,F1)
        #check functorial condition on simplicies
        for simp in self.domain.simplecies.list():
            for i in range(3):
                assert F0(simp.objectMap(i)) == F2(simp).objectMap(i), "Functorality failed: " + F0(simp.objectMap(i)).label +" != " +F2(simp).objectMap(i).label
                assert F1(simp.morphismMap(i)) == F2(simp).morphismMap(i), "Functorality failed: " + F1(simp.morphismMap(i)).label +" != " +F2(simp).morphismMap(i).label


################ TESTING
C = precategory()
a_C = C.addObject("a_C")
b_C = C.addObject("b_C")
c_C = C.addObject("c_C")
f_C = C.addMorphism(a_C,b_C,"f_C")
g_C = C.addMorphism(b_C,c_C,"g_C")
gof_C = C.addMorphism(a_C,c_C,"gof_C")
simp_C = C.addSimplex(f_C,g_C,gof_C)

D = precategory()
a_D = D.addObject("a_D")
b_D = D.addObject("b_D")
c_D = D.addObject("c_D")
f_D = D.addMorphism(a_D,b_D,"f_D")
g_D = D.addMorphism(b_D,c_D,"g_D")
gof_D = D.addMorphism(a_D,c_D,"gof_D")
simp_D = D.addSimplex(f_D,g_D,gof_D)

F0 = lambda o:D.multigraph.objects[o.index]
F1 = lambda f:D.multigraph.morphisms[f.index]
F2 = lambda simp:D.simplecies.list()[simp.index]
F = prefunctor(C,D,F0,F1,F2)
