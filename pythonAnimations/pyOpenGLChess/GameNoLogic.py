from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, sys, time

from defines import *
from openGLFunctions import *

import pygame

import Pawn
import Rook
import Knight
import Bishop
import Queen
import King
import Piece
import Image
import numpy as np
from Piece import emptyPiece

from engineDirectory.sunfish import *


# noinspection PyUnusedLocal,PyPep8Naming
class Game:
    def __init__(self):

        self.ready = False
        self.reshaping = False

        # draw shadows of figures
        self.showShadows = false
        # do animations
        self.doAnimation = false
        self.animationMode = false

        # use engine (basically two or one payer)
        self.useEngine = true

        # init the engine
        self.sunfish = engineSunfish()

        self.camPos = [0, 0, 10]
        self.up = [0, 1, 0]
        self.lookAt = [0, 0, 0]

        self.BGTEXID = 0

        self.zoom = 45.0
        self.button = None
        self.chosenBlock = [-1, -1]
        self.mouse = [0.0, 0.0]
        self.rotation = [0.0, 0.0]  # x and z rotation
        self.turn = white

        self.light = [1.6, 1.3, 7, 0.8]  # light position
        epsilon = -0.02
        self.matrixForShadow = (
            epsilon + self.light[2], 0, 0, 0, 0, epsilon + self.light[2], 0, 0, -self.light[0], -self.light[1], epsilon, -1,
            -epsilon * self.light[0], -epsilon * self.light[1], -epsilon * self.light[2], self.light[2])

        self.pawns = []
        self.rooks = []
        self.knights = []
        self.bishops = []
        self.queens = []
        self.kings = []
        self.height = 0
        self.width = 0
        self.keychache = []
        self.debug = true
        self.currentFrame = None
        self.newFrameArrived = False

        self.projection = None
        self.modelview = None

        self.array = {'Piece': {}, 'Piece': {}}
        self.height = 480
        self.width = 640

        self.clickedCoordinates = (-10.0, -10.0, -10.0)

    def init(self, width, height):

        self.height = height
        self.width = width
        # specify clear values for the color buffers
        # grey background
        glClearColor(0.7, 0.7, 0.7, 0.0)

        # specify the clear value for the depth buffer
        glClearDepth(1.0)
        #return

        # specify the value used for depth buffer comparisons
        # GL_LESS Passes if the incoming depth value is less than the stored depth value
        glDepthFunc(GL_LESS)

        # enable or disable server-side GL capabilities
        # draw lines with correct filtering. Otherwise, draw aliased lines
        glEnable(GL_LINE_SMOOTH)
        # draw points with proper filtering. Otherwise, draw aliased points
        glEnable(GL_POINT_SMOOTH)

        # select flat or smooth shading
        glShadeModel(GL_SMOOTH)

        # If no vertex shader is active,
        # normal vectors are normalized to unit length after transformation and before lighting
        glEnable(GL_NORMALIZE)

        # select a polygon rasterization mode
        # GL_FRONT_AND_BACK: both front and back-facing polygons
        # GL_FILL: The interior of the polygon is filled
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # init the chess board
        self.initPieces()

        # light set position and color
        lightPosition = (self.light[0], self.light[1], self.light[2], self.light[3])
        lightAmbient = (1.0, 1.0, 1.0, 0.0)
        lightDiffuse = (0.6, 0.6, 0.6, 0.0)
        lightSpecular = (0.2, 0.2, 0.2, 0.0)

        # set light source parameters
        glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)

        # have one or more material parameters track the current color
        glEnable(GL_COLOR_MATERIAL)

        # specify material parameters for the lighting model
        # GL_FRONT: Specifies which face or faces are being updated (front facing)
        glMaterialfv(GL_FRONT, GL_SHININESS, 1.0)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.35, 0.35, 0.35, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.35, 0.35, 0.35, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.4, 0.4, 0.4, 1.0])

        # include light i in the evaluation of the lighting equation
        glEnable(GL_LIGHT0)

        # If no vertex shader is active, use the current lighting parameters to compute
        # the vertex color or index. Otherwise, simply associate the current color or index with each vertex
        glEnable(GL_LIGHTING)

        # do depth comparisons and update the depth buffer. Note that even
        # if the depth buffer exists and the depth mask is non-zero, the depth buffer
        # is not updated if the depth test is disabled.

        # TODO: DANGEROUS COMMENT
        glEnable(GL_DEPTH_TEST)

        glClear(GL_DEPTH_BUFFER_BIT)

        # specify the clear value for the stencil buffer
        glClearStencil(0)

        # do stencil testing and update the stencil buffer
        glEnable(GL_STENCIL_TEST)

        if self.debug:
            print "adding axis"
            glNewList(debug, GL_COMPILE_AND_EXECUTE)
            self.addAxis()
            glEndList()
        # end of light


        # display lists generate a contiguous set of empty display lists
        if debug:
            displayLists = glGenLists(18)  # 18)
        else:
            displayLists = glGenLists(17)  # 18)

        glNewList(boardTop, GL_COMPILE_AND_EXECUTE)
        # draw the checkerboard
        self.drawBoardTop()
        glEndList()


        glNewList(background, GL_COMPILE_AND_EXECUTE)
        self.drawBackground()
        glEndList()


        glNewList(drawBorder, GL_COMPILE_AND_EXECUTE)
        # TODO: CAN BE REMOVED LATER (check the glGenLists length)
        self.drawBorder()
        glEndList()

        print "loading figures"
        # create objects
        temp = Pawn.Pawn(black, -1, -1, false)
        glNewList(drawBlackPawn, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()
        temp = Pawn.Pawn(objWhite, -1, -1, false)

        temp = Rook.Rook(black, -1, -1, false)
        glNewList(drawBlackRook, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()
        temp = Rook.Rook(objWhite, -1, -1, true)

        temp = Knight.Knight(black, -1, -1, false)
        glNewList(drawBlackKnight, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()
        temp = Knight.Knight(objWhite, -1, -1, true)

        temp = Bishop.Bishop(black, -1, -1, false)
        glNewList(drawBlackBishop, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()
        temp = Bishop.Bishop(objWhite, -1, -1, true)

        temp = Queen.Queen(black, -1, -1, false)
        glNewList(drawBlackQueen, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()
        temp = Queen.Queen(objWhite, -1, -1, true)

        temp = King.King(black, -1, -1, false)
        glNewList(drawBlackKing, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()
        temp = King.King(objWhite, -1, -1, true)
        print "done"
        # add all objects to the board (Black)
        glNewList(pieceChangeChoiceBlack, GL_COMPILE_AND_EXECUTE)
        self.drawPieceChoiceCallListBlack()
        glEndList()

        # add all objects to the board (White)
        glNewList(pieceChangeChoiceWhite, GL_COMPILE_AND_EXECUTE)
        self.drawPieceChoiceCallListWhite()
        glEndList()



        self.reshape(width, height)



    def setGlProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.projection is not None:
            glLoadMatrixd(self.projection)


    def setGlModelView(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if self.modelview is not None:
            glLoadMatrixd(self.modelview)
            glScale(1.0, 1.0, -1.0)



    def setLookatMatrix(self):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.zoom, self.width / self.height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        #print "cam pos = " + str(self.camPos)
        gluLookAt(self.camPos[0], self.camPos[1], self.camPos[2],
                  self.lookAt[0], self.lookAt[1], self.lookAt[2],
                  self.up[0], self.up[1], self.up[2]
                  )
        glRotatef(self.rotation[0], 1.0, 0.0, 0.0)
        glRotatef(self.rotation[1], 0.0, 0.0, 1.0)

    @staticmethod
    def addAxis():
        glLineWidth(5)
        # Draw x-axis line.
        glColor3d(1.0, 0.0, 0.0)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [1, 0, 0, 0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 0])

        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0.05, 0, 0)
        glEnd()

        # Draw y-axis line.
        glColor3d(0.0, 1.0, 0.0)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 1, 0, 0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 0])
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0.05, 0)
        glEnd()

        # Draw z-axis line.

        glColor3d(0.0, 0.0, 1.0)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 1, 0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 0])
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 0.05)
        glEnd()

    def drawPieceChoiceCallListBlack(self):
        glDisable(GL_COLOR_MATERIAL)
        glColor3d(0.15, 0.5, 0.45)

        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.15, 0.5, 0.35, 0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.0, 0.0, 0.0, 0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 0])

        glBegin(GL_POLYGON)
        glVertex3f((-1) * blockSize, blockSize, 0)
        glVertex3f(0, blockSize, 0)
        glVertex3f(0, 2 * blockSize, 0)
        glVertex3f((-1) * blockSize, 2 * blockSize, 0)
        glEnd()
        glBegin(GL_POLYGON)
        glVertex3f(0, blockSize, 0)
        glVertex3f(blockSize, blockSize, 0)
        glVertex3f(blockSize, 2 * blockSize, 0)
        glVertex3f(0, 2 * blockSize, 0)
        glEnd()
        glBegin(GL_POLYGON)
        glVertex3f(blockSize, blockSize, 0)
        glVertex3f(2 * blockSize, blockSize, 0)
        glVertex3f(2 * blockSize, 2 * blockSize, 0)
        glVertex3f(blockSize, 2 * blockSize, 0)
        glEnd()
        glBegin(GL_POLYGON)
        glVertex3f(2 * blockSize, blockSize, 0)
        glVertex3f(3 * blockSize, blockSize, 0)
        glVertex3f(3 * blockSize, 2 * blockSize, 0)
        glVertex3f(2 * blockSize, 2 * blockSize, 0)
        glEnd()
        glEnable(GL_COLOR_MATERIAL)

        # now draw Pieces:
        glPushMatrix()
        glTranslatef((-0.5) * blockSize, 1.5 * blockSize, 0)
        glCallList(drawBlackQueenObj)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.5 * blockSize, 1.5 * blockSize, 0)
        glCallList(drawBlackBishopObj)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(1.5 * blockSize, 1.5 * blockSize, 0)
        glCallList(drawBlackKnightObj)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(2.5 * blockSize, 1.5 * blockSize, 0)
        glCallList(drawBlackRookObj)
        glPopMatrix()

    def drawPieceChoiceCallListWhite(self):
        glDisable(GL_COLOR_MATERIAL)
        glColor3d(0.15, 0.5, 0.45)

        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.15, 0.5, 0.35, 0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.0, 0.0, 0.0, 0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 0])

        glBegin(GL_POLYGON)
        glVertex3f((-1) * blockSize, blockSize, 0)
        glVertex3f(0, blockSize, 0)
        glVertex3f(0, 2 * blockSize, 0)
        glVertex3f((-1) * blockSize, 2 * blockSize, 0)
        glEnd()
        glBegin(GL_POLYGON)
        glVertex3f(0, blockSize, 0)
        glVertex3f(blockSize, blockSize, 0)
        glVertex3f(blockSize, 2 * blockSize, 0)
        glVertex3f(0, 2 * blockSize, 0)
        glEnd()
        glBegin(GL_POLYGON)
        glVertex3f(blockSize, blockSize, 0)
        glVertex3f(2 * blockSize, blockSize, 0)
        glVertex3f(2 * blockSize, 2 * blockSize, 0)
        glVertex3f(blockSize, 2 * blockSize, 0)
        glEnd()
        glBegin(GL_POLYGON)
        glVertex3f(2 * blockSize, blockSize, 0)
        glVertex3f(3 * blockSize, blockSize, 0)
        glVertex3f(3 * blockSize, 2 * blockSize, 0)
        glVertex3f(2 * blockSize, 2 * blockSize, 0)
        glEnd()
        glEnable(GL_COLOR_MATERIAL)

        # now draw Pieces:
        glPushMatrix()
        glTranslatef((-0.5) * blockSize, 1.5 * blockSize, 0)
        glCallList(drawWhiteQueenObj)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.5 * blockSize, 1.5 * blockSize, 0)
        glCallList(drawWhiteBishopObj)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(1.5 * blockSize, 1.5 * blockSize, 0)
        glCallList(drawWhiteKnightObj)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(2.5 * blockSize, 1.5 * blockSize, 0)
        glCallList(drawWhiteRookObj)
        glPopMatrix()

    def initPieces(self):
        for i in range(-1, 10):
            for j in range(-1, 10):
                self.array[i, j] = emptyPiece
        print "loading pawns"
        # white pawns:
        for i in range(0, 8):
            self.pawns.append(Pawn.Pawn(objWhite, i + 1, 2, true))
            self.array[i + 1, 2] = self.pawns[i]
        # black pawns:
        for i in range(8, 16):
            self.pawns.append(Pawn.Pawn(black, i - 7, 7, false))
            self.array[i - 7, 7] = self.pawns[i]
        # rooks
        print "loading rooks"
        self.rooks.append(Rook.Rook(objWhite, 1, 1, true))
        self.array[1, 1] = self.rooks[0]
        self.rooks.append(Rook.Rook(objWhite, 8, 1, true))
        self.array[8, 1] = self.rooks[1]
        self.rooks.append(Rook.Rook(black, 1, 8, false))
        self.array[1, 8] = self.rooks[2]
        self.rooks.append(Rook.Rook(black, 8, 8, false))
        self.array[8, 8] = self.rooks[3]

        # knights
        print "loading knights"
        self.knights.append(Knight.Knight(objWhite, 2, 1, true))
        self.array[2, 1] = self.knights[0]
        self.knights.append(Knight.Knight(objWhite, 7, 1, true))
        self.array[7, 1] = self.knights[1]
        self.knights.append(Knight.Knight(black, 2, 8, false))
        self.array[2, 8] = self.knights[2]
        self.knights.append(Knight.Knight(black, 7, 8, false))
        self.array[7, 8] = self.knights[3]

        # bishops
        print "loading bishops"
        self.bishops.append(Bishop.Bishop(objWhite, 3, 1, true))
        self.array[3, 1] = self.bishops[0]
        self.bishops.append(Bishop.Bishop(objWhite, 6, 1, true))
        self.array[6, 1] = self.bishops[1]
        self.bishops.append(Bishop.Bishop(black, 3, 8, false))
        self.array[3, 8] = self.bishops[2]
        self.bishops.append(Bishop.Bishop(black, 6, 8, false))
        self.array[6, 8] = self.bishops[3]

        # queens
        print "loading queens"
        self.queens.append(Queen.Queen(objWhite, 4, 1, true))
        self.array[4, 1] = self.queens[0]
        self.queens.append(Queen.Queen(black, 4, 8, false))
        self.array[4, 8] = self.queens[1]

        # kings
        print "loading kings"
        self.kings.append(King.King(objWhite, 5, 1, true))
        self.array[5, 1] = self.kings[0]
        self.kings.append(King.King(black, 5, 8, false))
        self.array[5, 8] = self.kings[1]

    # reshape the animation when the window size changes
    def updateWindowShape(self, width, height):
        self.width = width
        self.height = height


    def reshape(self, width, height):
        self.reshaping = True
        # set the view port with low left corner and width and height
        glViewport(0, 0, width, height)
        self.updateWindowShape(width, height)

        # specify which matrix is the current matrix
        # GL_PROJECTION : Applies subsequent matrix operations to the projection matrix stack
        glMatrixMode(GL_PROJECTION)

        # replace the current matrix with the identity matrix
        glLoadIdentity()

        # set up a perspective projection matrix
        # Specifies the field of view angle, in degrees, in the y direction
        # Specifies the aspect ratio that determines the field of view in the
        # x direction. The aspect ratio is the ratio of x (width) to y (height).
        # Specifies the distance from the viewer to the near clipping plane (always positive)
        # Specifies the distance from the viewer to the far clipping plane (always positive)

        gluPerspective(45.0, width / height, 0.1, 100.0)

        # GL_MODELVIEW : Applies subsequent matrix operations to the modelview matrix stack
        glMatrixMode(GL_MODELVIEW)

        # replace the current matrix with the identity matrix
        glLoadIdentity()
        self.reshaping = False

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.drawBackground()

        self.setGlProjection()
        self.setGlModelView()

        self.beginRedraw()



        self.drawBoardTop()
        glCallList(drawBorder)
        # if self.pieceChange == true:
        self.endRedraw()



    def drawAnim(self):
        # start to redraw the scene
        self.beginRedraw()
        # draw the top board
        glCallList(boardTopAnim)
        # Todo: can be removed
        glCallList(drawBorder)

        self.endRedraw()

    def beginRedraw(self):
        # clear buffers to preset values
        # GL_COLOR_BUFFER_BIT: Indicates the buffers currently enabled for color writing.
        # GL_DEPTH_BUFFER_BIT: Indicates the depth buffer.


        # load a identity matrix
        # glLoadIdentity()

        # multiply the current matrix with a translation matrix
        # glTranslatef(0.0, 0.0, -10.0)

        # apply the current rotations
        # glRotatef(self.rotation[0], 1.0, 0.0, 0.0)
        # glRotatef(self.rotation[1], 0.0, 0.0, 1.0)

        # have one or more material parameters track the current color
        glDisable(GL_COLOR_MATERIAL)

        # specify the clear value for the stencil buffer
        glClearStencil(0)

        # reset the stencil bit
        glClear(GL_STENCIL_BUFFER_BIT)

        # set front and back function and reference value for stencil testing
        glStencilFunc(GL_ALWAYS, 0, 0x1)

        # set front and back stencil test actions
        glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)

        # draw the grey ground plane
        # Todo: can be reomved when it comes to VR
        glCallList(boardBottom)

        if debug:
            #print "adding axis"
            glCallList(debug)

        # set front and back function and reference value for stencil testing
        glStencilFunc(GL_ALWAYS, 1, 0x1)
        # set front and back stencil test actions
        glStencilOp(GL_REPLACE, GL_REPLACE, GL_REPLACE)

    def endRedraw(self):
        glEnable(GL_COLOR_MATERIAL)
        glPushMatrix()
        glMultMatrixd(self.matrixForShadow)

        glStencilFunc(GL_EQUAL, 1, 0x1)
        glStencilOp(GL_KEEP, GL_KEEP, GL_INCR)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_LIGHTING)
        # draw the shadows
        if self.showShadows == 1:
            self.drawShadows()

        glPopMatrix()
        glEnable(GL_LIGHTING)
        glDisable(GL_BLEND)

        glStencilFunc(GL_ALWAYS, 1, 0x1)
        glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)

        # draw all pieces
        self.drawPieces()

        glutSwapBuffers()
        glFlush()


    def key_pressed(self, key, x, y):
        ESCAPE = chr(27)

        if key == ESCAPE:
            sys.exit()

        elif key == 'x':
            if self.doAnimation == 1:
                self.doAnimation = 0
            else:
                self.doAnimation = 1

        elif key == 's':
            if self.showShadows == 1:
                self.showShadows = 0
            else:
                self.showShadows = 1
        elif key == 't':
            print "reset the cam pos"
            self.camPos = [sum(x) for x in zip(self.camPos, [1, 1, 1])]
        else:
            self.keychache.append(key)
            # assume a move was entered
            if len(self.keychache) == 4:
                move = ""
                for curKey in self.keychache:
                    move += curKey

                self.keychache = []
                print "Your move: " + move
                if self.sunfish.setMove(move):
                    self.setMove(move)
                    self.redraw()
                    engMove = self.sunfish.computeNextStep()
                    self.setMove(engMove)
                    self.redraw()

        if self.animationMode == 0:
            self.redraw()

    # handle mouse movement
    def mouse_moved(self, x, y):
        # only if the right button is used
        if self.button == GLUT_LEFT_BUTTON:
            # set the current rotation
            self.rotation[0] += (y - self.mouse[1]) / 85
            self.rotation[1] += (x - self.mouse[0]) / 85
            # mark the current window as needing to be redisplayed
            glutPostRedisplay()

    # handle clicks and scrolling
    def mouse_pressed(self, button, state, x, y):
        self.button = button
        # set the clicked coordinates
        if (button == GLUT_LEFT_BUTTON) and (state == GLUT_DOWN):
            self.mouse[0] = x
            self.mouse[1] = y
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            # print "redraw"
            self.redraw()

        # handle scroll event
        elif button == 3 or button == 4:
            if state == GLUT_UP:
                return

            if button == 3:
                self.zoom -= 1
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(self.zoom, self.width / self.height, 0.1, 100.0)
                glMatrixMode(GL_MODELVIEW)
                self.redraw()
            else:
                self.zoom += 1
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(self.zoom, self.width / self.height, 0.1, 100.0)
                glMatrixMode(GL_MODELVIEW)
                self.redraw()

        elif (button == GLUT_LEFT_BUTTON) and (state == GLUT_UP):
            return

    def processMenuEvents(self, option):
        if option == 0:
            if self.doAnimation == 1:
                self.doAnimation = 0
            else:
                self.doAnimation = 1

        elif option == 1:
            if self.showShadows == 1:
                self.showShadows = 0
            else:
                self.showShadows = 1

        elif option == 2:
            print "Undo not supported"

        elif option == 3:
            sys.exit()

        if self.animationMode == 0:
            self.redraw()


    def drawBackground(self):
        """  Draw background image using a quad. """
        if self.newFrameArrived and not self.reshaping:
            imgHeight, imgwidth, _ = self.currentFrame.shape
            if imgHeight == self.height and imgwidth == self.width:
                glDisable(GL_DEPTH_TEST)
                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                glLoadIdentity()
                glMatrixMode(GL_PROJECTION)
                glPushMatrix()
                #print "Happy printings1"
                #glMatrixMode(GL_MODELVIEW)
                #glLoadIdentity()

                #print "Happy printings"
                glLoadIdentity()
                #print "Happy printings"
                glOrtho(0, self.width, 0, self.height, -1.0, 1.0)
                #print "Happy printings"
                glViewport(0, 0, self.width, self.height)
                #print "Happy printings"
                glDisable(GL_TEXTURE_2D)
                glPixelZoom(1, -1)
                glRasterPos3f(0, self.height-0.5, -1)
                #print "Happy printings5"
                glDrawPixels(self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE, self.currentFrame)
                #print "Happy printings6"
                # glBegin(GL_QUADS)
                # glTexCoord2f(0.0,0.0); glVertex3f(-4.0,-3.0,-10.0)
                # glTexCoord2f(1.0,0.0); glVertex3f( 4.0,-3.0,-10.0)
                # glTexCoord2f(1.0,1.0); glVertex3f( 4.0, 3.0,-10.0)
                # glTexCoord2f(0.0,1.0); glVertex3f(-4.0, 3.0,-10.0)
                # glEnd()
                glPopMatrix()
                glMatrixMode(GL_MODELVIEW)
                glPopMatrix()
                glEnable(GL_DEPTH_TEST)
            #self.newFrameArrived = False



    def drawBoardBottom(self):
        # set the color
        glColor3d(0.8, 0.9, 0.5)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.4, 0.4, 0.5, 0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.5, 0.5, 0.5, 0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.0, 0])


        # board bottom
        glBegin(GL_POLYGON)
        glNormal3d(0, 0, -1)
        glVertex3f(-4.5 * blockSize, -4.5 * blockSize, -blockSize / 2)
        glNormal3d(0, 0, -1)
        glVertex3f(-4.5 * blockSize, 4.5 * blockSize, -blockSize / 2)
        glNormal3d(0, 0, -1)
        glVertex3f(4.5 * blockSize, 4.5 * blockSize, -blockSize / 2)
        glNormal3d(0, 0, -1)
        glVertex3f(4.5 * blockSize, -4.5 * blockSize, -blockSize / 2)
        glEnd()

        # board sides:
        # glColor3d(0.3,0.1,0.5)
        glBegin(GL_POLYGON)
        glNormal3d(-1, 0, 0)
        glVertex3f(-4.5 * blockSize, -4.5 * blockSize, -blockSize / 2)
        glNormal3d(-1, 0, 0)
        glVertex3f(-4.5 * blockSize, 4.5 * blockSize, -blockSize / 2)
        glNormal3d(-1, 0, 0)
        glVertex3f(-4.5 * blockSize, 4.5 * blockSize, 0)
        glNormal3d(-1, 0, 0)
        glVertex3f(-4.5 * blockSize, -4.5 * blockSize, 0)
        glEnd()

        glBegin(GL_POLYGON)
        glNormal3d(1, 0, 0)
        glVertex3f(4.5 * blockSize, 4.5 * blockSize, -blockSize / 2)
        glNormal3d(1, 0, 0)
        glVertex3f(4.5 * blockSize, -4.5 * blockSize, -blockSize / 2)
        glNormal3d(1, 0, 0)
        glVertex3f(4.5 * blockSize, -4.5 * blockSize, 0)
        glNormal3d(1, 0, 0)
        glVertex3f(4.5 * blockSize, 4.5 * blockSize, 0)
        glEnd()

        glBegin(GL_POLYGON)
        glNormal3d(0, 1, 0)
        glVertex3f(-4.5 * blockSize, 4.5 * blockSize, -blockSize / 2)
        glNormal3d(0, 1, 0)
        glVertex3f(4.5 * blockSize, 4.5 * blockSize, -blockSize / 2)
        glNormal3d(0, 1, 0)
        glVertex3f(4.5 * blockSize, 4.5 * blockSize, 0)
        glNormal3d(0, 1, 0)
        glVertex3f(-4.5 * blockSize, 4.5 * blockSize, 0)
        glEnd()

        glBegin(GL_POLYGON)
        glNormal3d(0, -1, 0)
        glVertex3f(-4.5 * blockSize, -4.5 * blockSize, -blockSize / 2)
        glNormal3d(0, -1, 0)
        glVertex3f(4.5 * blockSize, -4.5 * blockSize, -blockSize / 2)
        glNormal3d(0, -1, 0)
        glVertex3f(4.5 * blockSize, -4.5 * blockSize, 0)
        glNormal3d(0, -1, 0)
        glVertex3f(-4.5 * blockSize, -4.5 * blockSize, 0)
        glEnd()

    def setMove(self, move):
        abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        oldX = abc.index(move[0]) + 1
        oldY = int(move[1])
        newX = abc.index(move[2]) + 1
        newY = int(move[3])

        self.activePiece = self.array[oldX, oldY]

        # only turkis color is enabled if
        self.turn = 30
        self.activePiece.pos[0] = newX
        self.activePiece.pos[1] = newY
        if self.array[newX, newY] != emptyPiece:
            self.array[newX, newY].kill()
        self.array[newX, newY] = self.activePiece



    @staticmethod
    def drawBoardTop():
        # board blocks:

        for i in range(0, 8):
            for j in range(0, 8):
                if ((i % 2 == 0) and (j % 2 != 0)) or ((i % 2 != 0) and (j % 2 == 0)):
                    # white
                    glColor3d(0.95, 0.95, 0.95)
                    glMaterialfv(GL_FRONT, GL_AMBIENT, [1, 1, 1, 0])
                    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.1, 0.1, 0.1, 0])
                    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 0])
                else:
                    # black
                    glColor3d(0.05, 0.05, 0.05)
                    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0, 0.0, 0.0, 0])
                    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.1, 0.1, 0.1, 0])
                    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 0])

                glBegin(GL_POLYGON)
                glVertex3f((-4 + i) * blockSize, (-4 + j) * blockSize, 0)
                glVertex3f((-4 + i + 1) * blockSize, (-4 + j) * blockSize, 0)
                glVertex3f((-4 + i + 1) * blockSize, (-4 + j + 1) * blockSize, 0)
                glVertex3f((-4 + i) * blockSize, (-4 + j + 1) * blockSize, 0)
                glEnd()

    @staticmethod
    def drawBorder():

        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.4, 0.4, 0.5, 0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.5, 0.5, 0.5, 0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.0, 0])

        # extension for shadow:
        glBegin(GL_POLYGON)
        glNormal3d(0, 0, 1)
        glVertex3f(-4.5 * blockSize, -4.5 * blockSize, -0)
        glNormal3d(0, 0, 1)
        glVertex3f(-4.5 * blockSize, 4.5 * blockSize, -0)
        glNormal3d(0, 0, 1)
        glVertex3f(-4 * blockSize, 4.5 * blockSize, -0)
        glNormal3d(0, 0, 1)
        glVertex3f(-4 * blockSize, -4.5 * blockSize, -0)
        glEnd()
        glBegin(GL_POLYGON)
        glNormal3d(0, 0, 1)
        glVertex3f(-4 * blockSize, -4.5 * blockSize, -0)
        glNormal3d(0, 0, 1)
        glVertex3f(4 * blockSize, -4.5 * blockSize, -0)
        glNormal3d(0, 0, 1)
        glVertex3f(4 * blockSize, -4 * blockSize, -0)
        glNormal3d(0, 0, 1)
        glVertex3f(-4 * blockSize, -4 * blockSize, -0)
        glEnd()
        glBegin(GL_POLYGON)
        glNormal3d(0, 0, 1)
        glVertex3f(4.5 * blockSize, -4.5 * blockSize, -0)
        glNormal3d(0, 0, 1)
        glVertex3f(4.5 * blockSize, 4.5 * blockSize, -0)
        glNormal3d(0, 0, 1)
        glVertex3f(4 * blockSize, 4.5 * blockSize, -0)
        glNormal3d(0, 0, 1)
        glVertex3f(4 * blockSize, -4.5 * blockSize, -0)
        glEnd()
        glBegin(GL_POLYGON)
        glNormal3d(0, 0, 1)
        glVertex3f(-4 * blockSize, 4.5 * blockSize, -0)
        glNormal3d(0, 0, 1)
        glVertex3f(4 * blockSize, 4.5 * blockSize, -0)
        glNormal3d(0, 0, 1)
        glVertex3f(4 * blockSize, 4 * blockSize, -0)
        glNormal3d(0, 0, 1)
        glVertex3f(-4 * blockSize, 4 * blockSize, -0)
        glEnd()

    # draw all figures
    def drawPieces(self):
        for i in range(0, len(self.pawns)):
            self.pawns[i].draw()

        for i in range(0, len(self.rooks)):
            self.rooks[i].draw()

        for i in range(0, len(self.knights)):
            self.knights[i].draw()

        for i in range(0, len(self.bishops)):
            self.bishops[i].draw()

        for i in range(0, len(self.queens)):
            self.queens[i].draw()

        for i in range(0, len(self.kings)):
            self.kings[i].draw()

    # draw the shadows for all figures
    def drawShadows(self):
        for i in range(0, len(self.pawns)):
            self.pawns[i].drawShadow()

        for i in range(0, len(self.rooks)):
            self.rooks[i].drawShadow()

        for i in range(0, len(self.knights)):
            self.knights[i].drawShadow()

        for i in range(0, len(self.bishops)):
            self.bishops[i].drawShadow()

        for i in range(0, len(self.queens)):
            self.queens[i].drawShadow()

        for i in range(0, len(self.kings)):
            self.kings[i].drawShadow()

    def idleDraw(self):
        self.redraw()



    def start(self):
        argv = glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL)  # GLUT_ALPHA missing
        glutInitWindowPosition(20, 20)
        glutInitWindowSize(640, 480)
        glutCreateWindow("Augmented Reality Chess")

        glutDisplayFunc(self.redraw)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.key_pressed)
        glutMotionFunc(self.mouse_moved)
        glutMouseFunc(self.mouse_pressed)
        glutIdleFunc(self.idleDraw)

        glutCreateMenu(self.processMenuEvents)
        glutAddMenuEntry("toggle animation mode", 0)
        glutAddMenuEntry("toggle shadow mode", 1)
        glutAddMenuEntry("undo", 2)
        glutAddMenuEntry("Quit", 3)
        glutAttachMenu(GLUT_MIDDLE_BUTTON)

        self.init(640, 480)

        self.redraw()

        self.ready = True
        glutMainLoop()
