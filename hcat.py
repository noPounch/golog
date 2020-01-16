import itertools, os
from copy import copy
import tk_funcs



class Math_Data():
    def __init__(self,**kwargs):
        #math_data stores type, actual math data, and a function to delete it
        defaults = {'type':'\'None\'', 'math_data':'None'}
        for key in defaults:
            if key in kwargs: setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

    def delete(self,folder_path):

        if self.type == 'simpSet':
            #add handlers later, if needed.
            pass

        if self.type == 'golog':

            golog_dict = self.math_data
            #close window and remove mode_head if it has one
            golog = golog_dict['golog']
            if hasattr(golog,'mode_heads'):
                for mode_head in golog.mode_heads.values():
                    mode_head.reset()
                    mode_head.clean()

            folder_path = os.path.join(folder_path, *golog_dict['folder_path'])
            tk_funcs.ask_delete_path(folder_path)

        elif self.type == 'file':

            abs_file_path = os.path.join(folder_path,*self.math_data)
            tk_funcs.ask_delete_path(abs_file_path)

        elif self.type == 'latex':

            folder = os.path.join(folder_path, *self.math_data['folder'])
            tk_funcs.ask_delete_path(folder)

        elif self.type == 'weblink':
            pass #will ultimately just get deleted by overwriting
        print(self.type + ' Data Deleted')


    def __call__(self):
        return self.math_data


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

        #Apply default kwargs
        defaults = {'label':'\'\'','data':'dict()','math_data':'Math_Data()'}
        for key in defaults:
            if key in kwargs: setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))

        self.supports = []
        #add simplex to the list of supported simplecies
        for face in self.faces: face.supports.append(self)

    def copy(self):
        new = createSimplex(self.level)
    
    def pprint(self,level = 0):

        math_data = self.math_data()
        print( 4*level*'_'+' '+ self.label)

        if self.math_data.type == 'golog': rawSimps = math_data['golog'].sSet.rawSimps
        elif self.math_data.type == 'simpSet': rawSimps = math_data.rawSimps
        else: rawSimps = []
     
        for simp in rawSimps:
            if simp.level == 0: simp.pprint(level = level + 1)
        






#return a simplex of height n with a single simplex
def createSimplex(n,*args, **kwargs):
    if not 'label' in kwargs.keys():kwargs['label'] = str(n)+'-simplex'
    sSet = simpSet(label = "temp_simplicial_set_for_creating_simplex ")
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



    # functionality for adding simplecies, creating new ones, or inheriting an entire simplicial set
    def add(self,ob,*args, **kwargs):
        #raw addSimplex, will add simplex to sSet without
        #caring if faces are in sSet (used to add objects)
        def addSimplex(simp):
            if simp in self.rawSimps: return
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
                    recursiveAdd(f)
            addSimplex(simp)

        #if ob is a simplex, recursively add it
        if isinstance(ob,Simplex):
            recursiveAdd(ob)
            return ob

        #if ob is a Simplicial set, add all of it's simplecies
        elif isinstance(ob, simpSet):
            for s in ob.rawSimps:
                recursiveAdd(s)
            return self

        #if ob is a list (of faces) add a new simplex with those faces
        elif isinstance(ob, tuple):
            if len(ob)==0:
                s = Simplex(0,*args,**kwargs)
                recursiveAdd(s)

                return s
            n = ob[0].level+1
            s = Simplex(n,ob,*args,**kwargs) #this will throw errors if simplex assumptions are violated
            recursiveAdd(s)
            return s

        #if ob is an integer, create a whole new simplex and add all supports
        elif isinstance(ob, int):
            s = createSimplex(ob,*args,**kwargs)
            recursiveAdd(s)
            return s

    #return the hom_set of two 0-simplecies
    def hom(self, A ,B):
        if [A,B] in self.simplecies.keys(): return self.simplecies[[A,B]]
        return ()

    #recursively remove a simplex and it's math_data
    def remove(self,simplex, delete = False):
        print('removing '+simplex.label)
        assert simplex.supports == [], "simplex "+simplex.label+" still supports \n"+str([sup.label for sup in simplex.supports])
        for face in simplex.faces: face.supports.remove(simplex)
        self.simplecies[simplex.faces].remove(simplex)
        self.rawSimps.remove(simplex)
        if delete: del simplex


#functor takes a function F:dom.simplecies --> codom.simplecies and checks assertions
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



    def __call__(self,simplex):
        assert simplex in self.dom.rawSimps
        return self.F(simplex)

#create an isomorphic simplicial set with no math_data
def stripsSet(sSet):
    newsSet = simpSet(label = sSet.label)
    old_to_new = dict()
    def strip_and_add(simp):

        #if simp has already been handled, return it
        if simp in old_to_new.keys():
            # print(simp.label+" already in new sSet")
            return old_to_new[simp]
        # print("adding stripped "+simp.label)
        #if s hasn't yet been handled, handle faces
        newfaces = tuple(strip_and_add(f) for f in simp.faces)
        #once faces are handled, create a new simplex
        newsimp = newsSet.add(newfaces, label = simp.label)
        old_to_new[simp] = newsimp
        return newsimp

    for simp in sSet.rawSimps:
        strip_and_add(simp)

    old_to_new_functor = Functor(sSet,newsSet,lambda x:old_to_new[x])
    return old_to_new_functor

#class which asserts the submorphism conditions
###### SOON TO BE DEPRECIATED AND REPLACED BY SIMPLCIAL EXPANSION SETS#########
class submorphism(simpSet):
    ''' A submorphism is a simplicial set who's n-simplecies are (n-1)-simplecies (from an ambient sSet containing both its dom and codom) '''
    def __init__(self, dom, codom, *args, **kwargs):
        simpSet.__init__(self,*args,**kwargs)
        assert isinstance(dom, simpSet) and isinstance(codom, simpSet), 'a submorphism is between two simplicial sets'
        self.dom = stripsSet(dom)
        self.codom = stripsSet(codom)
        super(submorphism, self).add(self.dom.codom)
        super(submorphism, self).add(self.codom.codom)
        self.add(self.dom)
        self.add(self.codom)

    def add(self, ob , *args,**kwargs):

        def addSimplex(simp):
            if simp in self.rawSimps: return simp
            if simp.faces not in list(self.simplecies.keys()):
                self.simplecies[simp.faces] = []
            if simp not in self.simplecies[simp.faces]:
                self.simplecies[simp.faces].append(simp)
                self.rawSimps.append(simp)
                self.height = max(self.height, simp.level)

            return simp

        #recursively add simplecies and all supporting simplecies
        #checks that simplecies are supported on 0-simplecies in the image of the domain and codomain functors
        def recursiveAdd(simp):

            if simp.level == 0: return
            elif simp.level == 1:
                #assert the faces are in the image of the functors domain and codomin
                assert simp.faces[1] in self.dom.codom.rawSimps, simp.label + ' face ' + simp.faces[1].label +' not in domain'
                assert simp.faces[0] in self.codom.codom.rawSimps, simp.label + ' face ' + simp.faces[0].label +' not in codomain'
                return addSimplex(simp)
            else:
                for f in simp.faces:
                    if f not in self.rawSimps:
                        recursiveAdd(f) #if this fails, it's because of a support issue, thus the whole thing will be cancel
                return addSimplex(simp)



        if isinstance(ob,Simplex):
            assert ob.level != 0, 'submorphism simplecies must not be 0-simplecies'
            recursiveAdd(ob)
            return ob

        #if ob is a Simplicial set, add all of it's simplecies
        elif isinstance(ob, simpSet):
            assert (not ob.simplecies[()]), "submorphism can't inherit sSets with 0-simplecies"
            for s in ob.rawSimps:
                recursiveAdd(s)
            return self

        #if ob is a list (of faces) add a new simplex with those faces
        elif isinstance(ob, tuple):
            if not ob: return
            n = ob[0].level+1
            s = Simplex(n,ob,*args,**kwargs) #this will throw errors if simplex assumptions are violated
            recursiveAdd(s) # this will throw errors if there are support issues
            return s

#a function to get the simplicial set of subsimplicial sets and submorphisms
#a class with helper functions for analyzing simplex's math_data which MUST be a simplicial set of some type (submorphism or otherwise)
def sm(sSet, *args, **kwargs):
    sm_sSet = simpSet(label = 'sm( '+sSet.label+' )')
    #complete downward for a list of simplecies
    def complete_down(rawSimps):
        completed_sSet = simpSet()
        for simp in rawSimps: completed_sSet.add(simp)
        return completed_sSet

    raw_power = list(itertools.chain.from_iterable(itertools.combinations(sSet.rawSimps, r) for r in range(len(sSet.rawSimps)+1)))
    completed_list = []
    completed_raw_list = []
    for raw_list in raw_power:
        completed_sSet = complete_down(raw_list)
        if not (set(completed_sSet.rawSimps) in completed_raw_list):
            completed_raw_list.append(set(completed_sSet.rawSimps))
            completed_list.append(completed_sSet)

    for completed_sSet in completed_list:
        #package sSet into a math_data
        wrapped_sSet = Math_Data(math_data = completed_sSet, type = 'sSet')
        # add a 0-simplex with the math_data
        sm_sSet.add(0,math_data = wrapped_sSet)

    return sm_sSet

    #need to convert to set and check that it's not in it
    #check if list of rawSimps is already the math_data of some simplex







### TESTING ###
if __name__ == '__main__':
    s = simpSet()
    a = s.add(0,label = 'a_s')
    b = s.add(0,label = 'b_s')
    f = s.add((b,a),label = 'f_s')
    raw = sm(s)

    s2 = simpSet()
    a2 = s2.add(0,label = 'a_s2')
    b2 = s2.add(0,label = 'b_s2')
    f2 = s2.add((b2,a2),label = 'f_s2')

    sub = submorphism(s,s2,label = 'sub_test')
    a = sub.dom.codom.rawSimps[0]
    b = sub.codom.codom.rawSimps[0]
    sub.add((b,a),label = 'new guy')
    f = Simplex(1,faces = (b,a),label = 'new RAW guy, my dude')
    sub.add(f)

    A = Simplex(0,label = 'hi', math_data = Math_Data(type = 'simpSet', math_data = s))
