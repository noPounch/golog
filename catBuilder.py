import cat
import catFuncs

from matplotlib import pyplot as plt
import matplotlib.patches as ptc
from numpy.linalg import norm


##GLOBAL VARS
global r
r = .05


class catBuilder:
    #####################
    #catBuilder INITIALIZATION
    #####################
    def __init__(self,figure):
        self.category = cat.category("Cat") #Create a category
        self.cid = figure.canvas.mpl_connect('button_press_event', self.click)
        self.numObs = 0
        self.numMors = 0
        self.obLocList = []
        self.obMemory = [None,None]


        #Activated when the lineBuilder is called
    def __call__(self, event):
        print('click', event)

    #################
    # Event Handlers
    #################




    def leftClick(self,event):
        loc = (event.xdata,event.ydata)
        name = self.numObs


        #Distances from all other objects
        obDist = [norm(tuple((x-y for x,y in zip(ob.graphics.get_center(),loc)))) for ob in self.category.obList]
        print(obDist)

        #if in bounds of an object: record last two
        for i in range(len(obDist)):
            if obDist[i] < r:
                if self.obMemory[1] != None:
                    self.obMemory[1].graphics.set_facecolor('blue')

                lastOb = self.obMemory[1] = self.obMemory[0]
                thisOb = self.obMemory[0] = self.category.obList[i]


                if thisOb != None:
                    thisOb.graphics.set_facecolor('red')


                if lastOb != None:
                    lastOb.graphics.set_facecolor('green')
                    #add morphism with dom = lastOb, codom = thisOb
                    #morName = self.numMors
                    #self.category.addMorphism(morName,lastOb,thisOb)
                    #self.numMors = self.numMors + 1


                    #print(mor.pr)


                #Change Graphics of selected and previously selected
                fig.canvas.draw()
                return self.category.obList[i]


        #if not in bounds of any other object reset memory and colors
        for i in [0,1]:
            if self.obMemory[i] != None:
                self.obMemory[i].graphics.set_facecolor('blue')
                fig.canvas.draw()
            self.obMemory[i] = None






    def rightClick(self,event):
        loc = (event.xdata,event.ydata)
        circ = ptc.Circle(loc,radius=r)
        name = self.numObs



        circ.set_figure(fig)
        ob = self.category.addObject(name,graphics=circ)
        ax.add_patch(circ)
        fig.canvas.draw()
        self.numObs = self.numObs + 1

    def click(self,event):
        if  event.button == 1:
            self.leftClick(event)
        if event.button == 3:
            self.rightClick(event)

#Initiate figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('attempt')
catbuilder = catBuilder(fig)
plt.show()
