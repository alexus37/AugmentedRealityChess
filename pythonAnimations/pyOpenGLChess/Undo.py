# undo class

from defines import *
from Piece import emptyPiece
import Piece
import Pawn


class Undo:
  def __init__(self, game):
    self.undo_from = []
    self.undo_to = []
    self.undo_kill_figur = [] 
    self.option = []
    self.recentUndo = 0
    self.game = game
    
   
  def rememberUndo(self,akt_Figur, x, y, array, option=false):
    self.undo_from.append ([akt_Figur.pos[0], akt_Figur.pos[1]])
    self.undo_to.append ([x, y])
    self.undo_kill_figur.append (array[x, y])
    self.option.append (option)
    self.recentUndo = self.recentUndo + 1

  def undo(self, array):
    if self.recentUndo > 0:
      #undo:
      self.recentUndo = self.recentUndo - 1
      array[self.undo_to[self.recentUndo][0], self.undo_to[self.recentUndo][1]].pos = self.undo_from[self.recentUndo]
      array[self.undo_from[self.recentUndo][0], self.undo_from[self.recentUndo][1]].anim = array[self.undo_from[self.recentUndo][0], self.undo_from[self.recentUndo][1]].pos
      array[self.undo_from[self.recentUndo][0], self.undo_from[self.recentUndo][1]] = array[self.undo_to[self.recentUndo][0], self.undo_to[self.recentUndo][1]]

      if self.undo_kill_figur[self.recentUndo] != None and self.undo_kill_figur[self.recentUndo] != emptyPiece:
        self.undo_kill_figur[self.recentUndo].life = alive
        self.undo_kill_figur[self.recentUndo].factor = 1
        self.undo_kill_figur[self.recentUndo].pos = self.undo_to[self.recentUndo]
        self.undo_kill_figur[self.recentUndo].anim = self.undo_kill_figur[self.recentUndo].pos
        array[self.undo_to[self.recentUndo][0], self.undo_to[self.recentUndo][1]] = self.undo_kill_figur[self.recentUndo]
      else:
        array[self.undo_to[self.recentUndo][0], self.undo_to[self.recentUndo][1]] = emptyPiece
        
      if (self.option[self.recentUndo] == castlingOn):
        if (self.undo_to[self.recentUndo][0] < self.undo_from[self.recentUndo][0]): # was castling to left
          #undo for rook:
          array[4, self.undo_to[self.recentUndo][1]].pos = [1, self.undo_from[self.recentUndo][1]]
          array[4, self.undo_from[self.recentUndo][1]].anim = array [4, self.undo_from[self.recentUndo][1]].pos
          array [1, self.undo_to[self.recentUndo][1]] = array [4, self.undo_to[self.recentUndo][1]]
          array [4, self.undo_to[self.recentUndo][1]] = emptyPiece
          array [1, self.undo_to[self.recentUndo][1]].moved = false
          array[self.undo_from[self.recentUndo][0], self.undo_from[self.recentUndo][1]].moved = false
        else: # was castling to right
          #undo for rook:   
          array[6, self.undo_to[self.recentUndo][1]].pos = [8, self.undo_from[self.recentUndo][1]]
          array[6, self.undo_from[self.recentUndo][1]].anim = array[6, self.undo_from[self.recentUndo][1]].pos
          array [8, self.undo_to[self.recentUndo][1]] = array [6, self.undo_to[self.recentUndo][1]]
          array [6, self.undo_to[self.recentUndo][1]] = emptyPiece
          array [8, self.undo_to[self.recentUndo][1]].moved = false
          array[self.undo_from[self.recentUndo][0], self.undo_from[self.recentUndo][1]].moved = false
      elif (self.option[self.recentUndo] == changePawnOn):
        x = self.undo_from [self.recentUndo][0]
        y = self.undo_from [self.recentUndo][1]
        color = array[x, y].color
        # search for the correct pawn here:
        array[x, y].kill ()
        oldPawn = self.searchPawn (color, self.undo_to [self.recentUndo][0], self.undo_to [self.recentUndo][1])
        if (oldPawn != None):
          oldPawn.life = alive
          oldPawn.factor = 1
          array[x, y] = oldPawn
          oldPawn.pos = [x,y]
          oldPawn.anim = [x,y]
        else: # old pawn not found (should not occur)
          self.game.pawns.append (Pawn.Pawn (color, x, y))
          array[x, y] = self.game.pawns [(len (self.game.pawns) - 1)]
      elif (self.option[self.recentUndo] == kingFirstMove):
        array[self.undo_from[self.recentUndo][0], self.undo_from[self.recentUndo][1]].moved = false
      
      # remove last saved values
      self.undo_from.pop(self.recentUndo)
      self.undo_to.pop(self.recentUndo)
      self.undo_kill_figur.pop(self.recentUndo)
      self.option.pop (self.recentUndo)
      return array
    else:
      return None

      
  def searchPawn (self, color, x, y):
    for i in range (0, len (self.game.pawns)):
      if ((self.game.pawns [i].pos[0] == x) and (self.game.pawns [i].pos[1] == y) and (self.game.pawns [i].color == color)):
        return self.game.pawns [i]
    return None
  
  
  