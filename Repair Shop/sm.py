import cat

#create a category of small categories and submorphisms, with a notion of 2-simplex (as composition of submorphisms)

#A subsimplicial set is a downwardly complete subset of rawSimps (i.e. a monic natural transformation between simplicial sets)
#(imposing the extra simplicial axiom of degeneracy maps forces the necessity )
def completeDown(sub):
    #index simps by level
    lindSubs = dict()
    height = -1
    for sList in sub.values():
        #check if slist is empty first
        l = sList[0].level
        height = max(l,height)
        if l not in lindSubs.keys(): lindSubs[l] = []
        lindSubs[l] = lindSubs[l] + sList
    for l in range(0,height+1):
        if l not in lindSubs.keys(): lindSubs[l] = []
    #start at highest level, append faces, move down a level. if the faces are not in sub, add them.
    #Don't need to check faces of 0simplecies (if you do you will get an error when trying ob.faces.faces = ().faces)
    for l in range(height,0,-1):
        print(l)
        for simp in lindSubs[l]:
            print(simp.label)
            for fsimp in simp.faces:
                if fsimp not in lindSubs[l-1]:
                    if fsimp.faces not in sub.keys():sub[fsimp.faces] = []
                    if fsimp not in sub[fsimp.faces]: sub[fsimp.faces].append(fsimp)
    return cat.simpSet(simplecies = sub)




    newSimpSet = cat.simpSet()
    for simp in sub:

        for fsimp in simp.faces:
            if fsimp not in sub:



                sub.append(fsimp)

def sm(category):
    #create a simplicial set
    smC = cat.simpSet()
