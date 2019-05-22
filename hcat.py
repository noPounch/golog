import itertools
from copy import copy

# Create a new simplex with specified faces and kwargs
# Usage: Simplex(level, faces, *args, **{label:'', data:dict())
class Simplex():
    def __init__(self, n, faces = (), *args, **kwargs):


        # Check face data
        assert (len(faces) == n+1 or n==0), str(n)+"Simplecies MUST have "+ str(n+1) + "faces"
        for face in faces: assert (face.level == n-1 ), "Faces MUST be Simplecies of level "+str(n-1)

        # Set level and faces
        self.level = n
        self.faces = faces

        #check functorality
        if n>1:
            for j in range(n+1):
                for i in range(j):
                    assert self.faces[j].faces[i] == self.faces[i].faces[j-1], "Functorality Violated at: " + self.faces[j].faces[i].label+ " != " + self.faces[i].faces[j-1].label

        #Apply Kwargs
        defaults = {'label':'','data':dict()}
        for key in defaults:
            if key in kwargs: setattr(self,key,kwargs[key])
            else: setattr(self,key,defaults[key])

    def copy(clean = False):
        # return a new simplex supported on new simplecies
        # is shallow in that underlying data isn't changed
        # passing clean destroys all kwargs
        pass

#return a simplex of height n with a single simplex
def createSimplex(n,*args, **kwargs):
    sSet = simpSet()
    # create a new simplex and pass kwargs
    def createMessySimplex(n,*args, **kwargs):
        faces = []
        level = n

        if n == 0: return Simplex(0,*args,**kwargs)

    #Create new faces with new kwargs
        for i in range(n+1):
            nkwargs = copy(kwargs)
            nkwargs["label"] = nkwargs["label"] + str(i)
            s = createMessySimplex(n-1,*args,**nkwargs)
            faces.append(s)


    #re-arrange faces to satisfy functorality
        if n>1:
            for j in range(len(faces)):
                for i in range(j):
                    faces[j].faces[i] = faces[i].faces[j-1]
                    faces[j].faces[i].faces = tuple(faces[j].faces[i].faces)

        # clean deleted simplecies from 2 levels down
        # change simplex faces (from 2 levels down) to tuples

    ### CLEAN DELETED SIMPLECIES

        return Simplex(n,faces,*args,**kwargs)

    s = createMessySimplex(n, *args, **kwargs)
    def recursiveAdd(s,sSet):
        if not isinstance(s.faces,tuple):
            for f in s.faces:
                recursiveAdd(f,sSet)
            s.faces = tuple(s.faces)
        sSet.add(s)
    recursiveAdd(s,sSet)
    return s



class simpSet:
    def __init__(self,*args,**kwargs):

    #simps stored in a dictionary, indexed by their Faces
        defaults = {'label':'','simplecies':dict(),'data':dict()}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,defaults[key])

        self.rawSimps = list(set(itertools.chain(*list(self.simplecies.values()))))
        self.height = max([simp.level for simp in self.rawSimps]+[-1])

    def copy(self,**kwargs):
        #Shallow copy: different sset and attributes, same simplecies
        #If you want to copy certain attributes you have to pass them through kwargs

        newSimps = dict() #create a new simplicial set, with options to change arguements
        for key in self.simplecies.keys():
            newSimps[key] = []
            for simp in self.simplecies[key]:newSimps[key].append(simp)
        return simpSet(simplecies = newSimps,**kwargs)

    #append simplicial set to current simplicial set
    # def appendsSet(self,sSet):
    #     for key in sSet.simplecies.keys():
    #         for simp in sSet.simpleces

    def add(self,ob,*args, **kwargs):

        #raw addSimplex, will add simplex to sSet without
        #caring if faces are in sSet (used to add objects)
        def addSimplex(simp):
            if simp.faces not in list(self.simplecies.keys()):
                self.simplecies[simp.faces] = []
            if simp not in self.simplecies[simp.faces]:
                self.simplecies[simp.faces].append(simp)
                self.rawSimps.append(simp)
                self.height = max(self.height, simp.level)

        #recursively add simplecies and all supporting simplecies
        def recursiveAdd(simp):
            for f in simp.faces:
                if f not in self.rawSimps:
                    # print(f.label)
                    recursiveAdd(f)
            addSimplex(simp)

        #if ob is a simplex, recursively add it
        if isinstance(ob,Simplex):
            recursiveAdd(ob)
            return ob

        #if ob is a Simplicial set, add all of it's simplecies
        elif isinstance(ob, simpSet):
            for s in ob.rawSimps:
                self.add(s)
            return self

        #if ob is a list (of faces) add a new simplex with those faces
        elif isinstance(ob, tuple):
            n = ob[0].level+1
            s = Simplex(n,ob,*args,**kwargs)
            self.add(s)
            return s

        #if ob is an integer, create a whole new simplex and add all supports
        elif isinstance(ob, int):
            s = createSimplex(ob,*args,**kwargs)
            self.add(s)
            return s

    def hom(self, A ,B):
        if [A,B] in self.simplecies.keys(): return self.simplecies[[A,B]]
        return False





class Functor:
    def __init__(self,dom,codom,F , **kwargs):
        for simp in dom.rawSimps:
            assert F(simp) in codom.rawSimps, "F(" + simp.label + ") not in " + codom.label
            assert tuple(map(F,simp.faces)) == F(simp).faces, "Functorality Failed at: "+simp.label

        #apply args
        self.dom = dom
        self.codom = codom
        self.F = F
        #apply Kwargs
        defaults = {'label':'\'\''}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))
