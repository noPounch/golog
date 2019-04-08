import copy


#store everything in dictionaries to create pre-computed functions
#everything is defined in terms of simplecies
#lambda functions are all defined on actual instances, not their indecies





#Copy newly Made items (no references to overlying objects, uderlying must be copied and tied to a overlying object)
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


#####Graph ---> Simplicial Graph ((\inf,2)-simplicial set) ---> icategory (has identity)
####### RULES OF THUMB #########
#the only free floating objects are simplecies
#to create a structure on top of an underlying strucutre, you must copy the underlying structure first.
#pass everything through *args and **kwargs and check internally



###########need to add coherance axioms: uniqueness, identity, associativity, don't need fullness, may need to add identities to simplecies
class simpSet:
    def __init__(self,**kwargs):
        #simplecies are stored in a dictionary, their key is their domain and codomain
        defaults = {'label':'\'\'','simplecies':'dict()'}
        #set self.key = given or default value
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))
    def copy(self):
        #create a new graph object and return it
        pass

    #new addObject takes an actual 1-simplex and adds that to the list (and changes hom)
    def addSimplex(self,simp,*args,**kwargs):
        ######figure out how to check if faces are actually simplecies at all (may necessitate a global change to simplecies)
        if isinstance(simp,int): simp = Simplex(simp,*args,**kwargs) #if number is provided, add a new simplex (passing arguements)
        for F in simp.faces: assert F in self.simplecies[F.faces] #check if faces exist in graph
        if simp.faces not in list(self.simplecies.keys()): self.simplecies[simp.faces] = [] #add face key to simplex dictionary
        self.simplecies[simp.faces].append(simp)

        print([[s.label for s in slist] for slist in C.simplecies.values()])
        return simp











#graphs and #graphmaps
#simplecial graphs
C = simpSet()

A = Simplex(0,label = "A")
C.addSimplex(A)
B = C.addSimplex(0,label = "B")
D = C.addSimplex(0,label = "D")

f = Simplex(1,A,B, label = "f")
C.addSimplex(f)

g = C.addSimplex(1,B,D, label = "g")
h = C.addSimplex(1,A,D, label = "h")

S = C.addSimplex(2,f,g,h,label = "gof = h")
