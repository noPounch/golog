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
            self.faces = ()
            self.level = 0
            defaults = {'label':'\'\'','data':'None'}
            for key in defaults.keys():
                if key in kwargs.keys(): setattr(self,key,kwargs[key])
                else: setattr(self,key,eval(defaults[key]))
            #assertions

#morphisms
class Simplex1:
    def __init__(self,*args,**kwargs):
        #faces should be mutable,
        self.faces = tuple(args[0:2])
        self.level = 1
        defaults = {'label':'\'\'','data':'None'}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

#Commutative Triangles
class Simplex2:
    def __init__(self,*args,**kwargs):
        self.faces = tuple(args[0:3])
        self.level = 2
        defaults = {'label':'\'\'','data':'None'}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

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

    def copy(self,**kwargs):
        #Shallow copy: different sset and attributes, same simplecies
        #If you want to copy certain attributes you have to pass them through kwargs

        newSimps = dict() #create a new simplicial set, with options to change arguements
        for key in self.simplecies.keys():
            newSimps[key] = []
            for simp in self.simplecies[key]:newSimps[key].append(simp)
        new = simpSet(simplecies = newSimps,**kwargs)
        return new


    def addSimplex(self,simp,*args,**kwargs): #add a simplex to simpSet.simplecies dictionary
        ######figure out how to check if faces are actually simplecies at all (may necessitate a global change to simplecies)
        if isinstance(simp,int): simp = Simplex(simp,*args,**kwargs) #if number is provided, add a new simplex (passing arguements)
        for F in simp.faces: assert F in self.simplecies[F.faces] #check if faces exist in graph
        if simp.faces not in list(self.simplecies.keys()): self.simplecies[simp.faces] = [] #add face key to simplex dictionary
        self.simplecies[simp.faces].append(simp)
        return simp

    def hom(self, A ,B):
        if (A,B) in self.simplecies.keys(): return self.simplecies[(A,B)]
        return False












#graphs and #graphmaps
#simplecial graphs
C = simpSet(label = "C")
a = C.addSimplex(0,label = "a")
b = C.addSimplex(0,label = "b")
c = C.addSimplex(0,label = "c")
f = C.addSimplex(1,a,b, label = "f")

g = C.addSimplex(1,b,c, label = "g")
h = C.addSimplex(1,a,c, label = "h")
S = C.addSimplex(2,f,g,h,label = "gof = h")
D = C.copy(label = "D")
print(C == D)
f1 = D.addSimplex(1,a,b, label = "f1")
D.addSimplex(0,label = "xX$ilect$pectorXx")


print(C.label + ": ",[[s.label for s in slist] for slist in C.simplecies.values()])
print(D.label + ": ",[[s.label for s in slist] for slist in D.simplecies.values()])
print([s.label for s in C.hom(a,b)])
print([s.label for s in D.hom(a,b)])
