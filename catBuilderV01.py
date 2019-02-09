import cat
import catFuncs

from matplotlib import pyplot as plt
import matplotlib.patches as ptc
from numpy.linalg import norm


##GLOBAL VARS
global r
r = .05

class golog:
    def __init__(self,category):
        self.category = category
        self.numObs = 0
        self.circles = []
        self.connect()

    ############3
    #Event Handlers

    def connect(self):
        self.cidpress = fig.canvas.mpl_connect('button_press_event', self.on_press)


    def on_press(self,event):
        if event.button ==1:
            #check circles
            for c in self.circles:
                contains, attrd = c.circ.contains(event)
                #if click isn't on the circle disconnect it and switch it blue
                if not contains:
                     if c.connected: c.disconnect()
                     c.circ.set_facecolor('blue')
                     fig.canvas.draw()


                #if click is on circle connect it and change it to red
                if contains:
                    if not c.connected:
                        c.connect()
                    c.circ.set_facecolor('red')
                    fig.canvas.draw()


        if event.button == 3:
            c = self.addCircle(self.numObs,event)
            print(c.object.name)
            self.numObs = self.numObs +1


    ##############
    # Graphics creation
    def addCircle(self,name,event):
        loc = (event.xdata,event.ydata)
        circ = ptc.Circle(loc,radius=r)#first create Circle with center at the event
        circ.set_figure(fig)
        object = self.category.addObject(name,graphics = circ)#create object with name and circle graphics
        ax.add_patch(circ)
        fig.canvas.draw()

        c = circle(circ,self,object)
        self.circles.append(c)
        return c #Tie all together into circle and return it


class arrow:
    pass


class circle:
    def __init__(self,circ,golog,object):
        self.circ = circ
        self.golog = golog
        self.object = object
        self.press = None
        self.connected = False

    def connect(self):
        self.cidpress = self.circ.figure.canvas.mpl_connect('button_press_event', self.click)
        self.cidrelease = self.circ.figure.canvas.mpl_connect('button_release_event', self.release)
        self.cidmotion = self.circ.figure.canvas.mpl_connect('motion_notify_event', self.drag)
        self.connected = True
        print(self.object.name, "connected")

    def click(self,event):
        if event.inaxes != self.circ.axes: return
        contains, attrd = self.circ.contains(event)
        if not contains: return
        print('event contains', self.object.name)
        x0,y0 = self.circ.get_center()
        self.press = x0, y0, event.xdata, event.ydata

    def drag(self,event):
        if self.press is None:return
        if event.inaxes != self.circ.axes: return
        x_0,y_0,xpress,ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.circ.set_center((x_0+dx,y_0+dy))
        self.circ.figure.canvas.draw()

    def release(self,event):
        self.press = None
        self.circ.figure.canvas.draw()

    def disconnect(self):
        self.circ.figure.canvas.mpl_disconnect(self.cidpress)
        self.circ.figure.canvas.mpl_disconnect(self.cidrelease)
        self.circ.figure.canvas.mpl_disconnect(self.cidmotion)
        self.connected = False
        print(self.object.name, "disconnected")



fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('attempt')

C = cat.category("C")
G = golog(C)
plt.show()
