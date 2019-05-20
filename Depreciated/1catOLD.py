import itertools

####### RULES OF THUMB #########
#the only free floating objects are simplecies
#to create a structure on top of an underlying strucutre, you must copy the underlying structure first.
#pass everything through *args and **kwargs and check internally
#store everything in dictionaries to create pre-computed functions
#lambda functions are all defined on actual instances, not their indecies
#Keywords for defining new objects from old stored in a defaults dictionary (this allows live instanciation instead of during compiling)


def Simplex(n, *simplecies,**kwargs):
    #do generalizable assertions here:
    for s in simplecies:
        assert isinstance(s,eval('Simplex'+str(n-1))), "Faces must be Simplecies of level "+ str(n-1)
    return eval('Simplex'+str(n)+'(*simplecies,**kwargs)')


#grouding object

#objects
class Simplex0:
        def __init__(self,*args,**kwargs):
            defaults = {'label':'\'\'','data':'None'}
            for key in defaults.keys():
                if key in kwargs.keys(): setattr(self,key,kwargs[key])
                else: setattr(self,key,eval(defaults[key]))

            self.faces = ()
            #degeneracy gives identity 1-simplex
            #self.degens = Simplex1(self,self,label = "Id_" + self.label)
            self.level = 0
            #assertions

#morphisms
class Simplex1:
    def __init__(self,*args,**kwargs):
        defaults = {'label':'\'\'','data':'None'}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

        #faces should be mutable,
        self.faces = tuple(args[0:2])
        #degeneracy gives identity 2-simplecies
        #domId = Simplex2(self.faces[0].degens,self,self,label = self.label  + " = "+  self.label + " o " + self.faces[0].degens.label)
        #codomId = Simplex2(self,self.faces[1].degens,self, label = self.label  + " = " + self.faces[1].degens.label+" o "+self.label)
        #self.degens = (domId,codomId)
        self.level = 1


#Commutative Triangles (f,g,gof)
class Simplex2:
    def __init__(self,*args,**kwargs):
        self.faces = tuple(args[0:3])
        self.level = 2
        defaults = {'label':'\'\'','data':'None'}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

        ###need to generalize assertions before can generalize to SimplexN
        #assert domains line up
        assert self.faces[0].faces[1] == self.faces[1].faces[0], "domain of " + self.faces[0].label + " != codomain of " + self.faces[1].label
        assert self.faces[2].faces[0] == self.faces[0].faces[0], "domain of " + self.faces[2].label + " != domain of " + self.faces[0].label
        assert self.faces[2].faces[1] == self.faces[1].faces[1], "codomain of " + self.faces[2].label + " != codomain of "  + self.faces[1].label




###########need to add coherance axioms: uniqueness, identity, associativity, don't need fullness, may need to add identities to simplecies
class simpSet:
    def __init__(self,**kwargs):
        #simplecies are stored in a dictionary, their key is their domain and codomain
        defaults = {'label':'\'\'','simplecies':'dict()'}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))
        self.rawSimps = list(set(itertools.chain(*list(self.simplecies.values()))))
        self.height = max([simp.level for simp in self.rawSimps]+[-1]) #givens largest simplex, returns -1 for empty simplicial set

    def copy(self,**kwargs):
        #Shallow copy: different sset and attributes, same simplecies (with faces,degens and data)
        #If you want to copy certain attributes you have to pass them through kwargs

        newSimps = dict() #create a new simplicial set, with options to change arguements
        for key in self.simplecies.keys():
            newSimps[key] = []
            for simp in self.simplecies[key]:newSimps[key].append(simp)
        return simpSet(simplecies = newSimps,**kwargs)


    def addSimplex(self,simp,*args,**kwargs): #add a simplex to simpSet.simplecies dictionary
        ######figure out how to check if faces are actually simplecies at all (may necessitate a global change to simplecies)
        if isinstance(simp,int): simp = Simplex(simp,*args,**kwargs) #if number is provided, add a new simplex (passing arguements)
        for F in simp.faces: assert F in self.simplecies[F.faces] #check if faces exist in simpSet
        if simp.faces not in list(self.simplecies.keys()): self.simplecies[simp.faces] = [] #add face key to simplex dictionary
        if simp not in self.simplecies[simp.faces]: #check if simplex is already in simpSet
            self.simplecies[simp.faces].append(simp)
            self.rawSimps.append(simp)
        self.height = max(self.height, simp.level)
        return simp

    def hom(self, A ,B):
        if [A,B] in self.simplecies.keys(): return self.simplecies[[A,B]]
        return False



def isFunctor(dom,codom,F,**kwargs):
    #F is a function of domain.simplecies
    #check domain and codomain are correct
    for simp in dom.rawSimps:
        if F(simp) not in codom.rawSimps:
            return (False,simp.label,F(simp).label,0)

    #functorality: sm(F) o OG_{-1} ==  OG_{-1} o F
    for simp in dom.rawSimps:
        if tuple(map(F,simp.faces)) != F(simp).faces:
            return (False, simp.label, F(simp).label ,1)

    return Functor(dom,codom,F,**kwargs)


class Functor:
    def __init__(self, dom, codom, F, **kwargs):
        self.dom = dom
        self.codom = codom
        self.F = F

        defaults = {'label':'\'\''}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))
