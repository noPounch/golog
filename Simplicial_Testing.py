import tools
import copy


#store everything in dictionaries to create pre-computed functions
#everything is defined in terms of simplecies
#lambda functions are all defined on actual instances, not their indecies
#Copy newly Made items (no references to overlying objects, uderlying must be copied and tied to a overlying object)
#Keywords for defining new objects from old stored in a defaults dictionary


def Simplex(n, *simplecies,**kwargs):
    #do generalizable assertions here:
    for s in simplecies:
        assert isinstance(s,eval('Simplex'+str(n-1))), "domain and codomain must be instances of Simplex"+str(n)
    return eval('Simplex'+str(n)+'(*simplecies,**kwargs)')



#objects
class Simplex0:
        def __init__(self,*args,**kwargs):
            defaults = {'label':'\'\'','data':'None'}
            for key in defaults.keys():
                if key in kwargs.keys(): setattr(self,key,kwargs[key])
                else: setattr(self,key,eval(defaults[key]))
    #morphisms
class Simplex1:
    def __init__(self,*args,**kwargs):
        self.S0 = list(args[0:2])
        defaults = {'label':'\'\'','data':'None'}
        for key in defaults.keys():
            if key in kwargs.keys(): setattr(self,key,kwargs[key])
            else: setattr(self,key,eval(defaults[key]))


class Simplex2:
    def __init__(self,*args,**kwargs):
        for f in list(args[0:4]):
            assert isinstance(f,Simplex1), "arguements must be instances of Simplex1"
        self.S1 = [args[0],args[1],args[2]]


##### Universe Objects

#graphs and #graphmaps
#simplecial graphs






A = Simplex(0,label = "A")
B = Simplex(0,label = "B")
f = Simplex(1,A,B, label = "f")
g = Simplex(1,A,B, label = "g")
h = Simplex(1,A,B, label = "h")
S = Simplex(2,f,g,h)
print([[o.label for o in olist]for olist in [f.S0 for f in S.S1]])
