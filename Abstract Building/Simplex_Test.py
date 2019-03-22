import tools



#User Defined

#Category Defs
class object:
    def __init__(self,label = ''):
        self.label = label
        self.identity = morphism(self,self,"Id_"+ label)
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

    def addMorphism(self,domain,codomain,label = ''):
        if domain in self.objects and codomain in self.objects:
            f = morphism(domain,codomain, label)
            self.morphisms.append(f)
            f.index = len(self.morphisms)

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





        #2) Get index of A, B

        #3) Return HOM[i_A,i_B]

#####create simplex multigraph for formal composition
simplex = multigraph()
for i in range(3): simplex.addObject() #three vertices

simplex.addMorphism(simplex.objects[0],simplex.objects[1],"01") #three maps
simplex.addMorphism(simplex.objects[1],simplex.objects[2],"12")
simplex.addMorphism(simplex.objects[0],simplex.objects[2],"02")
#####

####takes multigraph domain and codomain, and lambda function object maps and function maps
class graphMap:
    def __init__(self,domain,codomain,obf,morf):
        self.domain = domain
        self.codomain = codomain
        self.objectMap = obf
        self.morphismMap = morf

#formally compose by creating a simplex in a precategory C
def simplicialDiag(codom, objects, morphisms):
    obf = lambda i :objects[i] #send vertices to given objects
    morf = lambda i:morphisms[i] #send arrows to given morphisms
    return graphMap(simplex, codom, obf, morf)

#A multigraph with a class of commutative diagrams, built by simplicies
class precategory:
    def __init__(self):
        self.multigraph = multigraph()

        #simplex database by function builder (check Tools)
        self.simplecies = tools.functionBuilder()

        #self.commDiags = []



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
            s = self.simplecies.eval((f,g))
        #exception is if (f,g,gof) is not yet a simplex in C
        except:
            simp = simplicialDiag(self, [f.domain,f.codomain,g.codomain],[f,g,gof])
            self.simplecies.addValue((f,g),simp)
        #if it does exist, return s
        else:
            return s

################ TESTING
C = precategory()
a = C.addObject("a")
b = C.addObject("b")
c = C.addObject("c")
f = C.addMorphism(a,b,"f")
g = C.addMorphism(b,c,"g")
gof = C.addMorphism(a,c,"gof")
simp = C.addSimplex(f,g,gof)
