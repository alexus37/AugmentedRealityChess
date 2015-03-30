# Bishop.py (Laeufer)

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *

from defines import *
from objloader import *
from openGLFunctions import set_color
import Piece


# noinspection PyPep8Naming
class Bishop(Piece.Piece):
    def __init__(self, c, x, y, useobj):
        if c == objWhite:
            Piece.Piece.__init__(self, bishop, white, x, y)
        elif c == objBlack:
            Piece.Piece.__init__(self, bishop, black, x, y)
        else:
            Piece.Piece.__init__(self, bishop, c, x, y)

        self.height1 = 3.1
        self.height2 = 1.4
        self.height3 = 1.6
        self.radius4 = 1.1
        self.radius1 = 0.6
        self.radius2 = 2.0
        self.radius3 = 0.5
        self.height4 = 0.6
        self.height5 = 1.6

        self.objFilePath = "obj/Bishop.obj"
        self.useObj = useobj
        self.obj = None

        if self.useObj :
            if c == objWhite:
                self.obj = OBJ(self.objFilePath, swapyz=True, listindex=drawWhiteBishopObj)
            else:
                self.obj = OBJ(self.objFilePath, swapyz=True, listindex=drawBlackBishopObj)

    def draw(self):
        if self.life == alive:
            glPushMatrix()
            self.translate()
            if self.factor == 1:
                if self.color == white and not self.useObj:
                    glCallList(drawWhiteBishop)
                elif self.color == black and not self.useObj:
                    glCallList(drawBlackBishop)
                elif self.useObj:
                    glScalef(0.04, 0.04, 0.04)
                    set_color(self.color, normal)
                    glCallList(self.obj.gl_list)
                else:
                    self.drawMe(normal)
            else:
                self.drawMe(normal)
            glPopMatrix()

    def drawShadow(self):
        if self.life == alive:
            glPushMatrix()
            self.translate()
            self.drawMe(shadow)
            glPopMatrix()

    def drawMe(self, drawMode):
        if self.useObj == true:
            glScalef(0.04, 0.04, 0.04)
            set_color(self.color, drawMode)
            glCallList(self.obj.gl_list)
        else:
            self.drawFeet(drawMode)
            self.drawHat()
            if drawMode == normal:
                set_color(self.color, color2)
            elif drawMode == shadow:
                set_color(self.color, shadow)
            self.drawHat(2)

