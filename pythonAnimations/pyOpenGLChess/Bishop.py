# Bishop.py (Laeufer)

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *

from defines import *
from openGLFunctions import set_color
import Piece


class Bishop(Piece.Piece):
  def __init__(self, c, x, y ):
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

  def draw (self):
    if self.life == alive:
      glPushMatrix()
      self.translate ()
      if self.factor == 1:
        if self.color == white:
          glCallList (drawWhiteBishop)
        elif self.color == black:
          glCallList (drawBlackBishop)
      else:
        self.drawMe (normal)
      glPopMatrix()

  def drawShadow (self):
    if self.life == alive:
      glPushMatrix()
      self.translate ()
      self.drawMe (shadow)
      glPopMatrix()

  def drawMe (self, drawMode):        
    self.drawFeet (drawMode)
    self.drawHat ()
    if drawMode == normal:
      set_color (self.color, color2)
    elif drawMode == shadow:
      set_color (self.color, shadow)
    self.drawHat(2)

  def moves (self, array):
    move = []
    possible = [(-1,-1),(-1,1),(1,-1),(1,1)]

    for k in range(0,len(possible)):
      self.tryToAddMove (move, possible[k][0], possible[k][1], mainPiece, array)

    return move
