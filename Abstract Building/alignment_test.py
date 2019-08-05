# for two panda nodes, a middle node, and a rope, align cone graphics to point along tangent
from direct.showbase.ShowBase import ShowBase
from math import cos, sin, sqrt, pi, atan, acos


def norm(vector):
    return sqrt(sum([x**2 for x in vector]))


class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()
        self.sphere = base.loader.loadModel("../models/sphere.egg.pz")
        self.cone = base.loader.loadModel('../models/Cone.egg')

        #camera
        self.camera.setPos(0,-100,0)

        #make node1
        self.node1 = self.render.attachNewNode('node1')
        self.sphere.instanceTo(self.node1)
        self.node1.setPos(10,0,0)

        #make middleNode
        self.middleNode = self.render.attachNewNode('middle')
        self.cone.instanceTo(self.middleNode)
        #create z basis vector for cone
        self.zbasis = self.middleNode.attachNewNode('zbasis')
        self.zbasis.setPos(0,0,1);
        xbasis = self.middleNode.attachNewNode('xbasis')
        xbasis.setPos(1,0,1);
        self.sphere.instanceTo(self.zbasis)
        # self.rotateTo(self.middleNode, zbasis, self.node1)
        base.taskMgr.add(self.rotateTask, 'rotate')






    def rotateTo(self, node, nodez, to_node):
        #get z vector
        zvect = tuple(nodez.getPos(self.render)-node.getPos())
        #get dirr vector
        diffvect = to_node.getPos() - node.getPos()
        dirrvect = tuple(diffvect/norm(tuple(diffvect)))

        #transform z to spherical
        (x1,y1,z1) = zvect
        if x1 != 0: theta1 = atan(y1/x1)
        else: theta1 = 0
        phi1 = acos(z1)
        print(theta1,phi1)


        #transform dirr to spherical
        (x2,y2,z2) = dirrvect

        if x2 != 0: theta2 = atan(y2/x2)
        else: theta2 = 0
        phi2 = acos(z2)
        print(theta2,phi2)
        #get angular difference, dphi = (sph(dirr)-sph(z))90/pi
        dphi = (phi2-phi1)*180/pi
        dtheta = (theta2-theta1)*180/pi

        #setHpr(getHpr()+(dphi,0))
        node.setHpr(node.getHpr()+ (dtheta,0,0))
        node.setHpr(node.getHpr()+ (0,0,dphi))



    def rotateTask(self, task):
        t = task.time
        self.node1.setPos(0,10*cos(t),10*sin(t))
        self.rotateTo(self.middleNode, self.zbasis, self.node1)


        return task.cont





r = runner()
render = r.render
r.run()
