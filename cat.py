import catFuncs
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
#A callable category is made up of objects and morphisms as well as a list
#of string references to them.


#Todo: Add class of commutative diagrams [f_i;g_j] such that
#1) dom(f_1) = dom(g_1)
#2) codom(f_n) = codom(g_m)
#3) codom(f_i) = dom(f_{i-1})



#Global Helper Functions
def homPrint(Hom):
    return [[[f.pr for f in hom] for hom in homi] for homi in Hom]

#Return simplified (for now) category under an object (from said category)
def categoryUnder(Category, Object):
    Ocat = category("Ocat")
    i = Category.obList.index(Object)


    #Pass Object into new Category
    O = Ocat.addObject(Object.name)
    #Pass endomorphisms into new category
    #Get everything except Identities (since they are added with addObject)
    for f in Category.hom(Object,Object)[1:]:
        #Pass morphism f:A -> Object to f:AO -> O
        Ocat.addMorphism(f.name,O,O)

    #run over all the objects in C except Object
    for A in Category.obList[:i]+Category.obList[i+1:]:
        #Check if Hom(A,Object) in Category is not empty
        if not not Category.hom(A,Object):
            #Pass A into new Ocat
            AO = Ocat.addObject(A.name)


            for f in Category.hom(A,Object):
                #Pass morphism f:A -> Object to f:AO -> O
                Ocat.addMorphism(f.name,AO,O)

    return Ocat

    #Initialize Variables


#Class Functor create a functor with ordered object associations
class Functor:
    def __init__(self,name,dom,codom,obMatrix,morMatrix):
        self.name = name
        self.dom = dom
        self.codom = codom
        #sends object dom.obList(i) to codom.obList(j) where obMatrix(i) = j
        self.obMatrix = obMatrix
        #sends morphism dom.morList(i) to codom.morList(j) where morMatrix(i) = j
        self.morMatrix = morMatrix


        ##################
        #assert morphisms compose
        ##################


class category:
    def __init__(self,name):
        self.name = name
        self.obList= []  #actual objects
        self.morList = []  #actual morphisms
        self.obNameList = []  #object reference names
        self.morNameList = []  #morphism reference names

        #Hom Functor starts out as empty list
        #List HOM[i][j] = HOM(i,j)
        self.Hom = []




    class object:
        def __init__(self,name):
            self.name = name
            #reference number in obList
            self.ref = None
            #initialization for golog location
            #store graphics information (if any)
            #In the future location should be stored in here
            self.graphics = None

            #add Hom Objects



    class morphism:
        def __init__(self,name,dom,codom):
            #String name
            self.name = name
            #Object dom
            self.dom = dom
            #Object codom
            self.codom = codom
            self.pr = str(self.name) + ": " + str(self.dom.name) +" -> "+str(self.codom.name)
            #Path from domas to codom in golog
            self.graphics = None
            #self.path = [self.dom.location,self.codom.location]


    #chain c = (f_n,...,f_1) such that dom(f_i) = codom(f_{i-1})
    class chain: #f = (f_n)
        def __init__(self,f):
            self.morList = f
            self.initial = f[-1].dom #initial object is domain of first morphism
            self.final = f[0].codom #final object is codomain of last morphism
            self.display = "[ "
            for g in f: self.display = self.display + g.name + " , "
            self.display = self.display[:-2] + "]"

    class commDiag:
        def __init__(self,chains):
            self.chainList = chains




#Adding Functions

    #get set of morphisms from dom to codom
    def hom(self,dom,codom):
        return self.Hom[self.obList.index(dom)][self.obList.index(codom)]

    #add commutative diagrams by
    def addCommDiag(self, *chains):

        #check if the initial and final objects are all the same
        initial = chains[0].initial
        final = chains[0].final
        for ch in chains:
            assert ch.initial == initial, "initial objects are fucked"
            assert ch.final == final, "final objects are fucked"

        #pass chains into a commDiag
        return self.commDiag(chains)


    #Manually add Chains by lists of string names of Morphisms
    #morphisms are listed like (f_n,....,f_1)
    def addChain(self,*fnamed):
        #get actual morphisms
        f = [self.getMorphism(g) for g in fnamed]

        #check if morphisms can compose
        index = range(len(f)-1) #only need to check up to final morphism
        for i in index:
            assert f[i].dom == f[i+1].codom, "codom(f_"+str(i)+") != dom(f_" + str(i+1)+")"

        return self.chain(f)




    #Manually add Objects by name
    def addObject(self,name,graphics=None):

        ################## CREATE OBJECT #############
        #Check if object is already in category
        assert name not in self.obNameList, str(name) + " already in" + str(self.name)
        newOb = self.object(name)
        newOb.graphics = graphics
        newOb.ref = len(self.obList) #set object's reference number
        self.obList.append(newOb)#Add object to object list
        self.obNameList.append(name)#add object name to object name list (for searching)



        ################ HOM OPERATIONS #################
        #Add to Global HOM list HOM[i][j] = HOM(i,j)
        #For all A in obList set HOM(A,newOb) = []
        for initVar in self.Hom:
            initVar.append([])


        #For all A in obList set HOM(newOb,A) = []
        #I.e. appending a list of empty lists, one for each object in obList
        newObHomList = []
        for initVar in self.obList:
            newObHomList.append([])
        self.Hom.append(newObHomList)

        #Add identity morphism
        self.addMorphism("Id_"+ str(newOb.name),newOb,newOb)


        return newOb

    #get object by reference name
    def getObject(self,ref):
        if ref in range(len(self.obList)):
            return self.obList[ref]

    def getAttachedMors(self,ob):
        attachedMors = []
        for X in self.obList:

            for f in self.hom(ob,X): attachedMors.append(f) #add morphisms out of ob into X

            if X!=ob: #Make sure we don't add endomorphisms of A twice
                for f in self.hom(X,ob): attachedMors.append(f) #add morphisms into ob out of X

        return attachedMors

    #Manually add Morphisms by string names of domain and codomain
    def addMorphism(self,name,dom,codom,graphics=None):
        #Check if morphism is already in Hom(dom,Codom)
        assert name not in [f.name for f in self.hom(dom,codom)], ("Morphism " + str(name) + " already in hom(" + str(dom.name) + " , " + str(codom.name) + ")" )
        #Check if dom and codom are actual objects in the category
        assert dom in self.obList, ("Object " + str(dom) + " not in " + "Category " +  str(self.name))
        assert codom in self.obList, ("Object " + str(codom) + " not in " + "Category " +  str(self.name))


        #get actual dom and codom objects
        domInd = self.obList.index(dom)
        codomInd = self.obList.index(codom)

        #add actual morphism and name reference to global morList and Hom list
        mor = self.morphism(name,dom,codom)
        self.morList.append(mor)
        self.morNameList.append(name)
        self.hom(dom,codom).append(mor)


        return

    #get morphism by reference name, dom and codom names
    def getMorphism(self,name):
        if name in self.morNameList:
            return self.morList[self.morNameList.index(name)]

################################
#Display functions



#Organizes category based on its objects,
#morphisms, and commDiags

#Future: Organize based on commutative diagrams
def organizeCat(Cat):
    obList = Cat.obList
    morList = Cat.morList
    i = 0.
    for ob in obList:
        ob.location = (i,i**2)
        i = i+1.

    for f in morList:
        f.path = [f.dom.location,f.codom.location]


    # organizing function Org:(obList,morList,commList) --> (R^2)^|Ob|


    #locList = Org(Cat)
    #for i in len(obList): obList[i].location = locList[i]



    #



def displayCat(Cat):
    fig, ax = plt.subplots()
    chains = comm.chainList
    for A in oblist:
        Apatch = patches.Circle(A.location,radius=.1)
        ax.add_patch(Apatch)
    for f in morList:
        c = [Path.MOVETO,Path.LINETO]
        fpath = Path(f.path,c)
        fpatch = patches.PathPatch(fpath)
        ax.add_patch(fpatch)
    ax.set_xlim(-1,10)
    ax.set_ylim(-1,10)
    plt.show()

#display objects and morphisms based on locations
def displayDiag(comm):
    #initialize window
    fig, ax = plt.subplots()
    chains = comm.chainList



    #Create paths
    for ch in chains:
        mors = ch.morList
        for f in mors:
            #Create Objects
            domplt = patches.Circle(f.dom.location,radius=.1)
            codomplt = patches.Circle(f.codom.location,radius=.1)
            ax.add_patch(domplt)
            ax.add_patch(codomplt)



            #Create Paths
            v = f.path      #f.path = (dom(f),codom(f))
            c = [Path.MOVETO,Path.LINETO]
            path = Path(v,c)
            patch = patches.PathPatch(path)
            ax.add_patch(patch)
    ax.set_xlim(-1,10)
    ax.set_ylim(-1,10)
    plt.show()


########
#Left off state
#everything passes through and the order problem with creating chains seems to
#still be an issue
#
# #
# C = category("C")
# A = C.addObject("A")
# B = C.addObject("B")
# C.addMorphism("f",B,A)
# C.addMorphism("g",A,B)
# print([f.pr for f in C.getAttachedMors(A)])
# print(homPrint(CB.Hom))
