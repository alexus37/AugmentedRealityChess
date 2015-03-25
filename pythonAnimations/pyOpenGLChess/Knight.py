# Knight.py (Springer / Pferd)

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *

from defines import *
from openGLFunctions import set_color
import Piece


class Knight(Piece.Piece):
  def __init__(self, c, x, y ):
    Piece.Piece.__init__(self, knight, c, x, y)
    self.height1 = 3.6
    self.radius1 = 0.5
    self.radius = 0.55*standardFactor

  def draw (self):
    if self.life == alive:
      glPushMatrix()
      self.translate ()
      if self.factor == 1:
        if self.color == black:
          glCallList (drawBlackKnight)
        elif self.color == white:
          glCallList (drawWhiteKnight)
      else:
        self.drawMe (normal)
      glPopMatrix()
  
  def drawShadow (self):
    if self.life == alive:
      glPushMatrix()
      self.translate ()
      self.drawMe (shadow)
      glPopMatrix()

  def drawMe (self, colorMode):
    self.drawFeet (colorMode)
    #glColor3f (0,0,0)
    set_color (self.color, colorMode)
    glTranslated(0,0,3.6*standardFactor*self.factor)

    #connection:
    glBegin(GL_QUAD_STRIP)
    glNormal3d(0,1,0)
    glVertex3d(-self.radius*self.factor,1.9*standardFactor*self.factor,0.4*standardFactor*self.factor)
    glNormal3d(0,1,0)
    glVertex3d(self.radius*self.factor,1.9*standardFactor*self.factor,0.4*standardFactor*self.factor)
    #glNormal3d(1,0,0)
    glVertex3d(-self.radius*self.factor,0.35*standardFactor*self.factor,1.7*standardFactor*self.factor)
    #glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,0.35*standardFactor*self.factor,1.7*standardFactor*self.factor)
    glNormal3d(0,-1,0)
    glVertex3d(-self.radius*self.factor,-1.9*standardFactor*self.factor,0.4*standardFactor*self.factor)
    glNormal3d(0,-1,0)
    glVertex3d(self.radius*self.factor,-1.9*standardFactor*self.factor,0.4*standardFactor*self.factor)
    glNormal3d(0,-0.5,-0.5)
    glVertex3d(-self.radius*self.factor,-0.5*standardFactor*self.factor,0)
    glNormal3d(0,-0.5,-0.5)
    glVertex3d(self.radius*self.factor,-0.5*standardFactor*self.factor,0)
    glNormal3d(0,0.5,-0.5)
    glVertex3d(-self.radius*self.factor,0.5*standardFactor*self.factor,0)
    glNormal3d(0,0.5,-0.5)
    glVertex3d(self.radius*self.factor,0.5*standardFactor*self.factor,0)
    glEnd()
    #'right' bottom polygon
    glBegin(GL_POLYGON)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,0.35*standardFactor*self.factor,1.7*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,1.9*standardFactor*self.factor,0.4*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,0.5*standardFactor*self.factor,0)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,-0.5*standardFactor*self.factor,0)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,-1.9*standardFactor*self.factor,0.4*standardFactor*self.factor)
    glEnd()
    #'left' bottom polygon
    glBegin(GL_POLYGON)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,-0.5*standardFactor*self.factor,0)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,0.5*standardFactor*self.factor,0)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,1.9*standardFactor*self.factor,0.4*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,0.35*standardFactor*self.factor,1.7*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,-1.9*standardFactor*self.factor,0.4*standardFactor*self.factor)
    glEnd()

    #top:
    glBegin(GL_POLYGON)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,-1.9*standardFactor*self.factor,0.4*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,0.35*standardFactor*self.factor,1.7*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,0.75*standardFactor*self.factor,3*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,0.85*standardFactor*self.factor,3.9*standardFactor*self.factor)
    #tail:
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,0.5*standardFactor*self.factor,3.9*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,0,3.8*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,-0.5*standardFactor*self.factor,3.65*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,-0.8*standardFactor*self.factor,3.4*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,-standardFactor*self.factor,3.15*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,-1.25*standardFactor*self.factor,2.8*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,-1.5*standardFactor*self.factor,2.3*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,-1.7*standardFactor*self.factor,1.8*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,-1.83*standardFactor*self.factor,1.2*standardFactor*self.factor)
    glEnd()

    glBegin(GL_POLYGON)
    #tail:
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,-1.83*standardFactor*self.factor,1.2*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,-1.7*standardFactor*self.factor,1.8*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,-1.5*standardFactor*self.factor,2.3*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,-1.25*standardFactor*self.factor,2.8*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,-standardFactor*self.factor,3.15*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,-0.8*standardFactor*self.factor,3.4*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,-0.5*standardFactor*self.factor,3.65*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,0,3.8*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,0.5*standardFactor*self.factor,3.9*standardFactor*self.factor)

    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,0.85*standardFactor*self.factor,3.9*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,0.75*standardFactor*self.factor,3*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,0.35*standardFactor*self.factor,1.7*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,-1.9*standardFactor*self.factor,0.4*standardFactor*self.factor)

    glEnd()

    #connection:
    glBegin(GL_QUAD_STRIP)
    #glNormal3d()
    glVertex3d(-self.radius*self.factor,0.35*standardFactor*self.factor,1.7*standardFactor*self.factor)
    #glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,0.35*standardFactor*self.factor,1.7*standardFactor*self.factor)
    glNormal3d(0,0.4,-0.6)
    glVertex3d(-self.radius*self.factor,0.75*standardFactor*self.factor,3*standardFactor*self.factor)
    glNormal3d(0,0.4,-0.6)
    glVertex3d(self.radius*self.factor,0.75*standardFactor*self.factor,3*standardFactor*self.factor)
    glNormal3d(0,0.5,0.5)
    glVertex3d(-self.radius*self.factor,0.85*standardFactor*self.factor,3.9*standardFactor*self.factor)
    glNormal3d(0,0.5,0.5)
    glVertex3d(self.radius*self.factor,0.85*standardFactor*self.factor,3.9*standardFactor*self.factor)

    #tail:
    glNormal3d(0,-0.1,0.9)
    glVertex3d(-self.radius*self.factor,0.5*standardFactor*self.factor,3.9*standardFactor*self.factor)
    glNormal3d(0,-0.1,0.9)
    glVertex3d(self.radius*self.factor,0.5*standardFactor*self.factor,3.9*standardFactor*self.factor)
    glNormal3d(0,-0.3,0.7)
    glVertex3d(-self.radius*self.factor,0,3.8*standardFactor*self.factor)
    glNormal3d(0,-0.3,0.7)
    glVertex3d(self.radius*self.factor,0,3.8*standardFactor*self.factor)
    glNormal3d(0,-0.2,0.8)
    glVertex3d(-self.radius*self.factor,-0.5*standardFactor*self.factor,3.65*standardFactor*self.factor)
    glNormal3d(0,-0.2,0.8)
    glVertex3d(self.radius*self.factor,-0.5*standardFactor*self.factor,3.65*standardFactor*self.factor)
    glNormal3d(0,-0.35,0.7)
    glVertex3d(-self.radius*self.factor,-0.8*standardFactor*self.factor,3.4*standardFactor*self.factor)
    glNormal3d(0,-0.35,0.7)
    glVertex3d(self.radius*self.factor,-0.8*standardFactor*self.factor,3.4*standardFactor*self.factor)
    glNormal3d(0,-0.45,0.5)
    glVertex3d(-self.radius*self.factor,-standardFactor*self.factor,3.15*standardFactor*self.factor)
    glNormal3d(0,-0.45,0.5)
    glVertex3d(self.radius*self.factor,-standardFactor*self.factor,3.15*standardFactor*self.factor)
    glNormal3d(0,-0.55,0.4)
    glVertex3d(-self.radius*self.factor,-1.25*standardFactor*self.factor,2.8*standardFactor*self.factor)
    glNormal3d(0,-0.55,0.4)
    glVertex3d(self.radius*self.factor,-1.25*standardFactor*self.factor,2.8*standardFactor*self.factor)
    glNormal3d(0,-0.7,0.3)
    glVertex3d(-self.radius*self.factor,-1.5*standardFactor*self.factor,2.3*standardFactor*self.factor)
    glNormal3d(0,-0.7,0.3)
    glVertex3d(self.radius*self.factor,-1.5*standardFactor*self.factor,2.3*standardFactor*self.factor)
    glNormal3d(0,-0.9,0.1)
    glVertex3d(-self.radius*self.factor,-1.7*standardFactor*self.factor,1.8*standardFactor*self.factor)
    glNormal3d(0,-0.9,0.1)
    glVertex3d(self.radius*self.factor,-1.7*standardFactor*self.factor,1.8*standardFactor*self.factor)
    glNormal3d(0,-1,0)
    glVertex3d(-self.radius*self.factor,-1.83*standardFactor*self.factor,1.2*standardFactor*self.factor)
    glNormal3d(0,-1,0)
    glVertex3d(self.radius*self.factor,-1.83*standardFactor*self.factor,1.2*standardFactor*self.factor)

    glNormal3d(0,-1,0)
    glVertex3d(-self.radius*self.factor,-1.9*standardFactor*self.factor,0.4*standardFactor*self.factor)
    glNormal3d(0,-1,0)
    glVertex3d(self.radius*self.factor,-1.9*standardFactor*self.factor,0.4*standardFactor*self.factor)
    glEnd()

    #nose:
    glBegin(GL_POLYGON)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,0.35*standardFactor*self.factor,1.7*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,1.55*standardFactor*self.factor,1.45*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,1.5*standardFactor*self.factor,2.55*standardFactor*self.factor)
    glNormal3d(-1,0,0)
    glVertex3d(-self.radius*self.factor,0.75*standardFactor*self.factor,3*standardFactor*self.factor)
    glEnd()
    glBegin(GL_POLYGON)
    glNormal3d(0,0.2,0.7)
    glVertex3d(-self.radius*self.factor,0.75*standardFactor*self.factor,3*standardFactor*self.factor)
    glNormal3d(0,0.2,0.7)
    glVertex3d(-self.radius*self.factor,1.5*standardFactor*self.factor,2.55*standardFactor*self.factor)
    glNormal3d(0,0.2,0.7)
    glVertex3d(self.radius*self.factor,1.5*standardFactor*self.factor,2.55*standardFactor*self.factor)
    glNormal3d(0,0.2,0.7)
    glVertex3d(self.radius*self.factor,0.75*standardFactor*self.factor,3*standardFactor*self.factor)
    glEnd()
    glBegin(GL_POLYGON)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,0.75*standardFactor*self.factor,3*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,1.5*standardFactor*self.factor,2.55*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,1.55*standardFactor*self.factor,1.45*standardFactor*self.factor)
    glNormal3d(1,0,0)
    glVertex3d(self.radius*self.factor,0.35*standardFactor*self.factor,1.7*standardFactor*self.factor)
    glEnd()
    glBegin(GL_POLYGON)
    glNormal3d(0,-0.1,-0.8)
    glVertex3d(self.radius*self.factor,0.35*standardFactor*self.factor,1.7*standardFactor*self.factor)
    glNormal3d(0,-0.1,-0.8)
    glVertex3d(self.radius*self.factor,1.55*standardFactor*self.factor,1.45*standardFactor*self.factor)
    glNormal3d(0,-0.1,-0.8)
    glVertex3d(-self.radius*self.factor,1.55*standardFactor*self.factor,1.45*standardFactor*self.factor)
    glNormal3d(0,-0.1,-0.8)
    glVertex3d(-self.radius*self.factor,0.35*standardFactor*self.factor,1.7*standardFactor*self.factor)
    glEnd()
    #nose front:
    glBegin(GL_POLYGON)
    glNormal3d(0,1,0.1)
    glVertex3d(-self.radius*self.factor,1.55*standardFactor*self.factor,1.45*standardFactor*self.factor)
    glNormal3d(0,1,0.1)
    glVertex3d(-self.radius*self.factor,1.5*standardFactor*self.factor,2.55*standardFactor*self.factor)
    glNormal3d(0,1,0.1)
    glVertex3d(self.radius*self.factor,1.5*standardFactor*self.factor,2.55*standardFactor*self.factor)
    glNormal3d(0,1,0.1)
    glVertex3d(self.radius*self.factor,1.55*standardFactor*self.factor,1.45*standardFactor*self.factor)
    glEnd()




  def moves (self, array):
    move = []
    possible = [(1,2),(-1,-2),(-1,2),(1,-2),(2,1),(-2,-1),(-2,1),(2,-1)]
    for k in range(0,len(possible)):
      self.tryToAddMove (move, possible[k][0], possible[k][1], kingAndKnight, array)

    return move

