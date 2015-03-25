# Queen.py

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *

from defines import *
from openGLFunctions import set_color
import Piece


class Queen(Piece.Piece):
  def __init__(self, c, x, y ):
    Piece.Piece.__init__(self, queen, c, x, y)
    self.height1 = 4.7
    self.radius1 = 0.5
    self.headRadius = 1.9
    self.crownDepth = (3/4)*self.headRadius
    self.crownHeight = 1.6
    self.crownRadius = 1.9

  def draw (self):
    if self.life == alive:
      glPushMatrix()
      self.translate ()
      if self.factor == 1:
        if self.color == white:
          glCallList (drawWhiteQueen)
        elif self.color == black:
          glCallList (drawBlackQueen)
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
    self.drawHead (colorMode)

  def moves (self, array):
    move = []
    possible = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (-1,1), (1,-1)]
    for k in range(0, len(possible)):
      self.tryToAddMove (move, possible[k][0], possible[k][1], mainPiece, array)
    return move

