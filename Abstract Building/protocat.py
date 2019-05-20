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


#return a simplicial set of height n with a single simplex
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
    #print([f.label for f in s.faces])
    def recursiveAdd(s,sSet):
        if not isinstance(s.faces,tuple):
            for f in s.faces:
                recursiveAdd(f,sSet)
            s.faces = tuple(s.faces)
        sSet.addSimplex(s)
    recursiveAdd(s,sSet)
    return sSet

class simpSet:
    def __init__(self,*args,**kwargs):

    #simps stored in a dictionary, indexed by their Faces
        defaults = {'label':'\'\'','simplecies':'dict()'}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

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

    def recursiveAdd(self,simp):
        for f in simp.faces:
            if f not in self.rawSimps:
                self.recursiveAdd(f)
        self.addSimplex(simp)

    def addSimplex(self, simp, *args, **kwargs):
        if isinstance(simp, simpSet): print("sSet") #append simplecies to self

        #if given faces, create a new simplex with faces
        elif isinstance(simp, list):
            #print("list")
            s = Simplex(simp[0].level, simp, *args, **kwargs)

        #if given number, create a completely new simplex
        elif isinstance(simp, int):
            #print("int")
            s = createSimplex(n, *args, **kwargs)
            #union sSet with current sSet
            ### ADD ALL SUB SIMPLECIES TOO

        #continue with given simplex
        elif isinstance(simp, Simplex):
            #recursively add the faces of a simplex
            # for f in simp.faces:
            #     if f not in self.rawSimps:
            #         self.addSimplex(f)
            # self.addSimplex(simp)
            s = simp


        else: return
        #print(self.simplecies)
        #add index faces to simplecies dictionary
        if s.faces not in list(self.simplecies.keys()):
            self.simplecies[s.faces] = []
        if s not in self.simplecies[s.faces]:
            self.simplecies[s.faces].append(s)
            self.rawSimps.append(s)
        self.height = max(self.height, s.level)

    def hom(self, A ,B):
        if [A,B] in self.simplecies.keys(): return self.simplecies[[A,B]]
        return False






######### TESTING #######
sSet = simpSet()
S = createSimplex(2,label = "S")
for s in S.rawSimps:
    sSet.recursiveAdd(s)

keychain = [[f for f in faces] for faces in list(S.simplecies.keys())]
print([[f.label for f in faces] for faces in list(S.simplecies.keys())])
print([f.label for f in S.simplecies[tuple(keychain[0])]])
