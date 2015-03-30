from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, sys, time

from defines import *
from openGLFunctions import *

import Pawn
import Rook
import Knight
import Bishop
import Queen
import King
import Piece
from Piece import emptyPiece


from engineDirectory.sunfish import *


# noinspection PyUnusedLocal,PyPep8Naming
class Game:
    def __init__(self):
        # draw shadows of figures
        self.showShadows = true
        # do animations
        self.doAnimation = false

        # use engine (basically two or one payer)
        self.useEngine = true

        # init the engine
        self.sunfish = engineSunfish()

        self.zoom = 45.0
        self.button = None
        self.chosenBlock = [-1, -1]
        self.mouse = [0.0, 0.0]
        self.rotation = [0.0, 0.0]  # x and z rotation
        self.turn = white

        self.light = [1.6, 1.3, 7, 0.8]  # light position
        epsilon = -0.02
        self.matrixForShadow = (epsilon + self.light[2], 0, 0, 0, 0, epsilon + self.light[2], 0, 0, -self.light[0], -self.light[1], epsilon, -1, -epsilon * self.light[0], -epsilon * self.light[1], -epsilon * self.light[2], self.light[2])

        self.pawns = []
        self.rooks = []
        self.knights = []
        self.bishops = []
        self.queens = []
        self.kings = []
        self.height = 0
        self.width = 0

        self.array = {'Piece': {}, 'Piece': {}}

        self.clickedCoordinates = (-10.0, -10.0, -10.0)

    def init(self, width, height):

        self.height = height
        self.width = width
        # specify clear values for the color buffers
        glClearColor(0.4, 0.4, 0.4, 0.0)

        # specify the clear value for the depth buffer
        glClearDepth(1.0)

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
        lightAmbient = (0.6, 0.6, 0.6, 0.0)
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
        #  GL_FRONT: Specifies which face or faces are being updated (front facing)
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
        glEnable(GL_DEPTH_TEST)

        # specify the clear value for the stencil buffer
        glClearStencil(0)

        # do stencil testing and update the stencil buffer
        glEnable(GL_STENCIL_TEST)

        # end of light

        # display lists generate a contiguous set of empty display lists
        displayLists = glGenLists(17)  # 18)

        # create or replace a display list (Display lists are groups of GL
        # commands that have been stored for subsequent execution)
        # Specifies the display-list name.
        # Specifies the compilation mode
        # TODO: CAN BE REMOVED LATER (check the glGenLists length)
        glNewList(boardBottom, GL_COMPILE_AND_EXECUTE)
        # draw the sides and the bottom of the board
        self.drawBoardBottom()
        glEndList()

        glNewList(boardTop, GL_COMPILE_AND_EXECUTE)
        # draw the checkerboard
        self.drawBoardTop()
        glEndList()

        # TODO: CHECK THE SIZE of glGenLists length (prob -1)
        # glNewList(boardTopAnim, GL_COMPILE_AND_EXECUTE)
        # self.drawBoardTopAnim()
        # glEndList()

        glNewList(drawBorder, GL_COMPILE_AND_EXECUTE)
        # TODO: CAN BE REMOVED LATER (check the glGenLists length)
        self.drawBorder()
        glEndList()

        # create a pawn ()
        # TODO: change to loading from model (all)
        temp = Pawn.Pawn(black, -1, -1)
        glNewList(drawBlackPawn, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()

        temp = Pawn.Pawn(white, -1, -1)
        glNewList(drawWhitePawn, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()

        temp = Rook.Rook(black, -1, -1)
        glNewList(drawBlackRook, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()

        temp = Rook.Rook(white, -1, -1)
        glNewList(drawWhiteRook, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()

        temp = Knight.Knight(black, -1, -1)
        glNewList(drawBlackKnight, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()

        temp = Knight.Knight(white, -1, -1)
        glNewList(drawWhiteKnight, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()

        temp = Bishop.Bishop(black, -1, -1)
        glNewList(drawBlackBishop, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()

        temp = Bishop.Bishop(white, -1, -1)
        glNewList(drawWhiteBishop, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()

        temp = Queen.Queen(black, -1, -1, false)
        glNewList(drawBlackQueen, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()

        temp = Queen.Queen(objWhite, -1, -1, true)
        # glNewList(drawWhiteQueen, GL_COMPILE_AND_EXECUTE)
        # temp.drawMe(normal)
        # glEndList()

        temp = King.King(black, -1, -1)
        glNewList(drawBlackKing, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()

        temp = King.King(white, -1, -1)
        glNewList(drawWhiteKing, GL_COMPILE_AND_EXECUTE)
        temp.drawMe(normal)
        glEndList()

        # add all objects to the board (Black)
        glNewList(pieceChangeChoiceBlack, GL_COMPILE_AND_EXECUTE)
        self.drawPieceChoiceCallListBlack()
        glEndList()

        # add all objects to the board (White)
        glNewList(pieceChangeChoiceWhite, GL_COMPILE_AND_EXECUTE)
        self.drawPieceChoiceCallListWhite()
        glEndList()

        self.reshape(width, height)

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
        glCallList(drawBlackQueen)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.5 * blockSize, 1.5 * blockSize, 0)
        glCallList(drawBlackBishop)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(1.5 * blockSize, 1.5 * blockSize, 0)
        glCallList(drawBlackKnight)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(2.5 * blockSize, 1.5 * blockSize, 0)
        glCallList(drawBlackRook)
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
        glCallList(drawWhiteBishop)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(1.5 * blockSize, 1.5 * blockSize, 0)
        glCallList(drawWhiteKnight)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(2.5 * blockSize, 1.5 * blockSize, 0)
        glCallList(drawWhiteRook)
        glPopMatrix()


    def drawPieceChoice(self):
        if (self.activePiece != None):
            if (self.activePiece.color == white):
                yAdd = 1
            else:
                yAdd = -1
            glPushMatrix()
            glTranslatef(blockSize * (-5 + self.activePiece.pos[0]), blockSize * (-6 + self.activePiece.pos[1] + yAdd),
                         0.01 * blockSize)
            if (self.activePiece.color == white):
                glCallList(pieceChangeChoiceWhite)
            else:
                glCallList(pieceChangeChoiceBlack)
            glPopMatrix()

    def initPieces(self):
        for i in range(-1, 10):
            for j in range(-1, 10):
                self.array[i, j] = emptyPiece
        # white pawns:
        for i in range(0, 8):
            self.pawns.append(Pawn.Pawn(white, i + 1, 2))
            self.array[i + 1, 2] = self.pawns[i]
        # black pawns:
        for i in range(8, 16):
            self.pawns.append(Pawn.Pawn(black, i - 7, 7))
            self.array[i - 7, 7] = self.pawns[i]
        # rooks
        self.rooks.append(Rook.Rook(white, 1, 1))
        self.array[1, 1] = self.rooks[0]
        self.rooks.append(Rook.Rook(white, 8, 1))
        self.array[8, 1] = self.rooks[1]
        self.rooks.append(Rook.Rook(black, 1, 8))
        self.array[1, 8] = self.rooks[2]
        self.rooks.append(Rook.Rook(black, 8, 8))
        self.array[8, 8] = self.rooks[3]

        # knights
        self.knights.append(Knight.Knight(white, 2, 1))
        self.array[2, 1] = self.knights[0]
        self.knights.append(Knight.Knight(white, 7, 1))
        self.array[7, 1] = self.knights[1]
        self.knights.append(Knight.Knight(black, 2, 8))
        self.array[2, 8] = self.knights[2]
        self.knights.append(Knight.Knight(black, 7, 8))
        self.array[7, 8] = self.knights[3]

        # bishops
        self.bishops.append(Bishop.Bishop(white, 3, 1))
        self.array[3, 1] = self.bishops[0]
        self.bishops.append(Bishop.Bishop(white, 6, 1))
        self.array[6, 1] = self.bishops[1]
        self.bishops.append(Bishop.Bishop(black, 3, 8))
        self.array[3, 8] = self.bishops[2]
        self.bishops.append(Bishop.Bishop(black, 6, 8))
        self.array[6, 8] = self.bishops[3]

        # queens
        self.queens.append(Queen.Queen(objWhite, 4, 1, true))
        self.array[4, 1] = self.queens[0]
        self.queens.append(Queen.Queen(black, 4, 8, false))
        self.array[4, 8] = self.queens[1]

        # kings
        self.kings.append(King.King(white, 5, 1))
        self.array[5, 1] = self.kings[0]
        self.kings.append(King.King(black, 5, 8))
        self.array[5, 8] = self.kings[1]

    # reshape the animation when the window size changes
    @staticmethod
    def reshape(width, height):
        #  set the view port with low left corner and width and height
        glViewport(0, 0, width, height)

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

    def redraw(self):
        self.beginRedraw()
        # glCallList (boardTop)
        self.drawBoardTop()

        glCallList(drawBorder)
        # if self.pieceChange == true:
        #    self.drawPieceChoice()
        self.endRedraw()


    def checkForCheck(self):
        if (self.isInCheck() == true):
            self.check = true
        else:
            self.check = false
        if (self.isCheckMate() == true):
            self.checkmate = true
        else:
            self.checkmate = false


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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # load a identity matrix
        glLoadIdentity()

        # multiply the current matrix with a translation matrix
        glTranslatef(0.0, 0.0, -10.0)

        # apply the current rotations
        glRotatef(self.rotation[0], 1.0, 0.0, 0.0)
        glRotatef(self.rotation[1], 0.0, 0.0, 1.0)

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


    def toggleTurn(self):
        if self.turn == white:
            self.turn = black
        else:
            self.turn = white

    def key_pressed(self, key, x, y):
        ESCAPE = chr(27)

        if key == ESCAPE:
            sys.exit()

        elif key == 'a':
            if self.doAnimation == 1:
                self.doAnimation = 0
            else:
                self.doAnimation = 1

        elif key == 's':
            if self.showShadows == 1:
                self.showShadows = 0
            else:
                self.showShadows = 1

        if self.animationMode == 0:
            self.redraw()

    # handle mouse movement
    def mouse_moved(self, x, y):
        # only if the right button is used
        if self.button != GLUT_RIGHT_BUTTON:
            return
        # set the current rotation
        self.rotation[0] += (y - self.mouse[1]) / 85
        self.rotation[1] += (x - self.mouse[0]) / 85
        #  mark the current window as needing to be redisplayed
        glutPostRedisplay()

    # handle clicks and scrolling
    def mouse_pressed(self, button, state, x, y):
        self.button = button
        # set the clicked coordinates
        if (button == GLUT_RIGHT_BUTTON) and (state == GLUT_DOWN):
            self.mouse[0] = x
            self.mouse[1] = y

        # handle scroll event
        elif button == 3 or button == 4:
            if state == GLUT_UP:
                return

            if button == 3:
                self.zoom += 1
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(self.zoom, self.width / self.height, 0.1, 100.0)
                glMatrixMode(GL_MODELVIEW)
                self.redraw()
            else:
                self.zoom -= 1
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(self.zoom, self.width / self.height, 0.1, 100.0)
                glMatrixMode(GL_MODELVIEW)
                self.redraw()

        elif (button == GLUT_LEFT_BUTTON) and (state == GLUT_UP):
            model = glGetDoublev(GL_MODELVIEW_MATRIX)
            proj = glGetDoublev(GL_PROJECTION_MATRIX)
            view = glGetIntegerv(GL_VIEWPORT)
            z = glReadPixelsf(x, view[3] - y - 1, 1, 1, GL_DEPTH_COMPONENT)
            self.clickedCoordinates = gluUnProject(x, view[3] - y - 1, z[0][0], model, proj, view)

            move = self.handleClick()
            self.redraw()

            if self.useEngine == true and move != "":
                # use a engine
                print "received move " + move
                print self.sunfish
                self.sunfish.setMove(move)
                engMove = self.sunfish.computeNextStep()
                self.setMove(engMove)
                self.redraw()


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


    def move(self, x, y, castling=false):

        self.array[self.activePiece.pos[0], self.activePiece.pos[1]] = emptyPiece
        # move:
        destination = [x, y]
        mov = 0.15
        distance = 0.3
        delta = [0, 0]
        mark = [-5, -5]
        index = [0, 0]
        s0 = [0, 0]
        s1 = [0, 0]
        to1 = 1
        fro1 = 1
        to2 = 1
        fro2 = 1

        self.activePiece.animate = 1
        self.activePiece.anim[0] = self.activePiece.pos[0]
        self.activePiece.anim[1] = self.activePiece.pos[1]
        delta[0] = destination[0] - self.activePiece.pos[0]
        if delta[0] > 0:
            mark[0] = 1
        elif delta[0] < 0:
            delta[0] *= -1
            mark[0] = -1
        else:
            mark[0] = 0
        delta[1] = destination[1] - self.activePiece.pos[1]
        if delta[1] > 0:
            mark[1] = 1
        elif delta[1] < 0:
            delta[1] *= -1
            mark[1] = -1
        else:
            mark[1] = 0

        if delta[1] > delta[0]:
            index[0] = 1
            index[1] = 0
        else:
            index[0] = 0
            index[1] = 1

        if (self.activePiece.type == knight):
            if delta[0] < delta[1]:
                s0 = [self.activePiece.pos[0], self.activePiece.pos[1] + mark[1]]
                s1 = [self.activePiece.pos[0] + mark[0], self.activePiece.pos[1] + mark[1]]
            else:
                s0 = [self.activePiece.pos[0] + mark[0], self.activePiece.pos[1]]
                s1 = [self.activePiece.pos[0] + mark[0], self.activePiece.pos[1] + mark[1]]

        akt = [-1, -1]
        if ((s0 != [0, 0]) and (self.array[s0[0], s0[1]] != emptyPiece)):
            self.array[s0[0], s0[1]].animate = 1
            self.array[s0[0], s0[1]].anim = [s0[0], s0[1]]
        if ((s1 != [0, 0]) and (self.array[s1[0], s1[1]] != emptyPiece)):
            self.array[s1[0], s1[1]].animate = 1
            self.array[s1[0], s1[1]].anim = [s1[0], s1[1]]

        if delta[1] > delta[0]:
            if mark[1] == 1:  # up
                while (self.activePiece.anim[1] + mark[1] * mov < destination[1]):
                    self.activePiece.anim[1] += mark[1] * mov
                    if (mark[0] >= 0):
                        if delta[1] != 0:
                            self.activePiece.anim[0] += mark[0] * mov * delta[0] / delta[1]
                            akt_x = int(self.activePiece.anim[0] + mark[0] * distance * blockSize * delta[0] / delta[1])
                        else:
                            akt_x = self.activePiece.pos[0]
                        akt_y = int(math.ceil(self.activePiece.anim[1] + mark[1] * distance * blockSize))
                        #draw aside:
                        if ((s0 != [0, 0]) and (self.array[s0[0], s0[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s0[0], s0[1]].anim[0] - mov * 5 / 12 > self.array[s0[0], s0[1]].pos[
                                0] - 0.4) and (to1 == 1)):
                                self.array[s0[0], s0[1]].anim[0] -= mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] += mov * 5 / 12
                            elif ((self.array[s0[0], s0[1]].anim[0] + mov * 5 / 12 < self.array[s0[0], s0[1]].pos[0]) and (
                                fro1 == 1)):
                                to1 = 0
                                self.array[s0[0], s0[1]].anim[0] += mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] -= mov * 5 / 12
                            else:
                                fro1 = 0
                                self.array[s0[0], s0[1]].anim[0] = self.array[s0[0], s0[1]].pos[0]
                                self.array[s0[0], s0[1]].anim[1] = self.array[s0[0], s0[1]].pos[1]
                                self.array[s0[0], s0[1]].animate = 0
                        if ((s1 != [0, 0]) and (self.array[s1[0], s1[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s1[0], s1[1]].anim[0] + mov * 5 / 12 < self.array[s1[0], s1[1]].pos[
                                0] + 0.4) and (to2 == 1)):
                                self.array[s1[0], s1[1]].anim[0] += mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] -= mov * 5 / 12
                            elif ((self.array[s1[0], s1[1]].anim[0] - mov * 5 / 12 > self.array[s1[0], s1[1]].pos[0]) and (
                                fro2 == 1)):
                                to2 = 0
                                self.array[s1[0], s1[1]].anim[0] -= mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] += mov * 5 / 12
                            else:
                                fro2 = 0
                                self.array[s1[0], s1[1]].anim[0] = self.array[s1[0], s1[1]].pos[0]
                                self.array[s1[0], s1[1]].anim[1] = self.array[s1[0], s1[1]].pos[1]
                                self.array[s1[0], s1[1]].animate = 0

                    elif (mark[0] < 0):
                        if delta[1] != 0:
                            self.activePiece.anim[0] += mark[0] * mov * delta[0] / delta[1]
                            akt_x = int(self.activePiece.anim[0] + mark[0] * distance * blockSize * delta[0] / delta[1])
                        else:
                            akt_x = self.activePiece.pos[0]
                        akt_y = int(math.ceil(self.activePiece.anim[1] + mark[1] * distance * blockSize))
                        #draw aside:
                        if ((s0 != [0, 0]) and (self.array[s0[0], s0[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s0[0], s0[1]].anim[0] + mov * 5 / 12 < self.array[s0[0], s0[1]].pos[
                                0] + 0.4) and (to1 == 1)):
                                self.array[s0[0], s0[1]].anim[0] += mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] += mov * 5 / 12
                            elif ((self.array[s0[0], s0[1]].anim[0] - mov * 5 / 12 > self.array[s0[0], s0[1]].pos[0]) and (
                                fro1 == 1)):
                                to1 = 0
                                self.array[s0[0], s0[1]].anim[0] -= mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] -= mov * 5 / 12
                            else:
                                fro1 = 0
                                self.array[s0[0], s0[1]].anim[0] = self.array[s0[0], s0[1]].pos[0]
                                self.array[s0[0], s0[1]].anim[1] = self.array[s0[0], s0[1]].pos[1]
                                self.array[s0[0], s0[1]].animate = 0
                        if ((s1 != [0, 0]) and (self.array[s1[0], s1[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s1[0], s1[1]].anim[0] - mov * 5 / 12 > self.array[s1[0], s1[1]].pos[
                                0] - 0.4) and (to2 == 1)):
                                self.array[s1[0], s1[1]].anim[0] -= mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] -= mov * 5 / 12
                            elif ((self.array[s1[0], s1[1]].anim[0] + mov * 5 / 12 < self.array[s1[0], s1[1]].pos[0]) and (
                                fro2 == 1)):
                                to2 = 0
                                self.array[s1[0], s1[1]].anim[0] += mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] += mov * 5 / 12
                            else:
                                fro2 = 0
                                self.array[s1[0], s1[1]].anim[0] = self.array[s1[0], s1[1]].pos[0]
                                self.array[s1[0], s1[1]].anim[1] = self.array[s1[0], s1[1]].pos[1]
                                self.array[s1[0], s1[1]].animate = 0


                    #self.drawAside(self.activePiece,akt_x,akt_y,delta[0],delta[1],mark[0],mark[1],destination[0],destination[1])
                    #time.sleep(0.003)
                    if self.array[destination[0], destination[1]] != emptyPiece:
                        self.array[destination[0], destination[1]].factor *= 5 / 6
                    self.drawAnim()

            elif mark[1] == -1:  # down
                while (self.activePiece.anim[1] + mark[1] * mov > destination[1]):
                    self.activePiece.anim[1] += mark[1] * mov
                    if (mark[0] >= 0):
                        if delta[1] != 0:
                            self.activePiece.anim[0] += mark[0] * mov * delta[0] / delta[1]
                            akt_x = int(self.activePiece.anim[0] + mark[0] * distance * blockSize * delta[0] / delta[1])
                        else:
                            akt_x = self.activePiece.pos[0]
                        akt_y = int(math.ceil(self.activePiece.anim[1] + mark[1] * distance * blockSize))
                        #draw aside:
                        if ((s0 != [0, 0]) and (self.array[s0[0], s0[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s0[0], s0[1]].anim[0] - mov * 5 / 12 > self.array[s0[0], s0[1]].pos[
                                0] - 0.4) and (to1 == 1)):
                                self.array[s0[0], s0[1]].anim[0] -= mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] -= mov * 5 / 12
                            elif ((self.array[s0[0], s0[1]].anim[0] + mov * 5 / 12 < self.array[s0[0], s0[1]].pos[0]) and (
                                fro1 == 1)):
                                to1 = 0
                                self.array[s0[0], s0[1]].anim[0] += mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] += mov * 5 / 12
                            else:
                                fro1 = 0
                                self.array[s0[0], s0[1]].anim[0] = self.array[s0[0], s0[1]].pos[0]
                                self.array[s0[0], s0[1]].anim[1] = self.array[s0[0], s0[1]].pos[1]
                                self.array[s0[0], s0[1]].animate = 0
                        if ((s1 != [0, 0]) and (self.array[s1[0], s1[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s1[0], s1[1]].anim[0] + mov * 5 / 12 < self.array[s1[0], s1[1]].pos[
                                0] + 0.4) and (to2 == 1)):
                                self.array[s1[0], s1[1]].anim[0] += mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] += mov * 5 / 12
                            elif ((self.array[s1[0], s1[1]].anim[0] - mov * 5 / 12 > self.array[s1[0], s1[1]].pos[0]) and (
                                fro2 == 1)):
                                to2 = 0
                                self.array[s1[0], s1[1]].anim[0] -= mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] -= mov * 5 / 12
                            else:
                                fro2 = 0
                                self.array[s1[0], s1[1]].anim[0] = self.array[s1[0], s1[1]].pos[0]
                                self.array[s1[0], s1[1]].anim[1] = self.array[s1[0], s1[1]].pos[1]
                                self.array[s1[0], s1[1]].animate = 0

                    elif (mark[0] < 0):
                        if delta[1] != 0:
                            self.activePiece.anim[0] += mark[0] * mov * delta[0] / delta[1]
                            akt_x = int(self.activePiece.anim[0] + mark[0] * distance * blockSize * delta[0] / delta[1])
                        else:
                            akt_x = self.activePiece.pos[0]
                        akt_y = int(math.ceil(self.activePiece.anim[1] + mark[1] * distance * blockSize))
                        #self.drawAside:
                        if ((s0 != [0, 0]) and (self.array[s0[0], s0[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s0[0], s0[1]].anim[0] + mov * 5 / 12 < self.array[s0[0], s0[1]].pos[
                                0] + 0.4) and (to1 == 1)):
                                self.array[s0[0], s0[1]].anim[0] += mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] -= mov * 5 / 12
                            elif ((self.array[s0[0], s0[1]].anim[0] - mov * 5 / 12 > self.array[s0[0], s0[1]].pos[0]) and (
                                fro1 == 1)):
                                to1 = 0
                                self.array[s0[0], s0[1]].anim[0] -= mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] += mov * 5 / 12
                            else:
                                fro1 = 0
                                self.array[s0[0], s0[1]].anim[0] = self.array[s0[0], s0[1]].pos[0]
                                self.array[s0[0], s0[1]].anim[1] = self.array[s0[0], s0[1]].pos[1]
                                self.array[s0[0], s0[1]].animate = 0
                        if ((s1 != [0, 0]) and (self.array[s1[0], s1[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s1[0], s1[1]].anim[0] - mov * 5 / 12 > self.array[s1[0], s1[1]].pos[
                                0] - 0.4) and (to2 == 1)):
                                self.array[s1[0], s1[1]].anim[0] -= mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] += mov * 5 / 12
                            elif ((self.array[s1[0], s1[1]].anim[0] + mov * 5 / 12 < self.array[s1[0], s1[1]].pos[0]) and (
                                fro2 == 1)):
                                to2 = 0
                                self.array[s1[0], s1[1]].anim[0] += mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] -= mov * 5 / 12
                            else:
                                fro2 = 0
                                self.array[s1[0], s1[1]].anim[0] = self.array[s1[0], s1[1]].pos[0]
                                self.array[s1[0], s1[1]].anim[1] = self.array[s1[0], s1[1]].pos[1]
                                self.array[s1[0], s1[1]].animate = 0

                    #self.drawAside(self.activePiece,akt_x,akt_y,delta[0],delta[1],mark[0],mark[1],destination[0],destination[1])
                    #time.sleep(0.003)
                    if self.array[destination[0], destination[1]] != emptyPiece:
                        self.array[destination[0], destination[1]].factor *= 5 / 6
                    self.drawAnim()

        else:  # delta[1] < delta[0]
            if mark[0] == 1:  # to right
                while (self.activePiece.anim[0] + mark[0] * mov < destination[0]):
                    self.activePiece.anim[0] += mark[0] * mov
                    if (mark[1] >= 0):  # to right top
                        if delta[0] != 0:
                            self.activePiece.anim[1] += mark[1] * mov * delta[1] / delta[0]
                            akt_y = int(self.activePiece.anim[1] + mark[1] * distance * blockSize * delta[1] / delta[0])
                        else:
                            akt_y = self.activePiece.pos[1]
                        akt_x = int(self.activePiece.anim[0] + mark[0] * mark[1] * distance * blockSize)
                        #draw aside:
                        if ((s0 != [0, 0]) and (self.array[s0[0], s0[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s0[0], s0[1]].anim[0] + mov * 5 / 12 < self.array[s0[0], s0[1]].pos[
                                0] + 0.4) and (to1 == 1)):
                                self.array[s0[0], s0[1]].anim[0] += mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] -= mov * 5 / 12
                            elif ((self.array[s0[0], s0[1]].anim[0] - mov * 5 / 12 > self.array[s0[0], s0[1]].pos[0]) and (
                                fro1 == 1)):
                                to1 = 0
                                self.array[s0[0], s0[1]].anim[0] -= mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] += mov * 5 / 12
                            else:
                                fro1 = 0
                                self.array[s0[0], s0[1]].anim[0] = self.array[s0[0], s0[1]].pos[0]
                                self.array[s0[0], s0[1]].anim[1] = self.array[s0[0], s0[1]].pos[1]
                                self.array[s0[0], s0[1]].animate = 0
                        if ((s1 != [0, 0]) and (self.array[s1[0], s1[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s1[0], s1[1]].anim[0] - mov * 5 / 12 > self.array[s1[0], s1[1]].pos[
                                0] - 0.4) and (to2 == 1)):
                                self.array[s1[0], s1[1]].anim[0] -= mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] += mov * 5 / 12
                            elif ((self.array[s1[0], s1[1]].anim[0] + mov * 5 / 12 < self.array[s1[0], s1[1]].pos[0]) and (
                                fro2 == 1)):
                                to2 = 0
                                self.array[s1[0], s1[1]].anim[0] += mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] -= mov * 5 / 12
                            else:
                                fro2 = 0
                                self.array[s1[0], s1[1]].anim[0] = self.array[s1[0], s1[1]].pos[0]
                                self.array[s1[0], s1[1]].anim[1] = self.array[s1[0], s1[1]].pos[1]
                                self.array[s1[0], s1[1]].animate = 0

                    elif (mark[1] < 0):  # to right bottom
                        if delta[0] != 0:
                            self.activePiece.anim[1] += mark[1] * mov * delta[1] / delta[0]
                            akt_y = int(self.activePiece.anim[1] + mark[1] * distance * blockSize * delta[1] / delta[0])
                        else:
                            akt_y = self.activePiece.pos[1]
                        akt_x = int(self.activePiece.anim[0] + mark[0] * distance * blockSize)
                        #self.drawAside:
                        if ((s0 != [0, 0]) and (self.array[s0[0], s0[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s0[0], s0[1]].anim[0] + mov * 5 / 12 < self.array[s0[0], s0[1]].pos[
                                0] + 0.4) and (to1 == 1)):
                                self.array[s0[0], s0[1]].anim[0] += mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] += mov * 5 / 12
                            elif ((self.array[s0[0], s0[1]].anim[0] - mov * 5 / 12 > self.array[s0[0], s0[1]].pos[0]) and (
                                fro1 == 1)):
                                to1 = 0
                                self.array[s0[0], s0[1]].anim[0] -= mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] -= mov * 5 / 12
                            else:
                                fro1 = 0
                                self.array[s0[0], s0[1]].anim[0] = self.array[s0[0], s0[1]].pos[0]
                                self.array[s0[0], s0[1]].anim[1] = self.array[s0[0], s0[1]].pos[1]
                                self.array[s0[0], s0[1]].animate = 0
                        if ((s1 != [0, 0]) and (self.array[s1[0], s1[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s1[0], s1[1]].anim[0] - mov * 5 / 12 > self.array[s1[0], s1[1]].pos[
                                0] - 0.4) and (to2 == 1)):
                                self.array[s1[0], s1[1]].anim[0] -= mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] -= mov * 5 / 12
                            elif ((self.array[s1[0], s1[1]].anim[0] + mov * 5 / 12 < self.array[s1[0], s1[1]].pos[0]) and (
                                fro2 == 1)):
                                to2 = 0
                                self.array[s1[0], s1[1]].anim[0] += mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] += mov * 5 / 12
                            else:
                                fro2 = 0
                                self.array[s1[0], s1[1]].anim[0] = self.array[s1[0], s1[1]].pos[0]
                                self.array[s1[0], s1[1]].anim[1] = self.array[s1[0], s1[1]].pos[1]
                                self.array[s1[0], s1[1]].animate = 0


                    #self.drawAside(self.activePiece,akt_x,akt_y,delta[0],delta[1],mark[0],mark[1],destination[0],destination[1])
                    #time.sleep(0.003)
                    if self.array[destination[0], destination[1]] != emptyPiece:
                        self.array[destination[0], destination[1]].factor *= 5 / 6
                    self.drawAnim()

            elif mark[0] == -1:  # to left
                while (self.activePiece.anim[0] + mark[0] * mov > destination[0]):
                    self.activePiece.anim[0] += mark[0] * mov
                    if (mark[1] >= 0):  # to left top
                        if delta[0] != 0:
                            self.activePiece.anim[1] += mark[1] * mov * delta[1] / delta[0]
                            akt_y = int(self.activePiece.anim[1] + mark[1] * distance * blockSize * delta[1] / delta[0])
                        else:
                            akt_y = self.activePiece.pos[1]
                        akt_x = int(self.activePiece.anim[0] + mark[0] * distance * blockSize)
                        # draw aside
                        if ((s0 != [0, 0]) and (self.array[s0[0], s0[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s0[0], s0[1]].anim[0] - mov * 5 / 12 > self.array[s0[0], s0[1]].pos[
                                0] - 0.4) and (to1 == 1)):
                                self.array[s0[0], s0[1]].anim[0] -= mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] -= mov * 5 / 12
                            elif ((self.array[s0[0], s0[1]].anim[0] + mov * 5 / 12 < self.array[s0[0], s0[1]].pos[0]) and (
                                fro1 == 1)):
                                to1 = 0
                                self.array[s0[0], s0[1]].anim[0] += mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] += mov * 5 / 12
                            else:
                                fro1 = 0
                                self.array[s0[0], s0[1]].anim[0] = self.array[s0[0], s0[1]].pos[0]
                                self.array[s0[0], s0[1]].anim[1] = self.array[s0[0], s0[1]].pos[1]
                                self.array[s0[0], s0[1]].animate = 0
                        if ((s1 != [0, 0]) and (self.array[s1[0], s1[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s1[0], s1[1]].anim[0] + mov * 5 / 12 < self.array[s1[0], s1[1]].pos[
                                0] + 0.4) and (to2 == 1)):
                                self.array[s1[0], s1[1]].anim[0] += mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] += mov * 5 / 12
                            elif ((self.array[s1[0], s1[1]].anim[0] - mov * 5 / 12 > self.array[s1[0], s1[1]].pos[0]) and (
                                fro2 == 1)):
                                to2 = 0
                                self.array[s1[0], s1[1]].anim[0] -= mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] -= mov * 5 / 12
                            else:
                                fro2 = 0
                                self.array[s1[0], s1[1]].anim[0] = self.array[s1[0], s1[1]].pos[0]
                                self.array[s1[0], s1[1]].anim[1] = self.array[s1[0], s1[1]].pos[1]
                                self.array[s1[0], s1[1]].animate = 0
                    elif (mark[1] < 0):  # to left top
                        if delta[0] != 0:
                            self.activePiece.anim[1] += mark[1] * mov * delta[1] / delta[0]
                            akt_y = int(self.activePiece.anim[1] + mark[1] * distance * blockSize * delta[1] / delta[0])
                        else:
                            akt_y = self.activePiece.pos[1]
                        akt_x = int(self.activePiece.anim[0] + mark[0] * distance * blockSize)
                        #draw aside:
                        if ((s0 != [0, 0]) and (self.array[s0[0], s0[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s0[0], s0[1]].anim[0] - mov * 5 / 12 > self.array[s0[0], s0[1]].pos[
                                0] - 0.4) and (to1 == 1)):
                                self.array[s0[0], s0[1]].anim[0] -= mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] += mov * 5 / 12
                            elif ((self.array[s0[0], s0[1]].anim[0] + mov * 5 / 12 < self.array[s0[0], s0[1]].pos[0]) and (
                                fro1 == 1)):
                                to1 = 0
                                self.array[s0[0], s0[1]].anim[0] += mov * 5 / 12
                                self.array[s0[0], s0[1]].anim[1] -= mov * 5 / 12
                            else:
                                fro1 = 0
                                self.array[s0[0], s0[1]].anim[0] = self.array[s0[0], s0[1]].pos[0]
                                self.array[s0[0], s0[1]].anim[1] = self.array[s0[0], s0[1]].pos[1]
                                self.array[s0[0], s0[1]].animate = 0
                        if ((s1 != [0, 0]) and (self.array[s1[0], s1[1]] != emptyPiece)):
                            #s0 to left*mark[0], s1 to right*mark[0]
                            if ((self.array[s1[0], s1[1]].anim[0] + mov * 5 / 12 < self.array[s1[0], s1[1]].pos[
                                0] + 0.4) and (to2 == 1)):
                                self.array[s1[0], s1[1]].anim[0] += mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] -= mov * 5 / 12
                            elif ((self.array[s1[0], s1[1]].anim[0] - mov * 5 / 12 > self.array[s1[0], s1[1]].pos[0]) and (
                                fro2 == 1)):
                                to2 = 0
                                self.array[s1[0], s1[1]].anim[0] -= mov * 5 / 12
                                self.array[s1[0], s1[1]].anim[1] += mov * 5 / 12
                            else:
                                fro2 = 0
                                self.array[s1[0], s1[1]].anim[0] = self.array[s1[0], s1[1]].pos[0]
                                self.array[s1[0], s1[1]].anim[1] = self.array[s1[0], s1[1]].pos[1]
                                self.array[s1[0], s1[1]].animate = 0

                    #self.drawAside(akt_Figur,akt_x,akt_y,delta[0],delta[1],mark[0],mark[1],destination[0],destination[1])
                    #time.sleep(0.003)
                    if self.array[destination[0], destination[1]] != emptyPiece:
                        self.array[destination[0], destination[1]].factor *= 5 / 6
                    self.drawAnim()

        self.activePiece.pos[0] = destination[0]
        self.activePiece.pos[1] = destination[1]
        self.activePiece.anim[0] = destination[0]
        self.activePiece.anim[1] = destination[1]
        self.activePiece.animate = 0

        if self.array[destination[0], destination[1]] != emptyPiece:
            self.array[destination[0], destination[1]].kill()
            self.array[destination[0], destination[1]] = emptyPiece
        self.array[destination[0], destination[1]] = self.activePiece
        self.drawAnim()


    def checkForPieceChange(self, x, y):
        self.pieceChange = false
        if (self.activePiece != None):
            if (self.activePiece.type == pawn):
                color = self.activePiece.color
                if (((color == white) and (y == 8)) or ((color == black) and (y == 1))):
                    self.pieceChange = true


    def removeMarkings(self):
        self.chosenBlock = [-1, -1]
        self.clickedCoordinates = [-10.0, -10.0, -10.0]
        self.mouse = [-1.0, -1.0]
        self.activePiece = None
        self.possibleMoves = []


    def changePawnPiece(self, i):
        color = self.activePiece.color
        x = self.activePiece.pos[0]
        y = self.activePiece.pos[1]
        if (i == -1):
            self.queens.append(Queen.Queen(color, x, y, false))
            self.array[x, y].kill()
            self.array[x, y] = self.queens[(len(self.queens) - 1)]
            self.removeMarkings()
            self.pieceChange = false
            self.toggleTurn()
            self.checkForCheck()
        elif (i == 0):
            self.bishops.append(Bishop.Bishop(color, x, y))
            self.array[x, y].kill()
            self.array[x, y] = self.bishops[(len(self.bishops) - 1)]
            self.removeMarkings()
            self.pieceChange = false
            self.toggleTurn()
            self.checkForCheck()
        elif (i == 1):
            self.knights.append(Knight.Knight(color, x, y))
            self.array[x, y].kill()
            self.array[x, y] = self.knights[(len(self.knights) - 1)]
            self.removeMarkings()
            self.pieceChange = false
            self.toggleTurn()
            self.checkForCheck()
        elif (i == 2):
            self.rooks.append(Rook.Rook(color, x, y))
            self.array[x, y].kill()
            self.array[x, y] = self.rooks[(len(self.rooks) - 1)]
            self.removeMarkings()
            self.pieceChange = false
            self.toggleTurn()
            self.checkForCheck()

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


    def myKing(self):
        if (self.kings[0].color == self.turn):
            return self.kings[0]
        else:
            return self.kings[1]


    def isCheckMate(self):
        if (self.isInCheck() == false):
            return false
        itsKing = self.myKing()

        # check all figures of own color for possible moves:
        if (itsKing.safeMoves(self.array) != []):
            return false
        for i in range(0, len(self.pawns)):
            if (self.pawns[i].color == self.turn):
                if (self.pawns[i].moves(self.array) != []):
                    return false
        for i in range(0, len(self.rooks)):
            if (self.rooks[i].color == self.turn):
                if (self.rooks[i].moves(self.array) != []):
                    return false
        for i in range(0, len(self.knights)):
            if (self.knights[i].color == self.turn):
                if (self.knights[i].moves(self.array) != []):
                    return false
        for i in range(0, len(self.bishops)):
            if (self.bishops[i].color == self.turn):
                if (self.bishops[i].moves(self.array) != []):
                    return false
        for i in range(0, len(self.queens)):
            if (self.queens[i].color == self.turn):
                if (self.queens[i].moves(self.array) != []):
                    return false

        return true


    def isInCheck(self):
        itsKing = self.myKing()
        if (itsKing.threat(itsKing.pos[0], itsKing.pos[1], self.array) == threatened):
            # print ("in check")
            return true
        else:
            return false

    def setMove(self, move):
        abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        oldX = abc.index(move[0]) + 1
        oldY = int(move[1])
        newX = abc.index(move[2]) + 1
        newY = int(move[3])
        print move
        print oldX
        print oldY
        print newX
        print newY

        self.activePiece = self.array[oldX, oldY]

        # only turkis color is enabled if
        self.turn = 30
        self.activePiece.pos[0] = newX
        self.activePiece.pos[1] = newY
        if self.array[newX, newY] != emptyPiece:
            self.array[newX, newY].kill()
        self.array[newX, newY] = self.activePiece

    # TODO: check out how to handle a click
    def handleClick(self):
        return ""
        curMove = ""
        if (self.pieceChange):
            if (self.activePiece != None):
                color = self.activePiece.color
                x = self.activePiece.pos[0]
                y = self.activePiece.pos[1]
                print "X = " + x + " Y = " + y
                if (color == white):
                    yAdd = 1
                else:
                    yAdd = -1
                for i in range(-1, 3):
                    if (( self.clickedCoordinates[0] > ((-4 + x + i - 1) * blockSize) ) and (
                        self.clickedCoordinates[1] > ((-4 + y + yAdd - 1) * blockSize) ) \
                                and ( self.clickedCoordinates[0] < ((-4 + x + i) * blockSize) ) and (
                        self.clickedCoordinates[1] < ((-4 + y + yAdd) * blockSize) ) ):
                        self.changePawnPiece(i)
        else:
            for i in range(0, 8):
                for j in range(0, 8):
                    if (( self.clickedCoordinates[0] > ((-4 + i) * blockSize) ) and (
                        self.clickedCoordinates[1] > ((-4 + j) * blockSize) ) \
                                and ( self.clickedCoordinates[0] < ((-4 + i + 1) * blockSize) ) and (
                        self.clickedCoordinates[1] < ((-4 + j + 1) * blockSize) ) ):
                        # if not yet chose a piece
                        if ((self.activePiece == None) and (self.checkmate == false)):
                            self.checkmate = false
                            if ((self.array[i + 1, j + 1] != emptyPiece) and (
                                self.array[i + 1, j + 1].color == self.turn)):  # and (self.chosenBlock == [-1,-1])):
                                self.chosenBlock = [i + 1, j + 1]
                                self.activePiece = self.array[i + 1, j + 1]
                                if (self.activePiece.type == king):
                                    self.possibleMoves = self.activePiece.safeMoves(self.array)
                                else:
                                    self.possibleMoves = self.activePiece.moves(self.array)
                        # if already chosed a piece
                        elif (self.checkmate == false):
                            self.checkmate = false
                            #if this chosen piece was selected:
                            if ((i + 1 == self.activePiece.pos[0]) and (j + 1 == self.activePiece.pos[1])):
                                #remove marking:
                                self.clickedCoordinates = [-10, -10, -10]
                                self.mouse = [-1.0, -1.0]
                                self.chosenBlock = [-1, -1]
                                self.activePiece = None
                                self.possibleMoves = []
                            elif ((i + 1 == self.activePiece.pos[0]) and (j + 1 == self.activePiece.pos[1])):
                                # do nothing:
                                nothing = 0
                            #if a possible move of the active piece was selected
                            elif ((i + 1, j + 1) in self.possibleMoves):
                                # castling:
                                self.doingCastling = false
                                if (self.activePiece.type == king):
                                    if ((self.activePiece.pos[0] - (i + 1) == 2) or (
                                            self.activePiece.pos[0] - (i + 1) == -2)):
                                        self.doingCastling = true
                                        # print ("castling")
                                    else:
                                        self.doingCastling = false
                                else:
                                    self.doingCastling = false
                                    self.checkForPieceChange(i + 1, j + 1)
                                #move:
                                if self.doAnimation == 1:
                                    self.animationMode = 1
                                    self.move(i + 1, j + 1, self.doingCastling)
                                    self.animationMode = 0
                                else:

                                    self.array[self.activePiece.pos[0], self.activePiece.pos[1]] = emptyPiece
                                    # move:
                                    abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
                                    oldX = abc[self.activePiece.pos[0] - 1]
                                    oldY = self.activePiece.pos[1]
                                    newX = abc[(i + 1) - 1]
                                    newY = (j + 1)
                                    curMove = oldX + str(oldY) + newX + str(newY)
                                    print "Move = %s%d%s%d" % (oldX, oldY, newX, newY)

                                    self.activePiece.pos[0] = i + 1
                                    self.activePiece.pos[1] = j + 1
                                    if self.array[i + 1, j + 1] != emptyPiece:
                                        self.array[i + 1, j + 1].kill()
                                    self.array[i + 1, j + 1] = self.activePiece

                                    if (self.doingCastling == true):
                                        # move rook:
                                        if (i + 1 == 7):
                                            self.array[i + 2, j + 1].pos[0] = i
                                            self.array[i, j + 1] = self.array[i + 2, j + 1]
                                            self.array[i + 2, j + 1] = emptyPiece
                                        elif (i + 1 == 3):
                                            self.array[i - 1, j + 1].pos[0] = i + 2
                                            self.array[i + 2, j + 1] = self.array[i - 1, j + 1]
                                            self.array[i - 1, j + 1] = emptyPiece

                                if (self.pieceChange == true):
                                    self.chosenBlock = [i + 1, j + 1]
                                if (self.activePiece != None):
                                    self.activePiece.moved = true

                                if (self.pieceChange == false):
                                    self.toggleTurn()

                                    #remove markings:
                                    self.chosenBlock = [-1, -1]
                                    self.clickedCoordinates = [-10, -10, -10]
                                    self.mouse = [-1.0, -1.0]
                                    self.activePiece = None
                                    self.checkForCheck()

                                self.possibleMoves = []

                            #choose new piece:
                            elif ((self.array[i + 1, j + 1] != emptyPiece) and (
                                self.array[i + 1, j + 1].color == self.turn)):  #and (self.chosenBlock == [-1,-1])):
                                self.chosenBlock = [i + 1, j + 1]
                                self.activePiece = self.array[i + 1, j + 1]
                                if (self.activePiece.type == king):
                                    self.possibleMoves = self.activePiece.safeMoves(self.array)
                                else:
                                    self.possibleMoves = self.activePiece.moves(self.array)
        return curMove

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

    def drawBorder(self):

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


    def start(self):
        argv = glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL)  # GLUT_ALPHA missing
        glutInitWindowPosition(20, 20)
        glutInitWindowSize(600, 500)
        glutCreateWindow("Augmented Reality Chess")

        glutDisplayFunc(self.redraw)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.key_pressed)
        glutMotionFunc(self.mouse_moved)
        glutMouseFunc(self.mouse_pressed)

        glutCreateMenu(self.processMenuEvents)
        glutAddMenuEntry("toggle animation mode", 0)
        glutAddMenuEntry("toggle shadow mode", 1)
        glutAddMenuEntry("undo", 2)
        glutAddMenuEntry("Quit", 3)
        glutAttachMenu(GLUT_MIDDLE_BUTTON)

        self.init(600, 500)

        glutMainLoop()
