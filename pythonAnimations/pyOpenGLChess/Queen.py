# Queen.py

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *

from defines import *
from objloader import *
from openGLFunctions import set_color
import Piece


# noinspection PyPep8Naming
class Queen(Piece.Piece):
    def __init__(self, c, x, y, useobj):
        if c == objWhite:
            Piece.Piece.__init__(self, queen, white, x, y)
        else:
            Piece.Piece.__init__(self, queen, c, x, y)
        self.height1 = 4.7
        self.radius1 = 0.5
        self.headRadius = 1.9
        self.crownDepth = (3/4)*self.headRadius
        self.crownHeight = 1.6
        self.crownRadius = 1.9
        self.objFilePath = "Queen.obj"
        self.useObj = useobj
        self.obj = None

        if self.useObj and c == objWhite:
            self.obj = OBJ(self.objFilePath, swapyz=True, listindex=drawWhiteQueenObj)

    def draw(self):
        if self.life == alive:
            glPushMatrix()
            self.translate()
            if self.factor == 1:
                if self.color == white and not self.useObj:
                    glCallList(drawWhiteQueen)
                elif self.color == black and not self.useObj:
                    glCallList(drawBlackQueen)
                elif self.color == white and self.useObj:
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


