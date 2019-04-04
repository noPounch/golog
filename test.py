from cat import *
from tools import *
import subcategories

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

F0 = lambda o:D.multigraph.objects[o.index]
F1 = lambda f:D.multigraph.morphisms[f.index]
F2 = lambda simp:D.simplecies.listImage()[simp.index]
Id_C = prefunctor(C,C,lambda x:x,lambda x:x,lambda x:x)
#print(isFaithfull(Id_C))
#F = prefunctor(C,D,F0,F1,F2,label = 'F')
#print(F.graphMap.label)
#print(F.graphMap.prefunctor)
#print(Id_C.graphMap.isPrefunctor())
#print([[F.F1(f).label for f in simplex.morphisms[3:]] for F in D.simplecies.listImage()])


subcategories.getSubcategories(C)
