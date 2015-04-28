# Rook.py (Turm)

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *

from defines import *
from objloader import *
from openGLFunctions import set_color
import Piece


# noinspection PyPep8Naming
class Rook(Piece.Piece):
    def __init__(self, c, x, y, useobj):

        if c == objWhite:
            Piece.Piece.__init__(self, rook, white, x, y)
        elif c == objBlack:
            Piece.Piece.__init__(self, rook, black, x, y)
        else:
            Piece.Piece.__init__(self, rook, c, x, y)

        self.height1 = 2.9
        self.radius1 = 0.65
        self.headRadius = 1.8
        self.crownDepth = (1 / 9) * self.headRadius
        self.crownHeight = 1.7
        self.crownRadius = 1.85

        self.useObj = useobj
        self.obj = None

        if self.useObj:
            if c == objWhite:
                self.objFilePath = "obj/RookWhite.obj"
                self.obj = OBJ(self.objFilePath, swapyz=True, listindex=drawWhiteRookObj)
            else:
                self.objFilePath = "obj/RookBlack.obj"
                self.obj = OBJ(self.objFilePath, swapyz=True, listindex=drawBlackRookObj)

    def draw(self):
        if self.life == alive:
            glPushMatrix()
            self.translate()
            if self.factor == 1:
                if self.color == white and not self.useObj:
                    glCallList(drawWhiteRook)
                elif self.color == black and not self.useObj:
                    glCallList(drawBlackRook)
                elif self.useObj:
                    glScalef(figureScale, figureScale, figureScale)
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
            glScalef(figureScale, figureScale, figureScale)
            set_color(self.color, colorMode)
            glCallList(self.obj.gl_list)
        else:
            self.drawFeet(colorMode)
            self.drawHead(colorMode)



