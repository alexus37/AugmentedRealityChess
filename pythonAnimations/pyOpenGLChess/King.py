# King.py

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *

from defines import *
from openGLFunctions import set_color
import Piece


class King(Piece.Piece):
  def __init__(self, c, x, y ):
    Piece.Piece.__init__(self, king, c, x, y)
    self.height1 = 4.3
    self.radius1 = 0.55
    self.headRadius = 1.9
    self.crownDepth = (3/4)*self.headRadius
    self.crownHeight = 3.2
    self.crownRadius = 1.9
    self.eyes = true

  def draw (self):
    if self.life == alive:
      glPushMatrix()
      self.translate ()
      if self.factor == 1:
        if self.color == white:
          glCallList (drawWhiteKing)
        elif self.color == black:
          glCallList (drawBlackKing)
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

    for k in range(0,len(possible)):
      self.tryToAddMove (move, possible[k][0], possible[k][1], kingAndKnight, array)

    return move


  def safeMoves (self, array):
    move = []
    possible = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (-1,1), (1,-1)]
    for k in range(0,len(possible)):
      self.tryToAddMove (move, possible[k][0], possible[k][1], kingAndKnightSafe, array)
      
    # castling:
    possible = [(1,0), (-1,0)];
    for k in range (0,len(possible)):
      self.tryToAddMove (move, possible[k][0], possible[k][1], castlingSafe, array)

    return move

