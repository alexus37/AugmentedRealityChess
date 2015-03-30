# King.py

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *

from defines import *
from objloader import *
from openGLFunctions import set_color
import Piece


# noinspection PyPep8Naming
class King(Piece.Piece):
    def __init__(self, c, x, y, useobj):
        if c == objWhite:
            Piece.Piece.__init__(self, king, white, x, y)
        elif c == objBlack:
            Piece.Piece.__init__(self, king, black, x, y)
        else:
            Piece.Piece.__init__(self, king, c, x, y)

        self.height1 = 4.3
        self.radius1 = 0.55
        self.headRadius = 1.9
        self.crownDepth = (3 / 4) * self.headRadius
        self.crownHeight = 3.2
        self.crownRadius = 1.9
        self.eyes = true

        self.objFilePath = "obj/King.obj"
        self.useObj = useobj
        self.obj = None

        if self.useObj:
            if c == objWhite:
                self.obj = OBJ(self.objFilePath, swapyz=True, listindex=drawWhiteKingObj)
            else:
                self.obj = OBJ(self.objFilePath, swapyz=True, listindex=drawBlackKingObj)

    def draw(self):
        if self.life == alive:
            glPushMatrix()
            self.translate()
            if self.factor == 1:
                if self.color == white and not self.useObj:
                    glCallList(drawWhiteKing)
                elif self.color == black and not self.useObj:
                    glCallList(drawBlackKing)
                elif  self.useObj:
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
            self.drawHead(colorMode)

