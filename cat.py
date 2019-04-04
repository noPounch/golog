import tools
from copy import deepcopy as copy

#Coding Precidents:
#lambda functions are all defined on actual instances, not their references
#Keywords for defining new objects from old stored in a defaults dictionary

#User Defined

#Category Defs
class object:
    def __init__(self,**kwargs):
        defaults = {'label':'\'\'','data':'None','identity':'None','index':'None','multigraph':'None'}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

class morphism:
    def __init__(self,dom,codom,**kwargs):
        self.domain = dom
        self.codomain = codom
        defaults = {'label':'\'\'','data':'None','index':'None','multigraph':'None'}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

        self.pprint = self.label + ":"+self.domain.label +" -> "+self.codomain.label

class multigraph:
    def __init__(self,**kwargs):
        ###change Hom to a dictionary (calling hom(A,B) is easier this way)
        defaults = {'label':'\'\'','objects':'[]','morphisms':'[]','Hom': '[]','precategory':'None'}
        #set self.key = given or default value
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

    def addObject(self,**kwargs):
        #create new object or copy obj
        o = object(multigraph = self,index = len(self.objects),**kwargs)


        #add object to objects list
        self.objects.append(o)

        #Add a new Hom(o,-) list
        self.Hom.append([])


        #Hom stuff

        #for all A create Hom(o,A) and Hom(o,A) excluding Hom(o,o)
        for A in self.objects[:-1]:
            self.Hom[o.index].append([]) #Hom(o,A) = Hom[o.index][A.index]
            self.Hom[A.index].append([]) #Hom(A,o) = Hom[A.index][o.index]

        #Create Hom(o,o) with identity already in it
        #self.Hom[o.index].append([o.identity])



        return o

    def addMorphism(self,domain,codomain,**kwargs):
        if domain in self.objects and codomain in self.objects:
            f = morphism(domain,codomain, **kwargs)
            f.index = len(self.morphisms)
            self.morphisms.append(f)

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
simplex = multigraph(label = "simplex")
for i in range(3): simplex.addObject(label = str(i)) #three vertices

simplex.addMorphism(simplex.objects[0],simplex.objects[1],label = "01") #three maps
simplex.addMorphism(simplex.objects[1],simplex.objects[2],label = "12")
simplex.addMorphism(simplex.objects[0],simplex.objects[2],label = "02")
#####

####takes multigraph domain and codomain, and function object maps and function maps
#Assertions as below
class graphMap:
    def __init__(self,domain,codomain,F0,F1,**kwargs):
        defaults = {'index':'None','label': '\'\'','prefunctor':'None'}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))


        self.domain = domain #can get objects as list by co/domain.objects or .morphisms
        self.codomain = codomain
        self.F0 = F0
        self.F1 = F1
        self.obImage = {self.F0(o) for o in domain.objects}
        self.morImage = {self.F1(f) for f in domain.morphisms}

        #check its actually a map
        assert self.obImage <= set(codomain.objects), "F0 doesnt map into codomain"
        assert self.morImage <= set(codomain.morphisms), "F1 doesnt map into codomain"



        #Check co/dom(morf(f)) = obf(co/dom(f))
        for f in domain.morphisms:
            assert self.F1(f).domain == self.F0(f.domain), self.F1(f).domain.label + " != " + self.F0(f.domain).label
            assert self.F1(f).codomain == self.F0(f.codomain), self.F1(f).codomain.label + " != "  + self.F0(f.codomain).label

        #Check if the graphMap is actually a functor between two categories
    def isPrefunctor(self):
                #get simplecies from domain
                domSimps = self.domain.precategory.simplecies.listImage()
                #check composition rules
                for simp in domSimps:
                    f = simp.F1(simplex.morphisms[3])

                    g = simp.F1(simplex.morphisms[4])
                    Fgof = self.F1(self.domain.precategory.compose(g,f))
                    FgoFf = self.codomain.precategory.compose(self.F1(g),self.F1(f))
                    if Fgof != FgoFf: return False
                return True

    def asPrefunctor(self):
        if self.domain.precategory == None or self.domain.precategory == None: return False
        if not self.isPrefunctor: return False
        if not self.prefunctor == None: return self.prefunctor

        Ff = 'self.F1(simp.F1(simplex.morphisms[0]))'
        Fg = 'self.F1(simp.F1(simplex.morphisms[1]))'
        F2 = lambda simp:self.codomain.precategory.simplecies.eval((eval(Ff),eval(Fg)))
        F = prefunctor(self.domain.precategory,self.codomain.precategory,self.F0,self.F1,F2, graphMap = self)
        self.prefunctor = F
        return F
    #def asPrefunctor(self):
        #return a prefunctorial version of itself if is functorial w.r.t. the over-precategories


#formally compose by creating a simplex in a precategory C
def simplicialDiag(codom, objects, morphisms):
    #########morphisms = morphisms #add identities to beginning of simplex list (so that S(Id_i) = Id_ob[i])
    obf = lambda o:objects[o.index] #send vertices to given objects
    morf = lambda o:morphisms[o.index] #sends identity to identities and morphisms to given morphisms
    return graphMap(simplex, codom, obf, morf)

#A multigraph with a class of commutative diagrams, built by simplicies
class precategory:
    def __init__(self, **kwargs):
        defaults = {'label':'\'\'','multigraph':'multigraph()','simplecies' :'tools.functionBuilder()'}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

        self.multigraph.label = "U("+self.label+")"
        self.multigraph.precategory = self

    def addObject(self, **kwargs):
        #add identity simplex
        o = self.multigraph.addObject(**kwargs)
        #add identity morphism(without adding identity simplex)
        o.identity = self.multigraph.addMorphism(o,o,label = "Id_"+ o.label)
        simp = self.addSimplex(o.identity,o.identity,o.identity)
        setattr(simp, 'isIdentity', True)
        return o


    def addMorphism(self,domain, codomain, **kwargs):
        f = self.multigraph.addMorphism(domain, codomain, **kwargs)
        setattr(f, 'isIdentity', False)
        lsimp = self.addSimplex(f.domain.identity,f,f)
        rsimp = self.addSimplex(f,f.codomain.identity,f)
        setattr(rsimp, 'isIdentity', True)
        setattr(lsimp, 'isIdentity', True)

        return f
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
            setattr(simp, 'isIdentity', False)
            return simp

    #compose based on simplecies
    def compose(self,g,f):
        if (f,g) in self.simplecies.listDomain():
            return self.simplecies.eval((f,g)).F1(simplex.morphisms[5])
        else: raise Exception("no simplex to define composition")



#Define a prefunctor as an object map F0:ob(C) -> ob(D), F1: mor(C) -> mor(D), F2:simp(C) -> simp(D)
#With conditons (in assertions below)
class prefunctor:
    def __init__(self,domain,codomain,F0,F1,F2,**kwargs):

        defaults = {'label': '\'\'','graphMap' : 'graphMap(domain.multigraph,codomain.multigraph,F0,F1, label = "U("+self.label+")", prefunctor = self )'}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

        ####PROBLEM: label and prefunctor not passing to graphMap class creator
        #Check domain and codomain are even correct functions ob -> ob,...
        # #self.graphMap = graphMap(domain.multigraph,codomain.multigraph,F0,F1)
        # self.graphMap.label = "U("+self.label+")"
        # self.graphMap.prefunctor = self
        self.F0 = F0
        self.F1 = F1
        self.F2 = F2
        self.domain = domain
        self.codomain = codomain

        #check image F0(domain.objects) <= codomain.objects
        assert {self.F0(o) for o in self.domain.multigraph.objects} <= set(self.codomain.multigraph.objects), "F0 doesn't map from domain to codomain"
        assert {self.F1(f) for f in self.domain.multigraph.morphisms} <= set(self.codomain.multigraph.morphisms), "F1 doesn't map from domain to codomain"
        assert {self.F2(simp) for simp in self.domain.simplecies.listImage()} <= set(self.codomain.simplecies.listImage()), "F2 doesn't map from domain to codomain"

        #self.graphMap = graphMap(domain.multigraph,codomain.multigraph,F0,F1)
        #check functorality condition on simplicies
        for simp in self.domain.simplecies.listImage():
            for i in range(3):
                #check F0(simp.ob) = F2(simp).ob and F1(simp.mor) = F2(simp).mor
                ####can definitely make this more succinct using mapto
                assert F0(simp.F0(simplex.objects[i])) == F2(simp).F0(simplex.objects[i]), "Functorality failed: " + F0(simp.F0(simplex.objects[i])).label +" != " +F2(simp).F0(simplex.objects[i]).label
                assert F1(simp.F1(simplex.morphisms[i])) == F2(simp).F1(simplex.morphisms[i]), "Functorality failed: " + F1(simp.F1(simplex.morphisms[i])).label +" != " +F2(simp).F1(simplex.morphisms[i]).label

#Check if
#subcategory a precategory is a subcategory if the inclusion graphMap is a faithfull prefunctor
def isFaithfull(F):
    if len(F.graphMap.obImage) == len(F.domain.multigraph.objects) and len(F.graphMap.morImage) == len(F.domain.multigraph.morphisms):
        return True
    else:
        return False
