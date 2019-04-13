import cat
import tools
from copy import copy


#return (category of) sub-precategories
def getSubcategories(C):
    #Create a precategory who's objects are subcategories, maps inclusion functors, of the category
    #Pass precategory instance to object.data
    subC = cat.precategory()
    Simps = C.simplecies.listImage()#S = get simplecies as list
    nonIDSimps = [] #remove identities (they will be added later with addObject + addMorphism)
    for simp in Simps:
        if not simp.isIdentity: nonIDSimps.append(simp)
    PS = tools.powerset(nonIDSimps)
    for subset in PS:

        #create a category and
        subcat = cat.precategory()
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
