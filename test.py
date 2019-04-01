from cat import *

################ TESTING
C = precategory(label = "C")
a_C = C.addObject("a_C")
b_C = C.addObject("b_C")
c_C = C.addObject("c_C")
f_C = C.addMorphism(a_C,b_C,"f_C")
g_C = C.addMorphism(b_C,c_C,"g_C")
gof_C = C.addMorphism(a_C,c_C,"gof_C")
simp_C = C.addSimplex(f_C,g_C,gof_C)


D = precategory(label = "D")
a_D = D.addObject("a_D")
b_D = D.addObject("b_D")
c_D = D.addObject("c_D")
f_D = D.addMorphism(a_D,b_D,"f_D")
g_D = D.addMorphism(b_D,c_D,"g_D")
gof_D = D.addMorphism(a_D,c_D,"gof_D")
simp_D = D.addSimplex(f_D,g_D,gof_D)

F0 = lambda o:D.multigraph.objects[o.index]
F1 = lambda f:D.multigraph.morphisms[f.index]
F2 = lambda simp:D.simplecies.listImage()[simp.index]
Id_C = prefunctor(C,C,lambda x:x,lambda x:x,lambda x:x)
#print(isFaithfull(Id_C))
F = prefunctor(C,D,F0,F1,F2,label = 'F')
#print(F.graphMap.label)
#print(F.graphMap.prefunctor)
print(Id_C.graphMap.isPrefunctor())
