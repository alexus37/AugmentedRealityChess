# Rook.py (Turm)

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *

from defines import *
from openGLFunctions import set_color
import Piece


class Rook(Piece.Piece):
  def __init__(self, c, x, y ):
    Piece.Piece.__init__(self, rook, c, x, y)
    self.height1 = 2.9
    self.radius1 = 0.65
    self.headRadius = 1.8
    self.crownDepth = (1/9)*self.headRadius
    self.crownHeight = 1.7
    self.crownRadius = 1.85

  def draw (self):
    if self.life == alive:
      glPushMatrix()
      self.translate ()
      if self.factor == 1:
        if self.color == white:
          glCallList (drawWhiteRook)
        elif self.color == black:
          glCallList (drawBlackRook)
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
    possible = [(-1,0),(0,1),(1,0),(0,-1)]
    for k in range(0,len(possible)):
      self.tryToAddMove (move, possible[k][0], possible[k][1], mainPiece, array)
    return move

