from hcat import *
import itertools

#helper_functions
#models A -f-> P(B) -P(g)-> P(P(C)) -U-> P(C)
def U(set_of_sets):
    U = set()
    for Set in set_of_sets: U = U|Set
    return U

def P0(Set):
    List = list(Set)
    return frozenset([frozenset(tup) for tup in list(itertools.chain.from_iterable(itertools.combinations(List, r) for r in range(len(List)+1)))])


def P1(f): return lambda subset: frozenset(f(x) for x in subset)

def Kleisli_Compose(g,f):
    Pg = P1(g)
    return lambda x:U(Pg(f(x)))

class eSimplex():
    def __init__(self, n,*args, **kwargs):
        defaults = {'label':'\'\'', 'faces':'(set())'}
        for key in defaults:
            if key in kwargs: setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

        #assertions
        #list length
        assert len(self.faces) == n+1 or n==0, str(n)+"-eSimplecies must have "+str(n+1)+" face_sets"
        #level assumption
        for face_set in self.faces:
            for face in face_set:
                assert isinstance(face, eSimplex), 'Faces should be eSimplecies'
                assert face.level == n-1, "Every face in the face_sets of an " + str(n)+"-esimplex must be an "+str(n-1)+ "-esimplex"
        #functorality (check that the Kleisli Composition gives the same face sets)
        if n>1:
            for j in range(n+1):
                for i in range(j):
                    assert U(face.faces[i] for face in self.faces[j]) == U(face.faces[i] for face in self.faces[j-1]), 'functorality violated (somewhere)'

        self.level = n

#from a simplex, return the esimplex with faces = {faces}
def brak(simplex):
    return eSimplex(simplex.level, faces = tuple([{(brak(face))} for face in simplex.faces]))

    # def add(face):
    #     assert


#
# class seSet():
#     defaults = {'label':'','submorphisms':dict()}
#     for key in defaults.keys():
#         if key in kwargs.keys(): setattr(self,key,kwargs[key])
#         else: setattr(self,key,defaults[key])




a = Simplex(0)
b = Simplex(0)
c = Simplex(1, faces = (a,b))
C = brak(c)
