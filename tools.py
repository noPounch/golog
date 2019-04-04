from itertools import chain, combinations


#lambda functions
def powerset(list):
    return chain.from_iterable(combinations(list , r) for r in range(len(list)+1))



class functionBuilder:
    def __init__(self,domain = [], function = lambda x:x):
        self.d = dict()
        for x in domain:
            self.d.update({x:f(x)})

    def __call__(self,o):
        return self.eval(o)


    def addValue(self,input,output):
        #if f(input) already exists return true/false if outputs are the same
        try: return output == self.d[input]
        #if self.d[input] raises an exception, catch and add f(input) = output
        except: self.d.update({input:output})

    def eval(self,input):
        try: return self.d[input]
        except: raise Exception("input is not defined in domain function")

    def listDomain(self):
        return list(self.d.keys())

    def listImage(self):
        return list(self.d.values())


#initializes attributes of sup from a dictionary of default {key:value}
#has a issue with resolving scope. Needs to somehow gain scope level of context where it is called.
# def keyInit(sup,defaults,kwargs):
#     for key in defaults.keys():
#         if key in kwargs.keys(): setattr(sup,key,kwargs[key])
#         else: setattr(sup,key,eval(defaults[key]))
