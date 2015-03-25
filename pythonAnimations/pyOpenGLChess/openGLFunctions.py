# OpenGL functions

from __future__ import division
from OpenGL.GL import *

from defines import *


def set_color (army, colorMode):
  if(colorMode == shadow):
    glColor4d(0,0.0,0,0.6)
    #glmaterialfv(gl_front, gl_shininess, 0.0)
    #glmaterialfv(gl_front, gl_ambient, [0, 0, 0, 0.5])
    #glmaterialfv(gl_front, gl_diffuse, [0, 0, 0, 0])
    #glmaterialfv(gl_front, gl_specular, [0, 0, 0, 0])
  elif(colorMode == color2):
    glColor3d(0,0,0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.35, 0.35, 0.35, 1.0])
  elif(army == black):
    glColor3d(0.6,0.2,0.4)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.35, 0.35, 0.35, 1.0])
  elif(army == white):
    glColor3d(0.3,0.6,0.7)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.35, 0.35, 0.35, 1.0])
    
    
          
                