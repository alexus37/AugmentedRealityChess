# Pawn.py (bauer)

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *

from defines import *
from objloader import *
from openGLFunctions import set_color
import Piece


# noinspection PyPep8Naming
class Pawn(Piece.Piece):
    def __init__(self, c, x, y, useobj):
        if c == objWhite:
            Piece.Piece.__init__(self, pawn, white, x, y)
        elif c == objBlack:
            Piece.Piece.__init__(self, pawn, black, x, y)
        else:
            Piece.Piece.__init__(self, pawn, c, x, y)

        self.height1 = 2.5
        self.height2 = 1.2
        self.height3 = 1.5
        self.radius1 = 0.7
        self.radius2 = 2.0
        self.radius3 = 0.35
        self.radius4 = 0.5

        self.useObj = useobj
        self.obj = None

        if self.useObj:
            if c == objWhite:
                self.objFilePath = "obj/PawnWhite.obj"
                self.obj = OBJ(self.objFilePath, swapyz=True, listindex=drawWhitePawnObj)
            else:
                self.objFilePath = "obj/PawnBlack.obj"
                self.obj = OBJ(self.objFilePath, swapyz=True, listindex=drawBlackPawnObj)

    def draw(self):
        if self.life == alive:
            glPushMatrix()
            self.translate()
            if self.factor == 1:
                if self.color == white and not self.useObj:
                    glCallList(drawWhitePawn)
                elif self.color == black and not self.useObj:
                    glCallList(drawBlackPawn)
                elif self.useObj:
                    glScalef(0.04, 0.04, 0.04)
                    set_color(self.color, normal)
                    glCallList(self.obj.gl_list)
                else:
                    self.drawMe(normal)
            glPopMatrix()

    def drawShadow(self):
        if self.life == alive:
            glPushMatrix()
            self.translate()
            self.drawMe(shadow)
            glPopMatrix()

    def drawMe(self, colorMode):
        if self.useObj == true:
            glScalef(0.04, 0.04, 0.04)
            set_color(self.color, colorMode)
            glCallList(self.obj.gl_list)
        else:
            self.drawFeet(colorMode)
            self.drawHat()
            # draw sphere on top:
            glColor3d(0, 0, 0)
            gfigur_6 = gluNewQuadric()
            glTranslated(0, 0, (self.height3 + (4 * self.radius4 / 5)) * standardFactor * self.factor)
            gluSphere(gfigur_6, self.radius4 * standardFactor * self.factor, 4, 4)
            gluDeleteQuadric(gfigur_6)

