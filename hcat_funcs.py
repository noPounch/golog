from hcat import Simplex, simpSet, Functor

def stripSimp(simp):
    newsimp = Simplex(label = simp.label)


def simpCopy(sSet):
    newsSet = simpSet(label = sSet.label+" stripped")
    old_to_new = dict()
    def strip_and_add(simp):

        #if simp has already been handled, return it
        if simp in old_to_new.keys():
            # print(simp.label+" already in new sSet")
            return old_to_new[simp]
        print("adding stripped "+simp.label)
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


sSet = simpSet(label = 'test')
a=sSet.add(0,label = 'a')
b=sSet.add(0,label = 'b')
c=sSet.add(0,label = 'c')
f= sSet.add((b,a),label = 'f')
g= sSet.add((c,b),label = 'g')
h= sSet.add((c,a),label = 'h')
s= sSet.add((g,h,f),label = 'gof = h')
F = simpCopy(sSet)
print([s.label for s in F.dom.rawSimps])
