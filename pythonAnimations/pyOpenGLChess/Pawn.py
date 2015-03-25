# Pawn.py (bauer)

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *

from defines import *
from openGLFunctions import set_color
import Piece


class Pawn(Piece.Piece):
  def __init__(self, c, x, y):
    Piece.Piece.__init__(self, pawn, c, x, y)
    self.height1 = 2.5
    self.height2 = 1.2
    self.height3 = 1.5
    self.radius1 = 0.7
    self.radius2 = 2.0
    self.radius3 = 0.35
    self.radius4 = 0.5

  def draw (self):
    if self.life == alive:
      glPushMatrix()
      self.translate ()
      if self.factor == 1:
        if self.color == white:
          glCallList (drawWhitePawn)
        elif self.color == black:
          glCallList (drawBlackPawn)
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
    self.drawHat ()
    # draw sphere on top:
    glColor3d(0,0,0)
    gfigur_6 = gluNewQuadric()
    glTranslated(0, 0, (self.height3+(4*self.radius4/5))*standardFactor*self.factor)
    gluSphere (gfigur_6, self.radius4*standardFactor*self.factor, 4, 4)
    gluDeleteQuadric (gfigur_6)
    

  def moves (self, array):
    move = []
    if self.color == white:
      if (self.tryToAddMove (move, 0, 1, pawnForward, array) == true) and (self.pos[1] == 2):
        self.tryToAddMove (move, 0, 2, pawnForward, array)
      self.tryToAddMove (move, -1, 1, pawnDefeat, array)
      self.tryToAddMove (move,  1, 1, pawnDefeat, array)
    elif self.color == black:
      if (self.tryToAddMove (move, 0, -1, pawnForward, array) == true) and (self.pos[1] == 7):
        self.tryToAddMove (move, 0, -2, pawnForward, array)
      self.tryToAddMove (move, -1, -1, pawnDefeat, array)
      self.tryToAddMove (move,  1, -1, pawnDefeat, array)
    return move

