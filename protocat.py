import itertools
from copy import copy


class Simplex():
    def __init__(self, n, faces = [], *args, **kwargs):

        assert (len(faces) == n+1 or n==0), str(n)+"Simplecies MUST have "+ str(n+1) + "faces"
        for face in faces:
            assert (face.level == n-1 ), "Faces MUST be Simplecies of level "+str(n-1)

        self.level = n
        self.faces = faces
        if n>1:
            for j in range(n+1):
                for i in range(j):
                    assert self.faces[j].faces[i] == self.faces[i].faces[j-1], "Functorality Violated at: " + self.faces[j].faces[i].label+ " != " + self.faces[i].faces[j-1].label

        defaults = {'label':'','data':None}
        for key in defaults:
            if key in kwargs: setattr(self,key,kwargs[key])
            else: setattr(self,key,defaults[key])



def createSimplex(n,*args, **kwargs):
    faces = []
    if n == 0: return Simplex(0,faces,*args,**kwargs)

    for i in range(n+1):
        nkwargs = copy(kwargs)
        nkwargs["label"] = nkwargs["label"] + str(i)
        s = createSimplex(n-1,*args,**nkwargs)
        faces.append(s)

    #re-arrange faces to satisfy functorality
    if n>1:
        for j in range(len(faces)):
            for i in range(j):
                print(i,j)
                print(len(faces[j].faces))
                faces[j].faces[i] = faces[i].faces[j-1]


    return Simplex(n,faces,*args,**kwargs)

s = createSimplex(2,label = "s")



print([f.label for f in s.faces])
