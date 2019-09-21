from hcat import *
from golog import *
from direct.showbase.ShowBase import ShowBase



S = simpSet(label = 'My First sSet')

a = S.add(0, label = 'a')
b = S.add(0, label = 'b')
c = S.add(0, label = 'c')

f = S.add((b,a), label = 'f')
g = S.add((c,b), label = 'g')
h = S.add((c,a), label = 'h')

simp = S.add((g,h,f))


print([simp.label for simp in S.rawSimps])
print([face.label for face in simp.faces])


class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        G = golog(self, label = 'My First Golog')
        a = G.add(0, label = 'a', pos = (0,0,0))
        b = G.add(0, label = 'b', pos = (1,0,1))
        c = G.add(0, label = 'c', pos = (2,0,3))

        f = G.add((b,a), label = 'f')
        g = G.add((c,b), label = 'g')
        h = G.add((c,a), label = 'h')




app  = runner()
app.run()
