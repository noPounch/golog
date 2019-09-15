from direct.showbase.ShowBase import ShowBase
from math import sin, cos
from panda3d.core import Point3, ButtonHandle, ModifierButtons
import sys, os
class runner(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()

        # need to migrate into gologToWindow
        base.accept("f5",sys.exit)
        base.accept("f6",sys.exit)
        base.accept('shift-mouse1',print, extraArgs = ['hello'])
        bt = self.buttonThrowers[0].node()
        newMB = ModifierButtons()
        newguy = ButtonHandle('shift')
        newMB.addButton(newguy)
        # bt.setModifierButtons(bt.getModifierButtons().addButton(newguy))
        # print(bt.getModifierButtons().getButton(0).getName())
        # print(bt.getModifierButtons().getButton(0).getAlias())
        print(newMB)

        # print(newguy.hasAsciiEquivalent())





r = runner()
r.run()
