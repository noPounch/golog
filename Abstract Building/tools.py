from pandas import DataFrame, Series

#Builds a Function by input x output database on the fly
class functionBuilder:
    def __init__(self):
        self.df = DataFrame([],index = [0])

    def addValue(self,input,output):
        if not isinstance(input, tuple):
            raise Exception("input must be a tuple")
            return
        self.df[input] = Series([output],index = [0])

    def eval(self,input):
        return self.df[input][0]
