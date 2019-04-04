import cat
import tools
from copy import copy


#return (category of) sub-precategories
def getSubcategories(C):
    #Create a precategory who's objects are subcategories, maps inclusion functors, of the category
    #Pass precategory instance to object.data
    subC = cat.precategory()
    #S = get simplecies as list
    Simps = C.simplecies.listImage()
    #remove identities (they will be added later with addObject + addMorphism)
    print(len(Simps))
    nonIDSimps = []
    for simp in Simps:
        print(simp.isIdentity,[simp.F1(cat.simplex.morphisms[i]).label for i in range(3)])
        if not simp.isIdentity: nonIDSimps.append(simp)

    for simp in nonIDSimps:
        print(simp.isIdentity,[simp.F1(cat.simplex.morphisms[i]).label for i in range(3)])
    PS = tools.powerset(nonIDSimps)
    i=0
    for subset in PS:

        #create a category and
        subcat = cat.precategory(label = str(i))
        i = i+1
        #get unique objects from original category
        objects = []
        #get unique non-identity morphisms
        morphisms = []
        newMorphisms = []
        #get simplecies
        for simp in subset:
            #get objects of simp
            for o in cat.simplex.objects:
                if simp.F0(o) in objects: pass
                else: objects.append(simp.F0(o))

            for f in cat.simplex.morphisms:
                if simp.F1(f) in morphisms: pass
                else: morphisms.append(simp.F1(f))


            #create a new



        for o in objects:
            subcat.addObject(label = o.label, data = o.data)

    print(i)
        #print([o.multigraph.label for o in subcat.multigraph.objects])
#
#        for f in morphisms:
#            newDom = C.multigraph.objects[objects.index(f.domain)]
#            newCodom = C.multigraph.objects[objects.index(f.codomain)]
#            print (f.domain.multigraph,newDom.multigraph)
#            subcat.addMorphism(newDom, newCodom, label = f.label, data = f.data)


#        subC = cat.precategory()

        #add simplex with copies maps and objects
        #simplecies.addValue((f,g),simp)
