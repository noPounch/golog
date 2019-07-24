from hcat import Simplex, simpSet, Functor

def stripSimp(simp):
    newsimp = Simplex(label = simp.label)

#strip a simplicial set of it's math_data
#return a functor associating the sSet with math_data to the sSet without
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


def open_math_data(simplex):
    # open actual math data and provide callback
    return simplex.math_data.open(simplex.Math_Data())
