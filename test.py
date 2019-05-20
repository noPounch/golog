from hcat import *
#import sm



C = simpSet(label = "C")
s = createSimplex(2,label = "s")
C.add(s)

D = simpSet(label = "D")
D.add(s)

F = lambda x: x
Functor(C,D,F)

for s in C.rawSimps: print("F(" +s.label + ") = " + F(s).label)


#graphs and #graphmaps
#simplecial graphs
