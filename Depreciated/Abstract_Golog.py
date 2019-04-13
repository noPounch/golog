
from cat import *
import tools

#Want to build a category of objects
golog = precategory(label = "golog")

#an object will be instanciated with "graphical data"
obGdata = (2,3)

#on rightclick
o = golog.addObject(label = "test", data = obGdata)

def addCircle(**params):
    graphics = None
    o =  golog.addObject(data = graphics,**params)

print(o.label,o.data, o.multigraph)
