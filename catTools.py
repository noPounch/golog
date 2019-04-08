import tools
from cat import *

#Input UF:C.underlyingMultigraph() -> G
def induce(UF):
    if not isinstance(UF,graphMap):
        return False
        raise Exception("UF needs to be a graphMap")

    #if UF is already a functor, don't recompute, just return it's prefunctor
    if UF.isFunctor:return UF.asFunctor
    #Domain needs to be a precategory
    if UF.domain.workingPrecategory == None:
        return False
        raise Exception("UF.domain needs to come from a precategory")

    #Check if codomain already has a precategory structure if so, return asPrefunctor
    if UF.codomain.workingPrecategory != None: return UF.asFunctor

    #create a new multigraph

    #create identities and indentity simplecies


    FrD = UF.codomain.asPrecategory()

    #for each simp in domain simplecies, build it's image simplex
    for simp in UF.domain.simplecies.listImage(): D.addSimplex(UF.F1(simp.F1(f)) for f in simplex.morphisms)
