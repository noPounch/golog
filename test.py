from cat import *
import sm






#graphs and #graphmaps
#simplecial graphs
C = simpSet(label = "C")
a = C.addSimplex(0,label = "a")
b = C.addSimplex(0,label = "b")
c = C.addSimplex(0,label = "c")
f = C.addSimplex(1,a,b, label = "f")

g = C.addSimplex(1,b,c, label = "g")
h = C.addSimplex(1,a,c, label = "h")
S = C.addSimplex(2,f,g,h,label = "gof = h")



print([s.label for s in C.rawSimps])
print(C.label + ": ",[[s.label for s in slist] for slist in C.simplecies.values()], "height = "+str(C.height))
print([s.label for s in C.hom(a,b)])


D = C.copy(label = "D")
D.simplecies.pop(()) #remove objects

sub  = D.simplecies

Dp = sm.completeDown(sub)

print(Dp.label + ": ",[[s.label for s in slist] for slist in Dp.simplecies.values()], "height = "+str(Dp.height))
