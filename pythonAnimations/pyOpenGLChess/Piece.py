# Piece.py

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from defines import *
from openGLFunctions import set_color


class Piece:
  def __init__(self, t, c, x, y):
    self.color = c
    self.type = t
    self.life = alive
    self.pos = [x,y]
    self.headRadius = 0
    self.radius1 = 0
    self.height1 = 0
    self.radius2 = 0
    self.height2 = 0
    self.radius3 = 0
    self.radius4 = 0
    self.eyes = false
    self.animate = 0
    self.anim = [0,0]
    self.factor = 1
    self.moved = false

  def setxpos(self, x):
    self.pos[0] = x

  def setypos(self, y):
    self.pos[1] = y

  def colorOfEnemy(self):
    if self.color == white:
      return black
    elif self.color == black:
      return white
    
  def threat (self, x, y, array):
    # check for dangerous knight:
    dangerous = [[x+1, y+2], [x+1, y-2], [x-1, y+2], [x-1, y-2], [x+2, y+1], [x+2, y-1], [x-2, y+1], [x-2, y-1]]
    for i in range (0, len(dangerous)):
      if (self.onTheBoard (dangerous [i][0], dangerous [i][1])):
        if (array[dangerous [i][0], dangerous [i][1]].type == knight):
          if (array[dangerous [i][0], dangerous [i][1]].color == self.colorOfEnemy()):
            return threatened
    
            
    dangerous = []
    
    add = 1
    while (self.onTheBoard (x+add, y) and array [x+add, y].color == -1):
      add = add + 1
    if array[x+add, y].color == self.colorOfEnemy():
      if array[x+add, y].type == rook:
        return threatened
      elif array[x+add, y].type == queen:
        return threatened
      elif array[x+add, y].type == king:
        if add == 1:
          return threatened
    
    add = -1
    while (self.onTheBoard (x+add, y) and array [x+add, y].color == -1):
      add = add - 1
    if array[x+add, y].color == self.colorOfEnemy():
      if array[x+add, y].type == rook:
        return threatened
      elif array[x+add, y].type == queen:
        return threatened
      elif array[x+add, y].type == king:
        if add == -1:
          return threatened
    
    add = 1
    while (self.onTheBoard (x, y+add) and array [x, y+add].color == -1):
      add = add + 1
    if array[x, y+add].color == self.colorOfEnemy():
      if array[x, y+add].type == rook:
        return threatened
      elif array[x, y+add].type == queen:
        return threatened
      elif array[x, y+add].type == king:
        if add == 1:
          return threatened
    
    add = -1
    while (self.onTheBoard (x, y+add) and array [x, y+add].color == -1):
      add = add - 1
    if array[x, y+add].color == self.colorOfEnemy():
      if array[x, y+add].type == rook:
        return threatened
      elif array[x, y+add].type == queen:
        return threatened
      elif array[x, y+add].type == king:
        if add == -1:
          return threatened
    
    
    xadd = 1
    yadd = 1
    while (self.onTheBoard (x+xadd, y+yadd) and array [x+xadd, y+yadd].color == -1):
      xadd = xadd + 1
      yadd = yadd + 1
    if array[x+xadd, y+yadd].color == self.colorOfEnemy():
      if array[x+xadd, y+yadd].type == bishop:
        return threatened
      elif array[x+xadd, y+yadd].type == queen:
        return threatened
      elif array[x+xadd, y+yadd].type == king:
        if xadd == 1 and yadd == 1:
          return threatened
      elif array[x+xadd, y+yadd].type == pawn:
        if self.colorOfEnemy() == black:
          if (xadd == 1 and yadd == 1):
            return threatened
        # !! add special pawn move here
    
    xadd = -1
    yadd = 1
    while (self.onTheBoard (x+xadd, y+yadd) and array [x+xadd, y+yadd].color == -1):
      xadd = xadd - 1
      yadd = yadd + 1
    if array[x+xadd, y+yadd].color == self.colorOfEnemy():
      if array[x+xadd, y+yadd].type == bishop:
        return threatened
      elif array[x+xadd, y+yadd].type == queen:
        return threatened
      elif array[x+xadd, y+yadd].type == king:
        if xadd == -1 and yadd == 1:
          return threatened
      elif array[x+xadd, y+yadd].type == pawn:
        if self.colorOfEnemy() == black:
          if xadd == -1 and yadd == 1:
            return threatened
        # !! add special pawn move here
    
    xadd = 1
    yadd = -1
    while (self.onTheBoard (x+xadd, y+yadd) and array [x+xadd, y+yadd].color == -1):
      xadd = xadd + 1
      yadd = yadd - 1
    if array[x+xadd, y+yadd].color == self.colorOfEnemy():
      if array[x+xadd, y+yadd].type == bishop:
        return threatened
      elif array[x+xadd, y+yadd].type == queen:
        return threatened
      elif array[x+xadd, y+yadd].type == king:
        if xadd == 1 and yadd == -1:
          return threatened
      elif array[x+xadd, y+yadd].type == pawn:
        if self.colorOfEnemy() == white:
          if xadd == 1 and yadd == -1:
            return threatened
        # !! add special pawn move here
    
    xadd = -1
    yadd = -1
    while (self.onTheBoard (x+xadd, y+yadd) and array [x+xadd, y+yadd].color == -1):
      xadd = xadd - 1
      yadd = yadd - 1
    if array[x+xadd, y+yadd].color == self.colorOfEnemy():
      if array[x+xadd, y+yadd].type == bishop:
        return threatened
      elif array[x+xadd, y+yadd].type == queen:
        return threatened
      elif array[x+xadd, y+yadd].type == king:
        if xadd == -1 and yadd == -1:
          return threatened
      elif array[x+xadd, y+yadd].type == pawn:
        if self.colorOfEnemy() == white:
          if xadd == -1 and yadd == -1:
            return threatened
        # !! add special pawn move here
    
    return notThreatened


  def kill(self):
    self.life = dead
                

  def translate (self):
    if self.animate == 1:
      glTranslated((-4.5+self.anim[0])*blockSize,(-4.5+self.anim[1])*blockSize,0)
    else:
      glTranslated((-4.5+self.pos[0])*blockSize,(-4.5+self.pos[1])*blockSize,0)
                  
                                
  def onTheBoard(self, x, y):
    if ((x in range(1,9)) and (y in range(1,9))):
      return 1
    else:
      return 0
                        
                        
  def testForChess (self, array, xAdd, yAdd):
    #do:
    savedBlock = array[self.pos[0]+xAdd, self.pos[1]+yAdd]
    array[self.pos[0]+xAdd, self.pos[1]+yAdd] = array[self.pos[0], self.pos[1]]
    array[self.pos[0], self.pos[1]] = emptyPiece
    # search for king position:
    kingPosition = [-1, -1]
    for i in range (1, 9):
      for j in range (1, 9):
        if (array[i,j].type == king):
          if (array[i,j].color == self.color):
            kingPosition = [i,j]
            break
    if (self.threat (kingPosition[0], kingPosition[1], array) == notThreatened):
      #undo:
      array[self.pos[0], self.pos[1]] = array[self.pos[0]+xAdd, self.pos[1]+yAdd]
      array[self.pos[0]+xAdd, self.pos[1]+yAdd] = savedBlock
      return true
    array[self.pos[0], self.pos[1]] = array[self.pos[0]+xAdd, self.pos[1]+yAdd]
    array[self.pos[0]+xAdd, self.pos[1]+yAdd] = savedBlock
    return false
          
                        
  def tryToAddMove(self, move, xAdd, yAdd, moveMode, array):
    if moveMode == pawnForward:
      if (emptyPiece == array[self.pos[0]+xAdd, self.pos[1]+yAdd]): 
        if (self.onTheBoard(self.pos[0]+xAdd, self.pos[1]+yAdd) == 1): # go forward
          if (self.testForChess (array, xAdd, yAdd)):
            move.append((self.pos[0]+xAdd, self.pos[1]+yAdd))
            return true
  
    elif moveMode == pawnDefeat:
      if(self.colorOfEnemy() == array[self.pos[0]+xAdd, self.pos[1]+yAdd].color and self.onTheBoard(self.pos[0]+xAdd, self.pos[1]+yAdd) == 1): # defeat a piece
        if (self.testForChess (array, xAdd, yAdd) == true):
          move.append((self.pos[0]+xAdd, self.pos[1]+yAdd))
          return true
  
    elif moveMode == mainPiece:
      i = 1
      if (-1 == array[self.pos[0]+i*xAdd,self.pos[1]+i*yAdd].color) and (self.onTheBoard(self.pos[0]+i*xAdd,self.pos[1]+i*yAdd) == 1):
        while (-1 == array[self.pos[0]+i*xAdd,self.pos[1]+i*yAdd].color) and (self.onTheBoard(self.pos[0]+i*xAdd,self.pos[1]+i*yAdd) == 1):
          if (self.testForChess (array, xAdd*i, yAdd*i) == true):
            move.append((self.pos[0]+i*xAdd,self.pos[1]+i*yAdd))
          i = i+1
      if(self.color != array[self.pos[0]+i*xAdd,self.pos[1]+i*yAdd].color) and (self.onTheBoard(self.pos[0]+i*xAdd,self.pos[1]+i*yAdd) == 1):
        if (self.testForChess (array, xAdd*i, yAdd*i) == true):
          move.append((self.pos[0]+i*xAdd,self.pos[1]+i*yAdd))
          return true
  
    elif moveMode == kingAndKnight:
      if self.onTheBoard(self.pos[0]+xAdd, self.pos[1]+yAdd) == 1:
        if self.color != array[self.pos[0]+xAdd, self.pos[1]+yAdd].color:
          if (self.testForChess (array, xAdd, yAdd) == true):
            move.append((self.pos[0]+xAdd, self.pos[1]+yAdd))
            return true
  
    elif moveMode == kingAndKnightSafe:
      if self.onTheBoard(self.pos[0]+xAdd, self.pos[1]+yAdd) == 1:
        if self.color != array[self.pos[0]+xAdd, self.pos[1]+yAdd].color:
          if self.threat(self.pos[0]+xAdd, self.pos[1]+yAdd, array) == notThreatened:
            if (self.testForChess (array, xAdd, yAdd) == true):
              move.append((self.pos[0]+xAdd, self.pos[1]+yAdd))
              return true
  
    elif moveMode == castlingSafe:
      ok = false
      if (self.onTheBoard(self.pos[0]+xAdd*2, self.pos[1]+yAdd) == 1):
        if (self.moved == false):
            if array[self.pos[0]+xAdd, self.pos[1]+yAdd].color == -1:
                if self.threat(self.pos[0], self.pos[1], array) == notThreatened:
                    if self.threat(self.pos[0]+xAdd, self.pos[1]+yAdd, array) == notThreatened:
                      if array[self.pos[0]+xAdd*2, self.pos[1]+yAdd].color == -1:
                        rookX = self.pos[0]+xAdd*2
                        if rookX > 4:
                          rookX = 8
                        else:
                          rookX = 1
                        if (array[rookX, self.pos[1]+yAdd].type == rook):
                          if (array[rookX, self.pos[1]+yAdd].color == self.color):
                            if (array[rookX, self.pos[1]+yAdd].moved == false):
                              if self.threat(self.pos[0]+xAdd*2, self.pos[1]+yAdd, array) == notThreatened:
                                move.append((self.pos[0]+xAdd*2, self.pos[1]+yAdd))
      return ok
    return false

                
  def drawFeet (self, drawMode):
    set_color (self.color, drawMode)
    if self.color == black:
      glRotatef(180,0,0,1)
        
    gfigur = gluNewQuadric()
    gluCylinder(gfigur, 2.1*standardFactor*self.factor, 2.1*standardFactor*self.factor, 1.15*standardFactor*self.factor, 16, 4)
    gluQuadricDrawStyle(gfigur, GLU_FILL)
    glTranslated(0, 0, 1.15*standardFactor*self.factor)
        
    glBegin(GL_POLYGON)
    for i in range(0,40):
      glVertex3f(2.1*standardFactor*self.factor*(math.cos((2*math.pi)*(i/40))), 2.1*standardFactor*self.factor*(math.sin((2*math.pi)*(i/40))), 0)
    glEnd();

    gfigur_2 = gluNewQuadric()
    gluCylinder(gfigur_2, 1.8*standardFactor*self.factor, 1.8*standardFactor*self.factor, 0.35*standardFactor*self.factor, 14, 6)
    gluQuadricDrawStyle(gfigur_2, GLU_FILL)
    glTranslated(0, 0, 0.35*standardFactor*self.factor)

    glBegin(GL_POLYGON)
    for i in range(0,40):
      glVertex3f(2.1*standardFactor*self.factor*(math.cos((2*math.pi)*(i/40))), 2.1*standardFactor*self.factor*(math.sin((2*math.pi)*(i/40))), 0)
    glEnd();

    if drawMode == normal:
      set_color (self.color, color2)
    gfigur_3 = gluNewQuadric()
    gluCylinder(gfigur_3, 1.8*standardFactor*self.factor, self.radius1*standardFactor*self.factor, self.height1*standardFactor*self.factor, 16, 4)
    gluQuadricDrawStyle(gfigur_3, GLU_FILL)
    set_color (self.color, drawMode)

    gluDeleteQuadric (gfigur)
    gluDeleteQuadric (gfigur_2)
    gluDeleteQuadric (gfigur_3)

        
        
  def drawHat (self, number=1):
    if number == 1:
      #hat bottom
      glTranslated(0, 0, self.height1*standardFactor*self.factor)
      gfigur_4 = gluNewQuadric()
      gluCylinder(gfigur_4, self.radius1*standardFactor*self.factor, self.radius2*standardFactor*self.factor, self.height2*standardFactor*self.factor, 16, 4)
      gluQuadricDrawStyle(gfigur_4, GLU_FILL)

      #hat top
      glTranslated(0, 0, self.height2*standardFactor*self.factor)
      gfigur_5 = gluNewQuadric()
      gluCylinder(gfigur_5, self.radius2*standardFactor*self.factor, self.radius3*standardFactor*self.factor, self.height3*standardFactor*self.factor, 16, 4)
      gluQuadricDrawStyle(gfigur_5, GLU_FILL)
      
      gluDeleteQuadric (gfigur_4)
      gluDeleteQuadric (gfigur_5)
      
    elif number == 2:
      #hat bottom
      glTranslated(0, 0, self.height3*standardFactor*self.factor)
      gfigur_4 = gluNewQuadric()
      gluCylinder(gfigur_4, self.radius3*standardFactor*self.factor, self.radius4*standardFactor*self.factor, self.height4*standardFactor*self.factor, 16, 4)
      gluQuadricDrawStyle(gfigur_4, GLU_FILL)

      #hat top
      glTranslated(0, 0, self.height4*standardFactor*self.factor)
      gfigur_5 = gluNewQuadric()
      gluCylinder(gfigur_5, self.radius4*standardFactor*self.factor, 0*standardFactor*self.factor, self.height5*standardFactor*self.factor, 16, 4)
      gluQuadricDrawStyle(gfigur_5, GLU_FILL)
      
      gluDeleteQuadric (gfigur_4)
      gluDeleteQuadric (gfigur_5)
                
                
  def drawHead (self, drawMode):
    set_color (self.color, drawMode)

    glPushMatrix()
    glTranslated(0, 0, (self.height1 + (7/8)*self.headRadius)*standardFactor*self.factor)
    # head:
    gfigur_4 = gluNewQuadric()
    gluQuadricDrawStyle(gfigur_4, GLU_FILL)
    gluSphere(gfigur_4, self.headRadius*standardFactor*self.factor, 16, 16)

    # eyes:
    if (self.eyes == true) and (drawMode == normal):
      glColor3d(1,1,1)
      glPushMatrix()
      glTranslated(0.45*standardFactor*self.factor,4/5*self.headRadius*standardFactor*self.factor,1/3*self.headRadius*standardFactor*self.factor)
      gfigur_5 = gluNewQuadric()
      gluQuadricDrawStyle(gfigur_5, GLU_FILL)
      gluSphere(gfigur_5, 0.37*standardFactor*self.factor, 8, 8)
      glPopMatrix()
      glPushMatrix()
      gluDeleteQuadric (gfigur_5)
      glTranslated(-0.45*standardFactor*self.factor,4/5*self.headRadius*standardFactor*self.factor,1/3*self.headRadius*standardFactor*self.factor)
      gfigur_6 = gluNewQuadric()
      gluQuadricDrawStyle(gfigur_6, GLU_FILL)
      gluSphere(gfigur_6, 0.37*standardFactor*self.factor, 8, 8)
      glPopMatrix()
      gluDeleteQuadric (gfigur_6)

    if drawMode == normal:
      set_color (self.color, color2)
    elif drawMode == shadow:
      set_color (self.color, shadow)
    glTranslated(0, 0, self.crownDepth*standardFactor*self.factor)
    #crown bottom:
    glBegin(GL_POLYGON)
    for i in range(0,40):
      glVertex3f(self.crownRadius*standardFactor*self.factor*(math.cos((2*math.pi)*(i/40))), self.crownRadius*standardFactor*self.factor*(math.sin((2*math.pi)*(i/40))), 0)
    glEnd()
    # crown:
    gfigur_7 = gluNewQuadric()
    gluCylinder(gfigur_7, self.crownRadius*standardFactor*self.factor, self.crownRadius*standardFactor*self.factor, self.crownHeight*standardFactor*self.factor, 16, 4)
    gluQuadricDrawStyle(gfigur_7, GLU_FILL)

    glTranslated(0, 0, self.crownHeight*standardFactor*self.factor)
    #crown top:
    glBegin(GL_POLYGON)
    for i in range(0,40):
      glVertex3f(self.crownRadius*standardFactor*self.factor*(math.cos((2*math.pi)*(i/40))), self.crownRadius*standardFactor*self.factor*(math.sin((2*math.pi)*(i/40))), 0)
    glEnd()

    glPopMatrix()

    gluDeleteQuadric (gfigur_4)
    gluDeleteQuadric (gfigur_7)

                
                
emptyPiece = Piece(-1, -1, -1, -1)
