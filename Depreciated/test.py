from cat import *
from tools import *
import subcategories
import catTools

################ TESTING
C = precategory(label = "C")
a_C = C.addObject(label = "a_C")
b_C = C.addObject(label = "b_C")
c_C = C.addObject(label = "c_C")
f_C = C.addMorphism(a_C,b_C,label = "f_C")
g_C = C.addMorphism(b_C,c_C,label = "g_C")
gof_C = C.addMorphism(a_C,c_C,label = "gof_C")
simp_C = C.addSimplex(f_C,g_C,gof_C)


D = precategory(label = "D")
a_D = D.addObject(label = "a_D")
b_D = D.addObject(label = "b_D")
c_D = D.addObject(label = "c_D")
f_D = D.addMorphism(a_D,b_D,label = "f_D")
g_D = D.addMorphism(b_D,c_D,label = "g_D")
gof_D = D.addMorphism(a_D,c_D,label = "gof_D")
simp_D = D.addSimplex(f_D,g_D,gof_D)

UD = multigraph(label = 'U(D)')
a_UD = UD.addObject(label = "a_uD")
b_UD = UD.addObject(label = "b_uD")
c_UD = UD.addObject(label = "c_uD")
f_UD = UD.addMorphism(a_UD,b_UD,label = "f_uD")
g_UD = UD.addMorphism(b_UD,c_UD,label = "g_uD")
gof_UD = UD.addMorphism(a_UD,c_UD,label = "gof_uD")


#Obdict = {a_C:a_UD,b_C:b_UD,c_C:c_UD}
#Mordict = {f_C:f_UD,g_C:g_UD,gof_C:gof_UD}
F0 = lambda o:D.workingMultigraph.objects[o.index]
F1 = lambda f:D.workingMultigraph.morphisms[f.index]
F2 = lambda simp:D.simplecies.listImage()[simp.index]
# UId_C = graphMap(C.multigraph,C.multigraph,lambda x:x,lambda x:x)
# Id_C = prefunctor(C,C,lambda x:x,lambda x:x,lambda x:x)
F = prefunctor(C,D,F0,F1,F2,label = 'F')
# def UF1(f):
#     if f in Mordict.keys():
#         return Mordict[f]
#
#
#UF = graphMap(C.multigraph, UD, lambda o:Obdict[o], lambda o:Mordict[o])
UF = graphMap(C.workingMultigraph,D.workingMultigraph,F0,F1)
G = UF.asPrefunctor()
# print([G.F0(o) == F.F0(o) for o in C.multigraph.objects])

#print(F.graphMap.label)
#print(F.graphMap.prefunctor)
#print(Id_C.graphMap.isPrefunctor())
#print([[F.F1(f).label for f in simplex.morphisms[3:]] for F in D.simplecies.listImage()])
#subcategories.getSubcategories(C)
