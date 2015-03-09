/** @file AugmentedReality.cpp
* @author Yarrago
* @note Website: http://yarrago.com
* @note Copyright © Yarrago 2011
* @version 1.0.2
* @date Created: 19/04/2011
* @date Modified: 10/08/2011
* @brief Augmented Reality program.
* 
* Please feel free to use this program, but please retain the copyright and licence information.
* TODO More info here.
* TODO, Include licence information here.
* Introduction to computer vision.
*
*
*
*
*
* License: "Modified BSD License" 3-clause license.
* 
* Copyright (c) 2011, Yarrago (yarrago.com)
* All rights reserved.
* 
* Redistribution and use in source and binary forms, with or without modification, are 
* permitted provided that the following conditions are met:
*   - Redistributions of source code must retain the above copyright notice, this list of 
*     conditions and the following disclaimer.
*   - Redistributions in binary form must reproduce the above copyright notice, this list of 
*     conditions and the following disclaimer in the documentation and/or other materials provided
*     with the distribution.
*   - Neither the name of the yarrago.com nor the names of its contributors may be used to endorse
*     or promote products derived from this software without specific prior written permission.
*   
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR 
* IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
* FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
* CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
* SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
* THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
* OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
* POSSIBILITY OF SUCH DAMAGE.
*/

#include "AugmentedReality.hpp"

using namespace std;
using namespace cv;

#ifndef WIN32
	const int nullptr = 0;
#endif



// Constant declarations
const int cameraId = 1;	// CV_ANY;	// The camera number to use (use CV_ANY to pick the default camera).

const int width = 640;				// Width of the frame in pixels.
const int height = 480;				// Height of the frame in pixels.
const float cameraFovy = 60.0;		// When using just the basic OpenGL camera need to set the field of view in the y dimension. 
const float zNear = 0.1;			// Distance to the OpenGL near clipping plane.
const float zFar = 1000.0;			// Distance to the OpenGL far clipping plane.

const float chessBoardScale = 1.0;	// Defines the scale of the virtual world realative to the size of a chess board square (i.e. 1 = a square = 1 virtual world measurement unit, 10 = a square = 10 virtual world measurement units).
const int chessCornersX = 9;		// Number of inner corners on the chessboard in the X dimension (number of chess board squares -1).
const int chessCornersY = 4;		// Number of inner corners on the chessboard in the Y dimension (number of chess board squares -1).

const int captureWidth = width;											// The width to capture images at from the webcam (the height will automatically be determined using the correct aspect ratio for the camera).
const string outputWindowName = "Augmented Reality - Output";			// The title for the output window.
const DisplayMethod displayMethod = DisplayMethod_GLUT;					// The display method to use for rendering the augmentation.

const int minimumMatchingPoints = 20;	// The minimum number of matching points that we must have after RANSAC matching to consider the homography valid.

const int findCornerFlags = CV_CALIB_CB_ADAPTIVE_THRESH | CV_CALIB_CB_FAST_CHECK;	// The flags to pass to findChessboardCorners().

const float selectionAspect = 1.5;			// The aspect ration to use when computing the homography.

const string calibrationImageFilenameBase = "CalibrationImage #.png";	// The filename to use when saving / loading the calibration images.
const string calibrationImageSequence = "#";							// The substring that represents the sequence number in the calibration image filename.
const int calibrationImageSequenceStart = 1;							// The first sequence number to use when saving / loading calibration images.

const string overlayImageFilename = "Overlay Image.png";				// The image to overlay into the basic augmentations.
const string saveHeldImageFilename = "Marker 0.png";					//



// State variables.
int augmentationMethod = 1;			// Number representing which augmentation method should be used.
const bool displayStats = true;		// Whether to display the stats in the console.

Mat heldImage;						// The program is capable of storing a single image for further use.
bool useHeldImage = false;			// Whether to use the last held image as the live image when grabFrame() is called.
bool holdImage = false;				// Whether to update the heldImage with the last image when grabFrame() is next called.
bool subPixelAccuracy = false;		// Whether to use sub pixel accuracy when finding corners.

vector<Mat> calibrationImages;			// A list containing all of the calibration images.
Mat calibrationMatrix;					// The cameras calibration matrix once calibrate() has been called.
Mat calibrationDistortionCoefficients;	// The cameras distortion coefficients once calibrate has been called.

SelectionMode selectionMode = SelectionMode_Region;	// The mode to use for selection.
vector<Point2f> selectionPoints;					// Selection points that the user has selected when cropping the marker image.
bool selectionRegionValid = false;					// Whether the selection region is set or not.

float naturalMarkerScale = 50.0;								// The scale to convert between image coordinates (pixels) and world coordinates (similar to chessBoardScale).
string naturalMarkerImageFilename = "Marker 1.png";				// The image that we want to find as a natural marker.


bool forceStaticTeapot = true;







/**
* @brief This function allows me to automate a few steps when the application is loaded.
*
* The contents of this function can be changed and used to quickly put the application
* into a different initial state, which is handy when debugging a particular mode.
*/
void debugInit()
{
	loadCalibrationImages();
	calibrate();

	augmentationMethod = 0;
}

/**
* @brief Uses OpenCV and OpenGL to obtain capture an image and augment it with virtual objects.
* @param args The number of command line arguments.
* @param argv The command line arguments (Not used).
* @return The success or failure of the program.
*/
int main(int args, char** argv)
{
	debugInit();

	if (displayMethod == DisplayMethod_OPEN_CV)
	{
		namedWindow(outputWindowName, CV_WINDOW_AUTOSIZE);

		for (;;)
		{
			Mat image = grabFrame();
			AugmentationInformation augmentedImage = processFrame(augmentationMethod, image);
			displayOpenCV(augmentedImage.liveImage);

			int key = cvWaitKey(10);
			if (key > 0)
			{
				if (keypress((unsigned char)key, 0, 0))
				{
					break;
				}
			}
		}
	}

	if (displayMethod == DisplayMethod_GLUT)
	{
		initialiseGLUT();
		
		glutMainLoop();
	}

	return 0;
}

/**
* @brief Gets a frame from the camera.
* @param flushBuffer Flushes the input buffer which is required on Linux (and maybe windows) when the camera gets behind.
* @param lastFrame Used to indicate that this will be the last frame we will get so we can close the capture stream.
* @return The image captured.
*
* This function will also updates the heldImage or returns the heldImage depending on the state of useHeldImage and holdImage.
*/ 
cv::Mat grabFrame(bool flushBuffer, bool lastFrame)
{	
	const int bufferLength = 5;

	static int framesCaptured = 0;					// Keep a count of how many frames we have captured.
	static VideoCapture video(cameraId);			// Open the video capture device.
	Mat rawCapturedImage;

	if (framesCaptured == 0)
	{
		// Set the width so that the camera captures at the specified resolution.
		video.set(CV_CAP_PROP_FRAME_WIDTH, captureWidth);											
	}

	// Should we use the held frame we captured instead of the live image?
	if (useHeldImage)																				
	{
		heldImage.copyTo(rawCapturedImage);
	}
	else
	{
		if (flushBuffer)
		{
			// Read all images out of the buffer except the last one to flush the buffer (we will read the last one when we grab the frame like normal).
			for(int i = 0; i < (bufferLength-1); i++)												
			{
				// Capture an image from the webcam.
				video >> rawCapturedImage;															
			}
		}
	
		// Capture an image from the webcam.
		video >> rawCapturedImage;																	
		framesCaptured++;

		// Do we want to hold the image for later use as a static image.
		if (holdImage)																				
		{
			rawCapturedImage.copyTo(heldImage);
			holdImage = false;
		}
	}

	if (lastFrame)
	{
		// TODO: Close the capture device.
	}

	return rawCapturedImage;
}

/**
* @brief This function multiplexes between the augmentation methods.
* @param method The augmentation method to use.
* @param image The image that we wamt to process.
* @return The augmented image information.
*
* That is it performs the augmentation specified by the method.
*/
AugmentationInformation processFrame(int method, cv::Mat rawCapturedImage)
{
	AugmentationInformation result;

	clock_t startTime = clock();	

	switch (method)
	{
	case 0:	// Do Nothing
		result = augmentationDoNothing(rawCapturedImage);
		break;
	case 1: // Find And Display Chess Corners
		result = augmentationChessPlanar(rawCapturedImage, subPixelAccuracy, false);
		break;
	case 2: // Augment Planar Image On Chessboard.
		result = augmentationChessPlanar(rawCapturedImage, subPixelAccuracy, true);
		break;
	case 3: // Augment Planar Image On Chessboard Surface.
		result = augmentationChessSurface(rawCapturedImage, subPixelAccuracy, true);
		break;
	case 4: // Show Calibration Images In Sequence.
		result = augmentationCalibrationImages(1.0);
		break;
	case 5: // Show 3D Figure On Chessboard.
		result = augmentationChess3D(rawCapturedImage, subPixelAccuracy);
		break;
	case 6: // Allow the user to select the marker (Old Show Rectified Image).
		//result = augmentationUndistort(rawCapturedImage);
		result = augmentationCaptureMarker(rawCapturedImage);
		break;
	case 7: // Show SIFT Features.
		result = augmentationNaturalMarkers1(rawCapturedImage, true, false, false);
		break;
	case 8: // Show SIFT Feature Mapping / Ransac.
		result = augmentationNaturalMarkers1(rawCapturedImage, false, false, true);
		break;
	case 9: // Show 3D Augmentation With Natural Planar Image.
		result = augmentationNaturalMarkers1(rawCapturedImage, false, false, false);
		break;
	}
	
	if (displayStats)
	{
		cout << "Max FPS (Based on augmentation processing): " << 1.0/(difftime(clock(), startTime)/CLOCKS_PER_SEC) << "\n";
		cout << "Augmentation processing time: " << difftime(clock(), startTime)/CLOCKS_PER_SEC << "\n";
	}

	return result;
}

/**
* @brief Initialises GLUT.
*
* Creates a window and sets up the necessary state vairables.
* This function indirectally initialises the OpenGL state variables.
*/
void initialiseGLUT()
{
	int args = 0;

	glutInit(&args, 0);
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA);
	glutInitWindowSize(width, height);
	glutCreateWindow(outputWindowName.c_str());

	initialiseOpenGL();

	glutDisplayFunc(displayGLUT);
	glutKeyboardFunc(keyboardGLUT);
	glutMouseFunc(mouseGLUT);
	glutMotionFunc(mouseMotionGLUT);
}

/**
* @brief Initialises OpenGL.
*
* This function initialises the OpenGL state variables.
*/
void initialiseOpenGL()
{
	glClearColor(0.0, 0.0, 0.0, 1.0);

	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();		
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();		

	glShadeModel(GL_SMOOTH);
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_LIGHTING);
	glEnable(GL_NORMALIZE);
	
	//glEnable(GL_CULL_FACE);
	//glCullFace(GL_FRONT);
	
	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

	// Initialise Texture States
	 glPixelStorei(GL_UNPACK_ALIGNMENT, 1);

	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE);
	//glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
	//glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND);
		
	//glPolygonMode(GL_FRONT, GL_LINE);
	//glPolygonMode(GL_BACK, GL_LINE);
}

/**
* @brief This is the GLUT drawing function.
*
* This function grabs a frame from the camera, augments it using the current augmentation method and then
* renders it to the GLUT window using OpenGL.
*
* This function is designed to work with double buffering.
* This function currently invalidates the framebuffer so that a new frame is begun to be
* drawing imeidatly after this frame completes.
*/
void displayGLUT()
{
	static int frames = 0;					// Keep a count of how many frames we've rendered.
	static const int fpsDuration = 3;		// The number of seconds to average the frame count over.
	static queue<clock_t> fps;				// Buffer to hold the number of frames we've rendered in the last period.
	// static clock_t startime = clock();

	// Grab the image from the real camera.
	Mat rawImage = grabFrame();
	AugmentationInformation augmentation = processFrame(augmentationMethod, rawImage);

	// Clear the last image.
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);									
	
	// Render the image that we grabed from the camera.
	renderBackgroundGL(augmentation.liveImage);											

	// If we are using the selection mode display the selection markers.
	if(augmentation.augmentationMode == AugmentationMode_SELECTION)
	{
		drawSelection();
	}

	if(augmentation.augmentationMode == AugmentationMode_3D)
	{
		/*
		glMatrixMode(GL_PROJECTION);
		glLoadIdentity();
		gluPerspective(cameraFovy, (GLfloat) width / (GLfloat) height, zNear, zFar);
	
		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity();
		gluLookAt(0.0, 0.0, -10.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0);
		// */

		// Load the projection and modelview matricies that we obtained from the augmentation method.
		// /*
		glMatrixMode(GL_PROJECTION);	
		GLfloat* projection = convertMatrixType(augmentation.projection);
		glLoadMatrixf(projection);
		delete[] projection;

		glMatrixMode(GL_MODELVIEW);
		GLfloat* modelview = convertMatrixType(augmentation.modelview);
		glLoadMatrixf(modelview);
		delete[] modelview;
		// */



		// Create a light, defining the light in this way means that it will stay with the camera.
		GLenum lightSource = GL_LIGHT0;
		float ambientLight[4] = {1.0, 1.0, 1.0, 1.0};
		float diffuseLight[4] = {1.0, 1.0, 1.0, 1.0};
		float specularLight[4] = {1.0, 1.0, 1.0, 1.0};
		const float lightPosition[4] = {0.0, 0.0, 1.0, 1.0};
	
		glEnable(lightSource);
		glLightfv(lightSource, GL_AMBIENT, ambientLight);
		glLightfv(lightSource, GL_DIFFUSE, diffuseLight);
		glLightfv(lightSource, GL_SPECULAR, specularLight);

		glPushMatrix();
			glLoadIdentity();
			glLightfv(lightSource, GL_POSITION, lightPosition);
		glPopMatrix();

		// Render the 3D objects into the scene.
		renderSceneGL(augmentation.augmentationModel);
	}

	// Draw the number of FPS onto the image.
	drawFPS(-1);

	// Tell OpenGL we have finished drawing.
	glFlush();
	
	// Operating in double buffered mode, swap the buffers.
	glutSwapBuffers();
	
	// Increment the frame count.
	frames++;

	/* Save renderings as a sequence of image files.
	static Mat renderImage(Size(width, height), CV_8UC3);
	glReadPixels(0, 0, renderImage.size().width, renderImage.size().height,  GL_BGR_EXT, GL_UNSIGNED_BYTE, renderImage.data);

	string filename = "Render Image " + intToString(frames) + ".png";
	imwrite(filename, renderImage);
	// */

	// Draw a new frame immediately.
	glutPostRedisplay();

	// Keep a buffered count of the number of frames per second over the last few seconds 
	// (so it is averaged and doesn't bounce all over the place).
	fps.push(clock());
	while ((!fps.empty()) && (difftime(clock(),fps.front())/CLOCKS_PER_SEC > fpsDuration))
	{
		fps.pop();
	}

	//cout << "FPS: " << float(frames)/(difftime(clock(), time)/CLOCKS_PER_SEC) << "\n";
	cout << "FPS: " << float(fps.size())/fpsDuration << "\n";
}

/**
* @brief This is the OpenCV drawing method.
* @param augmentedImage The image that is to be rendered to the screen.
*
* This function is only capable of drawing the image passed to it and no special options are supported.
*/
void displayOpenCV(cv::Mat augmentedImage)
{
	// Display the augmented image.
	imshow(outputWindowName, augmentedImage);
}

/**
* @brief Draws the basic image background image.
* @param image The image to render.
*/
void renderBackgroundGL(const cv::Mat& image)
{
	// Make sure that the polygon mode is set so we draw the polygons filled
	// (save the state first so we can restore it).
	GLint polygonMode[2];
	glGetIntegerv(GL_POLYGON_MODE, polygonMode);
	glPolygonMode(GL_FRONT, GL_FILL);
	glPolygonMode(GL_BACK, GL_FILL);

	// Set up the virtual camera, projecting using simple ortho so we can draw the background image.
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluOrtho2D(0.0, 1.0, 0.0, 1.0);
	
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	
	// Create a texture (on the first pass only, we will reuse it later) to hold the image we captured.
	static bool textureGenerated = false;
	static GLuint textureId;
	if (!textureGenerated)
	{
		glGenTextures(1, &textureId);

		glBindTexture(GL_TEXTURE_2D, textureId);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

		textureGenerated = true;
	}
	
	// Copy the image to the texture.
	glBindTexture(GL_TEXTURE_2D, textureId);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.size().width, image.size().height, 0, GL_BGR_EXT, GL_UNSIGNED_BYTE, image.data);
	
	// Draw the image.
	glEnable(GL_TEXTURE_2D);
	glBegin(GL_TRIANGLES);
		glNormal3f(0.0, 0.0, 1.0);
		
		glTexCoord2f(0.0, 1.0);
		glVertex3f(0.0, 0.0, 0.0);
		glTexCoord2f(0.0, 0.0);
		glVertex3f(0.0, 1.0, 0.0);
		glTexCoord2f(1.0, 1.0);
		glVertex3f(1.0, 0.0, 0.0);
		
		glTexCoord2f(1.0, 1.0);
		glVertex3f(1.0, 0.0, 0.0);
		glTexCoord2f(0.0, 0.0);
		glVertex3f(0.0, 1.0, 0.0);
		glTexCoord2f(1.0, 0.0);
		glVertex3f(1.0, 1.0, 0.0);
	glEnd();
	glDisable(GL_TEXTURE_2D);

	// Clear the depth buffer so the texture forms the background.
	glClear(GL_DEPTH_BUFFER_BIT);

	// Restore the polygon mode state.
	glPolygonMode(GL_FRONT, polygonMode[0]);
	glPolygonMode(GL_BACK, polygonMode[1]);
}

/**
* @brief Draws the FPS onto the image.
* @param fps The number of FPS.
*
* Note: This function requres the inclusion of freeglut instead of just glut.
*/
void drawFPS(float fps)
{
	if (fps >= 0)
	{
		// Save the state of GL lighting.
		GLboolean lighting = glIsEnabled(GL_LIGHTING);

		// Clear the depth buffer so we can write over the texture.
		glClear(GL_DEPTH_BUFFER_BIT);
	
		// Draw the number of FPS.
		glDisable(GL_LIGHTING);
		glColor3f(1.0, 1.0, 1.0);
		glRasterPos2f(0.01, 0.97);
		string frameRate = "FPS: " + intToString(fps);
		//glutBitmapString(GLUT_BITMAP_9_BY_15, (const unsigned char*)frameRate.c_str());

		if (lighting)
		{
			glEnable(GL_LIGHTING);
		}
	}
}

/**
* @brief Draws the 3D augmentation model using OpenGL.
* @param m The model to draw.
*/
void renderSceneGL(AugmentationModel m)
{
	if (forceStaticTeapot)
	{
		m = AugmentationModel_Teapot_Static;
	}

	switch (m)
	{
	case AugmentationModel_Teapot_Static:
		drawStaticTeapotGL();
		break;
	case AugmentationModel_Teapot_Dynamic:
		drawDynamicTeapotGL();
		break;
	case AugmentationModel_Tower_Static:
		drawStaticTowerGL();
		break;
	}

}

/**
* @brief Draws a teapot.
*/
void drawStaticTeapotGL()
{
	// Set the colour for all new objects.
	glColor3f(1.0, 0.0, 0.5);
	
	// The material properties for the teapot.
	float teapotAlpha = 1.0;
	float ambientTeapot[4]  = {1.0, 0.0, 0.0, teapotAlpha};
	float diffuseTeapot[4]  = {1.0, 0.0, 0.0, teapotAlpha};
	float specularTeapot[4] = {1.0, 1.0, 0.0, teapotAlpha};
	float shininessTeapot = 1;

	glMaterialfv(GL_FRONT, GL_AMBIENT, ambientTeapot);
	glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuseTeapot);
	glMaterialfv(GL_FRONT, GL_SPECULAR, specularTeapot);
	glMaterialf(GL_FRONT, GL_SHININESS, shininessTeapot);

	// Draw the teapot.
	glPushMatrix();
		glRotatef(90, -1.0, 0.0, 0.0);
		glutSolidTeapot(1.0);
	glPopMatrix();
}

/**
* @brief Draws a teapot that has a bit of movment.
*
* It grows the teapot into the scene and then spins it around.
*/
void drawDynamicTeapotGL()
{
	static const float animationTimeout = 0.5;		// Timeout in seconds.
	static const float animationIntroDuration = 1.0;	// Total time for the animation
	
	static clock_t startTime = clock();
	static clock_t lastTime = clock();

	if (difftime(clock(), lastTime)/CLOCKS_PER_SEC > animationTimeout)
	{
		startTime = clock();
	}

	for(int i = -1; i <= 1; i++)
	{
		glPushMatrix();
			glTranslatef(5.0*i, 0.0, 0.0);
		
			float percentThroughIntro = (difftime(clock(), startTime)/CLOCKS_PER_SEC)/animationIntroDuration;

			if (percentThroughIntro > 1.0)
			{
				glRotatef((percentThroughIntro-1)*90, 0, 0, 1);
			}
			else
			{
				glScalef(percentThroughIntro, percentThroughIntro, percentThroughIntro);
			}
		
			drawStaticTeapotGL();

		glPopMatrix();
	}

	lastTime = clock();
}


/**
* @brief Draws a very primative untextured tower (modeled on Telstra tower in Canberra Australia).
*/
void drawStaticTowerGL()
{
	const GLint stacks = 3, slices = 15, loops = 3;
	
	const int colourSize = 4;
	const GLfloat whiteConcreteAmbient[colourSize] = {0.4,0.4,0.4,1.0};
	const GLfloat whiteConcreteDiffuse[colourSize] = {0.4,0.4,0.4,1.0};
	const GLfloat whiteConcreteSpecular[colourSize] = {0.1,0.1,0.1,1.0};
	const GLfloat whiteConcreteShininess = 0.1;

	glMaterialfv(GL_FRONT, GL_AMBIENT, whiteConcreteAmbient);
	glMaterialfv(GL_FRONT, GL_DIFFUSE, whiteConcreteDiffuse);
	glMaterialfv(GL_FRONT, GL_SPECULAR, whiteConcreteSpecular);
	glMaterialf(GL_FRONT, GL_SHININESS, whiteConcreteShininess);

	GLUquadricObj* quadric;
	quadric = gluNewQuadric();
	gluQuadricDrawStyle(quadric, GLU_FILL);
	gluQuadricNormals(quadric, GLU_SMOOTH);
	gluQuadricOrientation(quadric, GLU_OUTSIDE);
	
	glPushMatrix();
		glScalef(0.3, 0.3, 0.3);
		//glRotatef(90,-1.0, 0.0, 0.0);
		glRotatef(-180,-1.0, 0.0, 0.0);
		glTranslated(0.0, -11.5, 0.0);	// Translate down by half the height of the tower so it is centered at the origin.

		// Center Spike
		glPushMatrix();
			glRotatef(90, -1.0, 0.0, 0.0);
			gluCylinder(quadric, 1.0, 0.25, 23, slices, stacks);
		glPopMatrix();
	
		// Center Spike Top Cap
		glPushMatrix();
			glTranslated(0.0, 23, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluDisk(quadric, 0, 0.25, slices, loops);
		glPopMatrix();

		// Telecommunications Mount
		glPushMatrix();
			glTranslated(0.0, 4, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluCylinder(quadric, 2, 2, 2.5, slices, stacks);
		glPopMatrix();

		// Telecommunications Mount Bottom Cap
		glPushMatrix();
			glTranslated(0.0, 4, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluDisk(quadric, 0, 2, slices, loops);
		glPopMatrix();
	
		// Telecommunications Mount Top Cap
		glPushMatrix();
			glTranslated(0.0, 6.5, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluDisk(quadric, 0, 2, slices, loops);
		glPopMatrix();

		// Viewing Platform
		glPushMatrix();
			glTranslated(0.0, 8.5, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluCylinder(quadric, 2.3, 2.6, 2, slices, stacks);
		glPopMatrix();

		// Viewing Platform Bottom Cap
		glPushMatrix();
			glTranslated(0.0, 8.5, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluDisk(quadric, 0, 2.3, slices, loops);
		glPopMatrix();

		// Viewing Platform Top Cap
		glPushMatrix();
			glTranslated(0.0, 10.5, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluDisk(quadric, 0, 2.6, slices, loops);
		glPopMatrix();
	
		// Extra Platform 1
		glPushMatrix();
			glTranslated(0.0, 13.0, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluCylinder(quadric, 1.5, 1.5, 0.5, slices, stacks);
		glPopMatrix();
		
		// Extra Platform 1 Bottom Cap
		glPushMatrix();
			glTranslated(0.0, 13, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluDisk(quadric, 0, 1.5, slices, loops);
		glPopMatrix();

		// Extra Platform 1 Platform Top Cap
		glPushMatrix();
			glTranslated(0.0, 13.5, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluDisk(quadric, 0, 1.5, slices, loops);
		glPopMatrix();

		// Extra Platform 2
		glPushMatrix();
			glTranslated(0.0, 14.0, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluCylinder(quadric, 1.5, 1.5, 0.5, slices, stacks);
		glPopMatrix();

		// Extra Platform 2 Bottom Cap
		glPushMatrix();
			glTranslated(0.0, 14, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluDisk(quadric, 0, 1.5, slices, loops);
		glPopMatrix();

		// Extra Platform 2 Platform Top Cap
		glPushMatrix();
			glTranslated(0.0, 14.5, 0.0);
			glRotatef(90, -1.0, 0.0, 0.0);
			gluDisk(quadric, 0, 1.5, slices, loops);
		glPopMatrix();
	glPopMatrix();
}

/**
* @brief Converts an OpenCV matrix into an OpenGL matrix.
* @param m The matrix to convert (must have type CV64FC1.
* @return The output matrix of type GLfloat[size].
*
* Note: This function allocates memory for the OpenGL matrix and it should
* manually be free'ed when it is no longer needed.
*/
GLfloat* convertMatrixType(const cv::Mat& m)
{
	typedef double precision;

	Size s = m.size();
	GLfloat* mGL = new GLfloat[s.width*s.height];

	for(int ix = 0; ix < s.width; ix++)
	{
		for(int iy = 0; iy < s.height; iy++)
		{
			mGL[ix*s.height + iy] = m.at<precision>(iy, ix);
		}
	}

	return mGL;
}

/**
* @brief Clears the selection.
*/
void clearSelection()
{
	selectionPoints.clear();
}

/**
* @brief Adds a new point to the selection points buffer.
* @param x The x location of the point in screen coordinates.
* @param y The y location of the point in screen coordinates.
*/
void selectPoint(int x, int y)
{
	if (selectionPoints.size() >= 4)
	{
		selectionPoints.clear();
	}
	else
	{
		selectionPoints.push_back(Point2f(x, y));
	}
}

/**
* @brief Sets the selection region (in the selection point buffer) based on two corners.
* @param x1 The x location of the 1st corner of the selection region in screen coordinates.
* @param y1 The y location of the 1st corner of the selection region in screen coordinates.
* @param x2 The x location of the 2nd corner of the selection region in screen coordinates.
* @param y2 The y location of the 2nd corner of the selection region in screen coordinates.
*/
void selectRegion(int x1, int y1, int x2, int y2)
{
	clearSelection();
	
	selectionPoints.push_back(Point2f(x1, y1));
	selectionPoints.push_back(Point2f(x2, y2));
}

/**
* @brief Renders a simple marker.
* @param size The size of the marker to draw.
* @param locationX The x location to draw the marker.
* @param locationY The y location to draw the marker.
*/
void drawSelectionMarker(float size, float locationX, float locationY)
{
	glBegin(GL_LINES);
		glColor3f(0.0, 1.0, 0.0);
		glVertex2f(locationX-size/2, locationY-size/2);
		glVertex2f(locationX+size/2, locationY+size/2);

		glVertex2f(locationX-size/2, locationY+size/2);
		glVertex2f(locationX+size/2, locationY-size/2);
	glEnd();
}

/**
* @brief Renders a box around the selection region.
* @param locationX1 The x location of one corner of the selection region.
* @param locationY1 The y location of one corner of the selection region.
* @param locationX2 The x location of the other corner of the selection region.
* @param locationY2 The y location of the other corner of the selection region.
*/
void drawSelectionRegion(float locationX1, float locationY1, float locationX2, float locationY2)
{
	glBegin(GL_LINES);
		glColor3f(0.0, 1.0, 0.0);
		glVertex2f(locationX1, locationY1);
		glVertex2f(locationX2, locationY1);

		glVertex2f(locationX2, locationY1);
		glVertex2f(locationX2, locationY2);
		
		glVertex2f(locationX2, locationY2);
		glVertex2f(locationX1, locationY2);

		glVertex2f(locationX1, locationY2);
		glVertex2f(locationX1, locationY1);
	glEnd();
}

/**
* @brief Renders the selection (either all the selection points in the current selection list or the selection region).
*/
void drawSelection()
{	
	// Save State
	bool initialLighting = glIsEnabled(GL_LIGHTING);

	GLint initMatrixMode;
	glGetIntegerv(GL_MATRIX_MODE, &initMatrixMode);

	GLfloat initialModelview[16];
	glGetFloatv(GL_MODELVIEW_MATRIX, initialModelview);
	
	GLfloat initialProjection[16];
	glGetFloatv(GL_PROJECTION_MATRIX, initialProjection);
	


	// Set State
	glDisable(GL_LIGHTING);

	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluOrtho2D(0.0, width, 0.0, height);
	
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	

	switch (selectionMode)
	{
	case SelectionMode_Points:
		// Draw markers.
		for(int i = 0; i < selectionPoints.size(); i++)
		{
			drawSelectionMarker(10.0, selectionPoints[i].x, height-selectionPoints[i].y);
		}
		break;
	case SelectionMode_Region:
		if (selectionPoints.size() >= 2)
		{
			drawSelectionRegion(selectionPoints[0].x, height-selectionPoints[0].y, selectionPoints[1].x, height-selectionPoints[1].y);
		}
		break;
	}

	// Restore State
	if (initialLighting)
	{
		glEnable(GL_LIGHTING);
	}
	else
	{
		glDisable(GL_LIGHTING);
	}

	glMatrixMode(GL_MODELVIEW);
	glLoadMatrixf(initialModelview);

	glMatrixMode(GL_PROJECTION);
	glLoadMatrixf(initialProjection);
	
	glMatrixMode(initMatrixMode);
}

/**
* @brief Handels a keypress.
* @param key The key that was pressed.
* @param x The x location of the mouse when the key was pressed (in screen coordinates).
* @param y The y location of the mouse when the key was pressed (in screen coordinates).
* @return Whether the keypress indicates we should terminate (ture = terminate, false = dont terminate).
*/
bool keypress(unsigned char key, int x, int y)
{
	switch (tolower(key))
	{
	case '0': // Augmentation mode.
	case '1':
	case '2':
	case '3':
	case '4':
	case '5':
	case '6':
	case '7':
	case '8':
	case '9':
		{
		char k = key;
		augmentationMethod = atoi(&k);
		}
		break;
	case 27:	// Escape
	case 'q':	// Quit the program.
		return true;
		break;
	case 'c': // Reload the calibration images.
		loadCalibrationImages();
		calibrate();
		break;
	case 'h': // Hold the current frame in the image buffer.
		setHoldImage();
		break;
	case 'a': // Add the currently held image to the calibration image set.
		addToCalibrationImages();
		break;
	case 's': // Save the calibration images.
		saveCalibrationImages();
		break;
	case 'b': // Save the held image as a marker image.
		saveHeldImage();
		break;
	case 'v': // Toggle the view so that you can see the currently held image.
		toggleUseHeldImage();
		break;
	case 'i': // Toggles on/off sub pixel accuracy for chess board images.
		toggleSubPixelAccuracy();
		break;
	case 'm': // Cycle through the natural markers.
		changeNaturalImageMarker();
		break;
	case 'd': // Changes the model displayed.
		forceStaticTeapot = !forceStaticTeapot;
		break;
	case '-': // Decreases the natural marker scale by a factor of 2.
		naturalMarkerScale /= 2;
		break;
	case '+': // Increases the natural marker scale by a factor of 2.
		naturalMarkerScale *= 2;
		break;
	}

	return false;
}

/**
* @brief Handels a mouse click.
* @param x The location of the mouse when the button was clicked (in screen coordinates).
* @param y The location of the mouse when the button was clicked (in screen coordinates).
*/
void mouseClick(int x, int y)
{
	
	switch (augmentationMethod)
	{
	case 5:
		selectPoint(x, y);
		break;
	}
}

/**
* @brief Handels a mouse drag action.
* @param pressedValid Whether the pressed value is valid or unknown (valid = true, unknown = false - the last value of pressed will be used).
* @param pressed Whether the button was pressed or released (pressed = true, released = false).
* @param x The location of the mouse when the button was clicked (in screen coordinates).
* @param y The location of the mouse when the button was clicked (in screen coordinates).
*/
void mouseDrag(bool pressedValid, bool pressed, int x, int y)
{
	static bool lastPressed = false;
	static int pressedX = 0;
	static int pressedY = 0;
	
	switch (augmentationMethod)
	{
	case 5:
		clearSelection();

		// If the user has just pressed the button.
		if (pressedValid && pressed)
		{
			selectionRegionValid = false;
			pressedX = x;
			pressedY = y;
		}
		else
		{
			if (pressedValid && !pressed)
			{
				selectionRegionValid = true;
			}
			
			// Make sure that they have selected at least some space.
			if (lastPressed && (x != pressedX) && (y != pressedY)) 
			{
				selectRegion(pressedX, pressedY, x, y);
			}
		}
		break;
	}

	if (pressedValid)
	{
		lastPressed = pressed;
	}
}

/**
* @brief This function is a callback for GLUT when a keypress is detected.
* @param key The key pressed.
* @param x The x location of the mouse when the key was pressed.
* @param y The y location of the mouse when the key was pressed.
*/
void keyboardGLUT(unsigned char key, int x, int y)
{
	if (keypress(key, x, y))
	{
		exit(0);
	}
}


/**
* @brief This function is a callback for GLUT when a mouse button is clicked.
* @param button The button that was pressed.
* @param state The state change that the button experienced.
* @param x The x location in screen co-ordinates when the action occured.
* @param y The y location in screen co-ordinates when the action occured.
*/
void mouseGLUT(int button, int state, int x, int y)
{
	if (button == GLUT_LEFT_BUTTON)
	{
		if (state == GLUT_DOWN)
		{
			switch (selectionMode)
			{
			case SelectionMode_Points:
				mouseClick(x, y);
				break;
			case SelectionMode_Region:
				mouseDrag(true, true, x, y);
				break;
			}
		}
		else
		{
			switch (selectionMode)
			{
			case SelectionMode_Region:
				mouseDrag(true, false, x, y);
				break;
			}
		}
	}
}

/**
* @brief This function is a callback for GLUT when the mouse with a button depressed.
* @param x The x location in screen co-ordinates when the event occured.
* @param y The y location in screen co-ordinates when the event occured.
*/
void mouseMotionGLUT(int x, int y)
{
	switch (selectionMode)
	{
	case SelectionMode_Region:
		mouseDrag(false, false, x, y);
		break;
	}
}

/**
* @brief Toggles the use held image state.
*
* The state is maintained as a bool and used elsewhere.
* This state reflects whether we are using the held image for display currently.
*/
void toggleUseHeldImage()
{
	useHeldImage = !useHeldImage;
}

/**
* @brief Sets up to grab the next image as the held image.
*
* The state is maintained as a bool and used elesewhere.
* This state reflects whether to capture the next image.
*/
void setHoldImage()
{
	holdImage = true;
}

/**
* @brief Toggles whether we are using sub pixel accuracy when finding the chessboard corners.
*
* The state is maintained as a bool and used elesewhere.
* This value is not used globally, instead some function calls make use of it and others override it
* and set the value explicitly.
*/
void toggleSubPixelAccuracy()
{
	subPixelAccuracy = !subPixelAccuracy;
}

/**
* @brief Changes the filename of the natural image marker we are using.
*/
void changeNaturalImageMarker()
{
	static int markerIndex = 0;

	markerIndex = (markerIndex+1)%5;

	switch (markerIndex)
	{
	case 0:
		naturalMarkerImageFilename = "Marker 1.png";
		break;
	case 1:
		naturalMarkerImageFilename = "Marker 2.png";
		break;
	case 2:
		naturalMarkerImageFilename = "Marker 3.png";
		break;
	case 3:
		naturalMarkerImageFilename = "Marker 4.png";
		break;
	case 4:
		naturalMarkerImageFilename = "Marker 0.png";
		break;
	}
}

/**
* @brief Saves the held image file to file.
*/
void saveHeldImage()
{
	Mat image = heldImage;

	if (augmentationMethod == 5)
	{
		image = selectionTransform(image, false);
	}

	// Save the image file.
	imwrite(saveHeldImageFilename, image);
}

/**
* @brief Adds the image in the held image buffer to the calibration image list.
*
* Note if holdImage = true this equates to the current image being used, and if
* heldImage = false then it equates to using the stored image.
*/
void addToCalibrationImages()
{
	Mat deepCopy;
	heldImage.copyTo(deepCopy);

	calibrationImages.push_back(deepCopy);
}

/**
* @brief Converts an int to a string.
* @param i The integer to be converted to a string.
* @return The string representation of the integer.
*/
string intToString(int i)
{
	stringstream s;
	s << i;
	return s.str();
}

/**
* @brief Saves all of the calibration images we have to file.
*/
void saveCalibrationImages()
{
	int number = calibrationImageSequenceStart;

	for(vector<Mat>::iterator i = calibrationImages.begin() ; i != calibrationImages.end(); i++)
	{
		// Get the base filename
		string filename = calibrationImageFilenameBase;
		// Find where to put the sequence number.
		string::size_type position = filename.find(calibrationImageSequence);
		// Put the image sequence number in the filename.
		filename.replace(position, calibrationImageSequence.length(), intToString(number++));

		// Save the image file.
		imwrite(filename, *i);
	}
}

/**
* @brief Loads all calibration images from file.
*
* Calibration images are loaded from file using the calibration image filename base
* with increasing sequence numbers until one sequence number is not found.
*/
void loadCalibrationImages()
{
	int number = calibrationImageSequenceStart;

	while (true)
	{
		// Get the base filename.
		string filename = calibrationImageFilenameBase;
		// Find where to put the sequence number.
		string::size_type position = filename.find(calibrationImageSequence);
		// Put the image sequence number in the filename.
		filename.replace(position, calibrationImageSequence.length(), intToString(number++));

		// Try to read the image.
		Mat image = imread(filename);

		// If we were successfully able to read the image.
		if (image.data != nullptr)
		{
			// Add it to the list.
			calibrationImages.push_back(image);
		}
		else
		{
			// Otherwise give up.
			break;
		}
	}
}

/**
* @brief Uses the set of calibration images to calculate the cameras intrinsic and distortion paramaters.
* @param subPixel Whether to use subpixel accuracy when extracting the chessboard corners from the calibration images (true = use subPixel accuracy, false = don't use subPixel accuracy).
*
* The paramaters discovered are immediatly stored to the appropriate global variables.
*/
void calibrate(bool subPixel)
{		
	vector<Mat> dummyRotation;		// The camera calibration function returns the object rotation for each image, but we have no use for it here.
	vector<Mat> dummyTranslation;	// The camera calibration function returns the object translation for each image, but we have no use for it here.

	vector<Point3f> virtualCorners;	// objectCorners - Thoes points that we hope to match with.
	vector<Point2f> realCorners;	// imageCorners - Thoes points that we have actually found.
	
	vector< vector<Point3f> > allVirtualCorners;
	vector< vector<Point2f> > allRealCorners;

	buildChessboardCornerPoints(&virtualCorners, chessBoardScale);

	// For all the calibration images.
	for(vector<Mat>::iterator i = calibrationImages.begin() ; i != calibrationImages.end(); i++)
	{
		// Find the chess board corners.
		bool foundCorners = findChessboardCorners(*i, Size(chessCornersX, chessCornersY), realCorners, findCornerFlags);
		
		// If we were able to find the corners.
		if (foundCorners)
		{
			if (subPixel)
			{
				improveCornerAccuracy(*i, realCorners);
			}

			// Store the real corners and there correspondance to the chessboard pattern.
			allRealCorners.push_back(realCorners);
			allVirtualCorners.push_back(virtualCorners);
		}
	}

	// If we have found some corners.
	if (allRealCorners.size() != 0)
	{
		Size imgSize = Size(width, height);

		calibrateCamera(allVirtualCorners, allRealCorners, imgSize, calibrationMatrix, calibrationDistortionCoefficients, dummyRotation, dummyTranslation);
	}
}

/**
* @brief Constructs a matrix which holds all of the corner points of the chessboard.
* @param corners The list of all the corners.
* @param scale The scale of the chess board corners (i.e. 1 square = how many units).
*
* The corners are ordered column at at time (as opposed to row at at time),
* ie. column 1 then column 2 etc.
*/
void buildChessboardCornerPoints(std::vector<cv::Point3f>* corners, float scale)
{
	if (corners != nullptr)
	{
		for(int ix = 0; ix < chessCornersY; ix++)
		{
			for(int iy = 0; iy < chessCornersX; iy++)
			{
				corners->push_back(Point3f(iy*scale, ix*scale, 0));
			}
		}
	}
}

/**
* @brief This function takes an image and improves the accuracy of the corner approximations.
* @param image The image to find the corners in.
* @param corners The corner approximations to improve (this is done insitue)
*
* This function simplifies the task rather then calling cornerSubPix() directly,
* because currently OpenCV 2.2 cornerSubPix() is incapable of automatically
* processing colour imaages and so the image needs to be manually converted to 
* greyscale first.
*/
void improveCornerAccuracy(const cv::Mat& image, std::vector<cv::Point2f>& corners)
{
	Mat gray(image.size(), CV_8UC1);

	cvtColor(image, gray, CV_BGR2GRAY);
		
	cornerSubPix(gray, corners, Size(11, 11), Size(-1, -1), TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1));
}

/**
* @brief This function decomposes a homography using the cameras intrinsic pramaters to find the extrinsic pramaters.
* @param H The homograpgy to decompose.
* @param rotation The extrinsic camera rotation.
* @param translation The extrinsic camera translation.
*
* See Learning OpenCV Computer Vision with the OpenCV Library 
* G Bradski & A Kaehler 1ST Edition Page 391 for a reference to the maths in this function.
*/
void getExtrinsicsFromHomography(cv::Mat H, cv::Mat& rotation, cv::Mat& translation)
{
	typedef double precision;
	int precisionType = CV_64FC1;

	Mat inverseCalibrationMatrix = calibrationMatrix.inv(DECOMP_SVD);
	
	// Split the homography matrix into 3 vectors.
	double h1A[3][1] = {{H.at<precision>(0,0)} , {H.at<precision>(1,0)} , {H.at<precision>(2,0)}};
	Mat h1(3, 1, precisionType, h1A);
	
	double h2A[3][1] = {{H.at<precision>(0,1)} , {H.at<precision>(1,1)} , {H.at<precision>(2,1)}};
	Mat h2(3, 1, precisionType, h2A);

	double h3A[3][1] = {{H.at<precision>(0,2)} , {H.at<precision>(1,2)} , {H.at<precision>(2,2)}};
	Mat h3(3, 1, precisionType, h3A);
	
	// Remove the calibration paramaters before computing the scale length.
	Mat scaleVector = inverseCalibrationMatrix * h1;

	// Calculate the the length of H1 for normalising.
	double scale = sqrt(scaleVector.at<precision>(0,0)*scaleVector.at<precision>(0,0) +
						scaleVector.at<precision>(1,0)*scaleVector.at<precision>(1,0) +
						scaleVector.at<precision>(2,0)*scaleVector.at<precision>(2,0));

	if(scale != 0)
	{
		scale = 1/scale;

		// Normalise the inverseCalibrationMatrix
		inverseCalibrationMatrix = inverseCalibrationMatrix * scale;

		// Remove the calibration paramaters from the translation.
		translation = inverseCalibrationMatrix * h3;

		Mat r1 = inverseCalibrationMatrix * h1;
		Mat r2 = inverseCalibrationMatrix * h2;
		Mat r3 = r1.cross(r2);			// Find the vector perpendicular (orthogonal) to the other 2 rotation vectors.
   
		precision rotationMatrixA[3][3] = {{r1.at<precision>(0,0) , r2.at<precision>(0,0) , r3.at<precision>(0,0)},
												  {r1.at<precision>(1,0) , r2.at<precision>(1,0) , r3.at<precision>(1,0)},
												  {r1.at<precision>(2,0) , r2.at<precision>(2,0) , r3.at<precision>(2,0)}};
		Mat rotationMatrix(3, 3, precisionType, rotationMatrixA);
	
		// Enforce RT*R = R*RT = I (Where RT is R transpose), by setting D to I (I = identity matrix).
		SVD decomposed(rotationMatrix);
		rotation = decomposed.u * decomposed.vt;
	}
	else 
	{
		// Can't divide by a zero.
		translation = Mat::zeros(3, 1, precisionType) ;
		rotation = Mat::eye(3, 3, precisionType) ;
	}
}

/**
* @brief This function turns the cameras intrinsic and extrinsic pramaters into the OpenGL projection and modelview matricies.
* @param calibration The camreas intrinsic pramaters.
* @param rotation The cameras extrinsic pramater (rotation).
* @param translation The cameras extrinsic pramater (translation).
* @param projection Variable to store the OpenGL projection matrix.
* @param modelview Variable to store the OpenGL modelview matrix.
*
* This function implicitly translates between OpenCV's coordinate system and OpenGL's coordinate system.
*/
void generateProjectionModelview(const cv::Mat& calibration, const cv::Mat& rotation, const cv::Mat& translation, cv::Mat& projection, cv::Mat& modelview)
{
	typedef double precision;

 	projection.at<precision>(0,0) = 2*calibration.at<precision>(0,0)/640;
	projection.at<precision>(1,0) = 0;
	projection.at<precision>(2,0) = 0;
	projection.at<precision>(3,0) = 0;

	projection.at<precision>(0,1) = 0;
	projection.at<precision>(1,1) = 2*calibration.at<precision>(1,1)/480;
	projection.at<precision>(2,1) = 0;
	projection.at<precision>(3,1) = 0;

	projection.at<precision>(0,2) = 1-2*calibration.at<precision>(0,2)/640;
	projection.at<precision>(1,2) = -1+(2*calibration.at<precision>(1,2)+2)/480;
	projection.at<precision>(2,2) = (zNear+zFar)/(zNear - zFar);
	projection.at<precision>(3,2) = -1;

	projection.at<precision>(0,3) = 0;
	projection.at<precision>(1,3) = 0;
	projection.at<precision>(2,3) = 2*zNear*zFar/(zNear - zFar);
	projection.at<precision>(3,3) = 0;
	

	modelview.at<precision>(0,0) = rotation.at<precision>(0,0);
	modelview.at<precision>(1,0) = rotation.at<precision>(1,0);
	modelview.at<precision>(2,0) = rotation.at<precision>(2,0);
	modelview.at<precision>(3,0) = 0;

	modelview.at<precision>(0,1) = rotation.at<precision>(0,1);
	modelview.at<precision>(1,1) = rotation.at<precision>(1,1);
	modelview.at<precision>(2,1) = rotation.at<precision>(2,1);
	modelview.at<precision>(3,1) = 0;

	modelview.at<precision>(0,2) = rotation.at<precision>(0,2);
	modelview.at<precision>(1,2) = rotation.at<precision>(1,2);
	modelview.at<precision>(2,2) = rotation.at<precision>(2,2);
	modelview.at<precision>(3,2) = 0;

	modelview.at<precision>(0,3) = translation.at<precision>(0,0);
	modelview.at<precision>(1,3) = translation.at<precision>(1,0);
	modelview.at<precision>(2,3) = translation.at<precision>(2,0);
	modelview.at<precision>(3,3) = 1;

	// This matrix corresponds to the change of coordinate systems.
	static double changeCoordArray[4][4] = {{1, 0, 0, 0}, {0, -1, 0, 0}, {0, 0, -1, 0}, {0, 0, 0, 1}};
	static Mat changeCoord(4, 4, CV_64FC1, changeCoordArray);
	
	modelview = changeCoord*modelview;
}

/**
* @brief Draws the homography of a s sized rectangle projected on the image.
* @param image The image to draw the rectangle on.
* @param H The homography to apply (it type is assumed to be CV_32FC1).
* @param s The size of the "rectangle" to draw.
* @param colour The colour to draw the rectangle in.
* @param thickness The thickness of the lines of the rectangle.
* @param lineType The connectedness of the line (i.e. 4, 8 etc).
* @param shift 
*
* The last paramaters of this function call match the function call paramaters of the
* OpenCV function drawLine().
*
* Note: The precision of float here is so that it matches the precision of the Homography, which
* in the case of the caller is float and because of Point2f (note the F).
*/
void drawHomography(cv::Mat& image, cv::Mat& H, cv::Size s, cv::Scalar colour, int thickness, int lineType, int shift)
{	
	typedef float precision;

	// Corners of the rectangle we will be projecting.
    vector<Point2f> corners(4);
	corners[0].x =0;
	corners[0].y =0;
	corners[1].x =s.width;
	corners[1].y =0;
	corners[2].x =s.width;
	corners[2].y =s.height;
	corners[3].x =0;
	corners[3].y = s.height;

	// Compute the coner positions after they have been transformed by the homography.
	Mat cornersTransformed;
    perspectiveTransform(Mat(corners), cornersTransformed, H);
	
	// Draw the rectangle on to the image.
	for(int i = 0; i < 4; i++)
	{
		Point p1 = Point(cornersTransformed.at<precision>(i, 0), cornersTransformed.at<precision>(i, 1));
		Point p2 = Point(cornersTransformed.at<precision>((i+1)%4, 0), cornersTransformed.at<precision>((i+1)%4, 1));

		line(image, p1, p2, colour, thickness, lineType, shift);
	}
}

/**
* @brief Calculates the euclidian distance between two points.
* @param p1 The first point.
* @param p2 The first point.
* @return The euclidian distance.
*/
float calcDistance(cv::Point2f p1, cv::Point2f p2)
{
	return sqrt((p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y));
}

/**
* @brief Clamps the value within the range.
* @param value The value to clamp to the range.
* @param min The minimum value.
* @param max The maximum value.
* @return The value clamped in the range min to max (the result is undefined if max < min).
*/
int clamp(int value, int min, int max)
{
	value = value < min ? min : value;
	value = value > max ? max : value;

	return value;
}

/**
* @brief Transforms the specified image using the selection points (if there are 4).
* @param image the image to transform.
* @param maintainSize Whether to maintin the input images size for the output image.
* @return The image once it has been transformed.
*
* If there arnt 4 points selected the image is returned un altered.
*/
cv::Mat selectionTransform(const cv::Mat& image, bool maintainSize)
{
	if ((selectionMode == SelectionMode_Region) && selectionRegionValid && (selectionPoints.size() == 2))
	{
		int minX = selectionPoints[0].x < selectionPoints[1].x ? selectionPoints[0].x : selectionPoints[1].x;
		int minY = selectionPoints[0].y < selectionPoints[1].y ? selectionPoints[0].y : selectionPoints[1].y;
		int maxX = selectionPoints[0].x > selectionPoints[1].x ? selectionPoints[0].x : selectionPoints[1].x;
		int maxY = selectionPoints[0].y > selectionPoints[1].y ? selectionPoints[0].y : selectionPoints[1].y;
		
		minX = clamp(minX, 0, maxX);
		minY = clamp(minY, 0, maxY);

		maxX = clamp(maxX, minX, image.size().width-1);
		maxY = clamp(maxY, minY, image.size().height-1);

		Rect r(minX, minY, maxX-minX, maxY-minY);
		Mat warpROI(image, r);
		Mat warp(r.size(), image.type());
		warpROI.copyTo(warp);

		return warp;
	}

	if ((selectionMode == SelectionMode_Points) && (selectionPoints.size() == 4))
	{
		// Specifiy the size and aspect ration of the selection after the transformation.
		//Size newSize = image.size;
		//Size newSize = Size(selectionPoints[1].x-selectionPoints[0].x, selectionPoints[3].y-selectionPoints[1].y);	// Need to accuratly get the size from the original image or atleast aspect ratio (is this even possible?).
		float dx1 = calcDistance(selectionPoints[0], selectionPoints[1]);												// This calculation also forces the user to select the points in the order below (again we really need to untangle these to make it easier for the user).
		float dy1 = calcDistance(selectionPoints[1], selectionPoints[3]);
		float dx2 = calcDistance(selectionPoints[2], selectionPoints[3]);
		float dy2 = calcDistance(selectionPoints[0], selectionPoints[2]);
		
		float dXMax = dx1 > dx2 ? dx1 : dx2;
		float dYMax = dy1 > dy2 ? dy1 : dy2;

		Size newSize;
		if (dXMax > dYMax)
		{
			newSize = Size(dXMax, dYMax/selectionAspect);
		}
		else
		{
			newSize = Size(dXMax*selectionAspect, dYMax);
		}

		// Specify the real coordinates that the selected points should be translated to.
		// Note the order of the corners here must match the order we select the corners (in future could perfom some simple maths to untangle them if the user selects in a different order).
		Point2f imgCorners[4];																						
		imgCorners[0].x = 0;
		imgCorners[0].y = 0;
		imgCorners[1].x = newSize.width;
		imgCorners[1].y = 0;
		imgCorners[2].x = 0;
		imgCorners[2].y = newSize.height;
		imgCorners[3].x = newSize.width;
		imgCorners[3].y = newSize.height;

		// Convert the selected points representation (vector to array).
		Point2f selPoints[4];
		for(int i = 0; i < selectionPoints.size(); i++)
		{
			selPoints[i]= selectionPoints[i];
		}

		// Compute the transform we need to warp the old image to the new image.
		Mat t = getPerspectiveTransform(selPoints, imgCorners);									

		// Compute the size of the new image (either the new size or put it in the corner of an image of the original image size).
		Size warpSize = newSize;
		if (maintainSize)
		{
			warpSize = image.size();
		}

		// Create a new image to hold the warped part of the original image.
		Mat warp(warpSize, image.type());										
		// Pick out the region of interest that we want to warp the image to.
		Mat warpROI = warp(Rect(0, 0, newSize.width, newSize.height));				
		// Warp the portion of the old image to the portion of the new image.
		warpPerspective(image, warpROI, t, newSize, INTER_LINEAR, BORDER_TRANSPARENT);

		return warp;
	}

	return image;
}

/**
* @brief This is a simple augmentation to just render the image we are grabbing.
* @param image The image that we are processing.
* @return The augmented image information.
*
* This function is useful for making sure that all the base functionality is working
* correctly and we are succesfully grabbing an image from the camera. It can also
* beused to examine artifacts etc in the initial image, and provides a baseline for
* augmentation performance because it does nothing it allows for the fastest possible
* framerate.
*/
AugmentationInformation augmentationDoNothing(const cv::Mat& image)
{
	AugmentationInformation ai;

	ai.liveImage = image;
	ai.augmentationMode = AugmentationMode_NONE;

	return ai;
}

/**
* @brief Computes the augmentation with a planar chess board.
* @param image The image that we are processing.
* @param subPixel Whether to use subpixel accuracy when extracting the chessboard corners (true = use subPixel accuracy, false = don't use subPixel accuracy).
* @param overlayImage Either overlay or draw chessboard (true = overlay, false = draw chess board).
* @param  modulate Either modulate the image (add the image to it) or replace the image (true = modulate, false = replace).
* @return The augmented image information.
*
* If modifiying this function make similar updates to augmentationChessSurface(), if I have time merge these two functions.
*/
AugmentationInformation augmentationChessPlanar(const cv::Mat& image, bool subPixel, bool overlayImage, bool modulate)
{
	AugmentationInformation augmentation;
	augmentation.liveImage = image;
	
	// Find the corners in the image.
	std::vector<Point2f> corners;
	bool foundCorners = findChessboardCorners(image, Size(chessCornersX, chessCornersY), corners, findCornerFlags);
	 
	// If we have found some corners.
	if(foundCorners)
	{
		if (subPixel)
		{
			improveCornerAccuracy(image, corners);
		}
		
		// Load the overlay image from file.
		static Mat loadedImage = imread(overlayImageFilename);

		if ((overlayImage) && (loadedImage.data != nullptr))
		{		
			// Store the pixel coordinates at each of the 4 image corner points.
			Point2f imgCorners[4];
			imgCorners[0].x = 0;
			imgCorners[0].y = 0;
			imgCorners[1].x = loadedImage.size().width;
			imgCorners[1].y = 0;
			imgCorners[2].x = 0;
			imgCorners[2].y = loadedImage.size().height;
			imgCorners[3].x = loadedImage.size().width;
			imgCorners[3].y = loadedImage.size().height;
		
			// Find the outter 4 corners of the detected chessboard.
			Point2f chessCorners[4];
			chessCorners[0].x = corners[0].x;
			chessCorners[0].y = corners[0].y;
			chessCorners[1].x = corners[chessCornersX-1].x;
			chessCorners[1].y = corners[chessCornersX-1].y;
			chessCorners[2].x = corners[chessCornersX*(chessCornersY-1)].x;
			chessCorners[2].y = corners[chessCornersX*(chessCornersY-1)].y;
			chessCorners[3].x = corners[chessCornersX*chessCornersY-1].x;
			chessCorners[3].y = corners[chessCornersX*chessCornersY-1].y;
		
			// Compute the transform that maps the image corners to the chessboard corners.
			Mat transform = getPerspectiveTransform(imgCorners, chessCorners);
			// Create space to store the image when we warp it.
			Mat warp(image.size().height, image.size().width, image.type());

			if (modulate)
			{
				// Warp the image and add it to the live image.
				warpPerspective(loadedImage, warp, transform, warp.size());
				add(image, warp, warp);
			}
			else
			{
				// Warp the image directly into the live image.
				warp = image;
				warpPerspective(loadedImage, warp, transform, warp.size(), INTER_LINEAR, BORDER_TRANSPARENT);
			}
			
			augmentation.liveImage = warp;
		}
		else
		{
			// Just draw the detected chess board corners onto the image.
			drawChessboardCorners(augmentation.liveImage, Size(chessCornersX, chessCornersY), Mat(corners), foundCorners);
		}
	}
 	 	
	return augmentation;
}

/**
* @brief Computes the augmentation with a chess board that can be warped slightly.
* @param image The image that we are processing.
* @param subPixel Whether to use subpixel accuracy when extracting the chessboard corners (true = use subPixel accuracy, false = don't use subPixel accuracy).
* @param overlayImage Either overlay or draw chessboard (true = overlay, false = draw chess board).
* @param  modulate Either modulate the image (add the image to it) or replace the image (true = modulate, false = replace).
* @return The augmented image information.
*
* This function probably could and should be merged with augmentationChessPlanar() they share much of the same code, but I haven't 
* had time to merge them properly yet.
*/
AugmentationInformation augmentationChessSurface(const cv::Mat& image, bool subPixel, bool overlayImage, bool modulate)
{
	AugmentationInformation augmentation;
	augmentation.liveImage = image;
	
	// Find the corners in the image.
	std::vector<Point2f> corners;
	bool foundCorners = findChessboardCorners(image, Size(chessCornersX, chessCornersY), corners, findCornerFlags);

	Mat warp(image.size().height, image.size().width, image.type());
	 
	// If we have found some corners.
	if(foundCorners)
	{
		if (subPixel)
		{
			improveCornerAccuracy(image, corners);
		}
		
		// Load the overlay image from file.
		static Mat loadedImage = imread(overlayImageFilename);

		if ((overlayImage) && (loadedImage.data != nullptr))
		{		
			// Store the pixel coordinates the correspond to the size of a chess square.		
			Point2f imgCorners[4];
			imgCorners[0].x = 0;
			imgCorners[0].y = 0;
			imgCorners[1].x = loadedImage.size().width/(chessCornersX-1);
			imgCorners[1].y = 0;
			imgCorners[2].x = 0;
			imgCorners[2].y = loadedImage.size().height/(chessCornersY-1);
			imgCorners[3].x = loadedImage.size().width/(chessCornersX-1);
			imgCorners[3].y = loadedImage.size().height/(chessCornersY-1);
		
			// For each of the chess squares.
			Point2f chessCorners[4];
			for(int ix = 0; ix < (chessCornersX-1); ix++)
			{
				for(int iy = 0; iy < (chessCornersY-1); iy++)
				{
					// Find the corners of the current chess square.
					Point2f chessCorners[4];
					chessCorners[0].x = corners[ix+iy*chessCornersX].x;
					chessCorners[0].y = corners[ix+iy*chessCornersX].y;
					chessCorners[1].x = corners[(ix+1)+iy*chessCornersX].x;
					chessCorners[1].y = corners[(ix+1)+iy*chessCornersX].y;
					chessCorners[2].x = corners[ix+(iy+1)*chessCornersX].x;
					chessCorners[2].y = corners[ix+(iy+1)*chessCornersX].y;
					chessCorners[3].x = corners[(ix+1)+(iy+1)*chessCornersX].x;
					chessCorners[3].y = corners[(ix+1)+(iy+1)*chessCornersX].y;
		
					// Compute the transform that maps the image corners to the chessboard corners for this piece.
					Mat transform = getPerspectiveTransform(imgCorners, chessCorners);
					
					// Compute the size of the subregion of the image we are going to extract and take just this bit of the image.
					float subRegionSizeX = loadedImage.size().width/(chessCornersX-1);
					float subRegionSizeY = loadedImage.size().height/(chessCornersY-1);
					
					Mat subRegion = loadedImage(Rect(ix*subRegionSizeX, iy*subRegionSizeY, subRegionSizeX, subRegionSizeY));

					if (modulate)
					{
						// Warp the image and add it to the live image.
						warpPerspective(subRegion, warp, transform, warp.size());
						add(image, warp, warp);
					}
					else
					{
						// Warp the image directly into the live image.
						warp = image;
						warpPerspective(subRegion, warp, transform, warp.size(), INTER_LINEAR, BORDER_TRANSPARENT);
					}
				}
			}
			
			augmentation.liveImage = warp;
		}
		else
		{
			// Just draw the detected chess board corners onto the image.
			drawChessboardCorners(augmentation.liveImage, Size(chessCornersX, chessCornersY), Mat(corners), foundCorners);
		}
	}
 	 	
	return augmentation;
}

/**
* @brief A simple augmentation that allows us to display the calibration images.
* @param frequency The rate at which the image is changed in seconds.
* @return The augmented image information.
*/
AugmentationInformation augmentationCalibrationImages(float frequency)
{
	AugmentationInformation ai;
	static clock_t startTime = clock();

	int images = calibrationImages.size();

	if (images > 0)
	{
		float seconds = (float(difftime(clock(), startTime)))/CLOCKS_PER_SEC;

		int image = (int(seconds/frequency))%images;

		ai.liveImage = calibrationImages[image];
	}

	return ai;
}

/**
* @brief This funation uses the distortion coefficients discovered during calibration to compensate for distortion in the cameras image.
* @param image The image that we are processing.
* @return The augmented image information.
*
* Note: Could split the code in this function off to a seperate function and undistort all images before further processing them.
* I would then need to set the optotimed camera calibration matrix for futher use from there.
* But no need, both web cams I have showed no obvious reason to use them, maybe the dirver
* is already doing this before I grab the image (factory calibration???).
*/
AugmentationInformation augmentationUndistort(const cv::Mat& image)
{
	AugmentationInformation ai;

	// Compute the ideal new camera calibration matrix (with no distortion).
	Mat optimalCameraMatrix = getOptimalNewCameraMatrix(calibrationMatrix, calibrationDistortionCoefficients, image.size(), 0, image.size());

	// Undistort the image.
	Mat undistortedImage;
	undistort(image, undistortedImage, calibrationMatrix, calibrationDistortionCoefficients, optimalCameraMatrix);

	ai.liveImage = undistortedImage;
	ai.augmentationMode = AugmentationMode_NONE;
	
	return ai;
}

/**
* @brief This augmentation is designed to allow the user to select an image marker from the current image.
* @param image The image that we are processing.
* @return The augmented image information.
*
* This augmentation method effectively allows the user to pick a region from the current image
* and then aligns the region plane to the screen plane.
*/
AugmentationInformation augmentationCaptureMarker(const cv::Mat& image)
{
	AugmentationInformation ai;

	ai.liveImage = image;
	ai.augmentationMode = AugmentationMode_SELECTION;

	
	if ((selectionPoints.size() == 4) || (selectionRegionValid && (selectionPoints.size() == 2)))
	{
		ai.liveImage = selectionTransform(image, true);
		ai.augmentationMode = AugmentationMode_NONE;
	}

	return ai;
}

/**
* @brief Computes the augmentation for an input image that has a chess board in it.
* @param image The image that we are processing.
* @param subPixel Whether to use subpixel accuracy when extracting the chessboard corners from the calibration images (true = use subPixel accuracy, false = don't use subPixel accuracy).
* @return The augmented image information.
*
* This function really calculates the extrinsic pramaters for the chess board in the current image.
*/
AugmentationInformation augmentationChess3D(cv::Mat& image, bool subPixel)
{
	AugmentationInformation ai;

	ai.modelview.create(4, 4, CV_64FC1);
	ai.projection.create(4, 4, CV_64FC1);
	ai.liveImage = image;
	ai.augmentationMode = AugmentationMode_3D;
	ai.augmentationModel = AugmentationModel_Teapot_Dynamic;

	vector<Point2f> realCorners;		// The corners we found in the real image.
	vector<Point3f> virtualCorners;		// The corresponding corner positions for where the corners lie on the chess board (measured in virtual units).
		
	Mat rotation;						// The calculated rotation of the chess board.
	Mat translation;					// The calculated translation of the chess board.

	// Try to find the chess board corners in the image.
	bool foundCorners = findChessboardCorners(image, Size(chessCornersX, chessCornersY), realCorners, findCornerFlags);
	
	// If we weren't able to find the corners exit early.
	if(!foundCorners)
	{
		ai.augmentationMode = AugmentationMode_NONE;
		return ai;
	}

	if (subPixel)
	{
		improveCornerAccuracy(image, realCorners);
	}

	buildChessboardCornerPoints(&virtualCorners, chessBoardScale);

	//drawChessboardCorners(image, Size(chessCornersX, chessCornersY), realCorners, foundCorners);

	// Compute the rotation / translation of the chessboard (the cameras extrinsic pramaters).
	solvePnP(Mat(virtualCorners), Mat(realCorners), calibrationMatrix, calibrationDistortionCoefficients, rotation, translation);

	// Converte the rotation from 3 axis rotations into a rotation matrix.
	Mat rotationMatrix;
	Rodrigues(rotation, rotationMatrix);

	// The tranlation corresponds to the origin, which is at the corner of the chess board
	// but I would like to define the origin so that it is at the center of the chess board
	// so I need to offset by half of the size of the chessboard and need to multiply it by
	// the rotation so that it is in the local coordinate system of the chessboard.
	double offsetA[3][1] = {{(chessCornersX-1.0)/2.0}, {(chessCornersY-1.0)/2.0}, {0}};
	Mat offset(3, 1, CV_64FC1, offsetA);
	translation = translation + rotationMatrix*offset;
	
	// Turn the intrinsic and extrinsic pramaters into the projection and modelview matrix for OpenGL to use.
	generateProjectionModelview(calibrationMatrix, rotationMatrix, translation, ai.projection, ai.modelview);
	
	return ai;
}

/**
* @brief Computes augmentation using natural markers.
* @param image The image that we are processing.
* @param displayKeypoints Just find and display the keypoints found.
* @param displayMatches Just find and display all best matching keypoints.
* @param displayRansac Just find the homography using RANSAC and then display the inlier (matches) and outliers.
* @return The augmented image information.
*
* If you would like to experiment using other feature detectors, extractors
* and matchers here is a list of current OpenCV implementation you can try 
* easily by just changing the name.
*
* --- featureDetectorTypes ---
* "FAST"
* "STAR"
* "SIFT"
* "SURF"
* "MSER"
* "GFTT"
* "HARRIS"
* "Grid"
* "Pyramid"
* "Dynamic"
*
* --- descriptorExtractorTypes ---
* SIFT
* SURF
* BRIEF
* Opponent
*
* --- descriptorMatcherTypes ---
* FlannBased
* BruteForce
* BruteForce-L1
* BruteForce-Hamming
* BruteForce-HammingLUT
*/
AugmentationInformation augmentationNaturalMarkers1(const cv::Mat& image, bool displayKeypoints, bool displayMatches, bool displayRansac)
{
	AugmentationInformation ai;

	ai.modelview.create(4, 4, CV_64FC1);
	ai.projection.create(4, 4, CV_64FC1);
	ai.liveImage = image;
	ai.augmentationMode = AugmentationMode_3D;
	ai.augmentationModel = AugmentationModel_Tower_Static;
	
	
	
	const string featureDetectorType = "SURF";
	const string descriptorExtractorType = "SURF";
	const string descriptorMatcherType = "BruteForce";

	Ptr<FeatureDetector> featureDetector = FeatureDetector::create(featureDetectorType);
	Ptr<DescriptorExtractor> descriptorExtractor = DescriptorExtractor::create(descriptorExtractorType);
	Ptr<DescriptorMatcher> descriptorMatcher = DescriptorMatcher::create(descriptorMatcherType);

/*	// Check to make sure that we were able to create all the necessary componenets.
	if (featureDetector == nullptr) || descriptorExtractor == nullptr) || (descriptorMatcher == nullptr)
	{
		// Unable to create one of the feature identifier or matching types.
		return ai;
	} */

	
	// Read in the marker image.
	Mat img = image;
	static Mat marker;
	static string loadedMarkerFilename = "";
	bool newMarker = false;

	if (loadedMarkerFilename != naturalMarkerImageFilename)
	{
		newMarker = true;
		loadedMarkerFilename = naturalMarkerImageFilename;

		marker = imread(loadedMarkerFilename);

		if (marker.data == nullptr) // Unable to load file.
		{
			loadedMarkerFilename = "";

			ai.augmentationMode = AugmentationMode_NONE;
			return ai;
		}
	}

	// Find the key points.
	vector<KeyPoint> image_keypoints;
	static vector<KeyPoint> marker_keypoints;
	featureDetector->detect(img, image_keypoints);
	if (newMarker)
	{
		marker_keypoints.clear();
		featureDetector->detect(marker, marker_keypoints);
	}
	
	// Variables to hold the extracted keypoint feature information.
	Mat image_descriptors;
	static Mat marker_descriptors;
	
	try
	{
		// Extract the keypoints.
		descriptorExtractor->compute(img, image_keypoints, image_descriptors);
		if (newMarker)
		{
			descriptorExtractor->compute(marker, marker_keypoints, marker_descriptors);
		}
	}
	catch(Exception e)
	{
		// Debugging problems with BRIEF can remove this code.
		// If you find features using SURF and then extract with BRIEF then because the distance is floating point and BRIEF rounds up to the nearest pixel BRIEF can go out of bounds on the image size.
		float maxX = 0;
		float maxY = 0;

		float sX = 0;
		float sY = 0;
		for(int i = 0; i < image_keypoints.size(); i++)
		{
			if (image_keypoints[i].pt.x > maxX)
			{
				maxX = image_keypoints[i].pt.x;
				sX = image_keypoints[i].size;
			}
			if (image_keypoints[i].pt.y > maxY)
			{
				maxY = image_keypoints[i].pt.y;
				sY = image_keypoints[i].size;
			}
		}

		return ai;
	}


	// Display the keypoints.
	if (displayKeypoints)
	{
		int radius  = 5;
		bool showSize = false;
		
		int width = image.size().width + marker.size().width;
		int height = (image.size().height >  marker.size().height) ? image.size().height :  marker.size().height ;
		Mat debugImage(height, width, image.type());
		
		Mat roi(debugImage, Rect(0, 0, image.size().width, image.size().height));
		image.copyTo(roi);
		Mat roi2(debugImage, Rect(image.size().width, 0, marker.size().width, marker.size().height));
		marker.copyTo(roi2);

		for(int i=0; i < image_keypoints.size(); i++)
		{
			if (showSize)
			{
				radius = image_keypoints[i].size;
			}
			circle(debugImage, image_keypoints[i].pt, radius, Scalar(0, 0, 255));
		}
	
		for(int i=0; i < marker_keypoints.size(); i++)
		{
			if (showSize)
			{
				radius = marker_keypoints[i].size;
			}
			circle(debugImage, marker_keypoints[i].pt + Point2f(image.size().width, 0), radius, Scalar(0, 0, 255));
		}

		ai.liveImage = debugImage;
		ai.augmentationMode = AugmentationMode_NONE;
		return ai;
	}


	// Find corresponding keypoints (i.e. match points from one image to the other).
	vector<DMatch> matches;
    descriptorMatcher->match(image_descriptors, marker_descriptors, matches);
	
	// If we haven't found any matches return.
	if (matches.size() <= 10)
	{
		return ai;
	}

	// Convert from a list of matches to 2 lists of corresponding points.
	vector<Point2f> markerMatch; 
	vector<Point2f> imageMatch;
    for( size_t i = 0; i < matches.size(); i++ )
    {
		imageMatch.push_back(image_keypoints[matches[i].queryIdx].pt);
		markerMatch.push_back(marker_keypoints[matches[i].trainIdx].pt);
    }
	
	// Convert to matrix
	Mat markerMatchMatrix = Mat(markerMatch);
	Mat imageMatchMatrix = Mat(imageMatch);
	
	// Use RANSAC to find the homography.
	const double ransacReprojThreshold = 10;
	vector<uchar> ransacMatches;
    Mat H = findHomography(markerMatchMatrix, imageMatchMatrix, ransacMatches, CV_RANSAC, ransacReprojThreshold);
	
	if(H.empty())	
	{
		return ai;
	}
		
	// Display the matches and RANSAC matches.
	if (displayMatches || displayRansac)
	{
		Mat debugImage(image.size(), image.type());

		if (!displayRansac) // Draw matches
		{
			drawMatches(img, image_keypoints, marker, marker_keypoints, matches, debugImage, CV_RGB(255, 0, 0), CV_RGB(0, 255, 0));
		}
		else	// Draw RANSAC inliers.
		{
			vector<char> matchesMask(matches.size(), 0);
	
			Mat markerMatchTransformed; 
			perspectiveTransform(Mat(markerMatch), markerMatchTransformed, H);
			for(size_t i1 = 0; i1 < markerMatch.size(); i1++ )
			{
				if(norm(imageMatch[i1] - markerMatchTransformed.at<Point2f>((int)i1,0)) < ransacReprojThreshold)
				{
					matchesMask[i1] = 1;		// Inlier
				}
			}

			drawMatches(img, image_keypoints, marker, marker_keypoints, matches, debugImage, CV_RGB(255, 0, 0), CV_RGB(0, 255, 0), matchesMask);
		}
		drawHomography(debugImage, H, marker.size(), CV_RGB(0, 0, 255), 5);

		ai.liveImage = debugImage;
		ai.augmentationMode = AugmentationMode_NONE;
		return ai;
	}

	// Count the ransac matches so we can exit if we didn't find enough matches.
	int ransacMatchCount = 0;
	for(int i = 0; i < ransacMatches.size(); i++)
	{
		if (ransacMatches[i] == 1)
		{
			ransacMatchCount++;
		}
	}

	// Make sure that we have aleast a good number of points used
	// to generate our homography or else quit to indicate the marker
	// couldn't be found.
	if (ransacMatchCount < minimumMatchingPoints)
	{
		ai.augmentationMode = AugmentationMode_NONE;
		return ai;
	}

	// Turn the homography into the cameras extrinsic pramaters 
	// (find the rotation and translation of the object from the camera).
	Mat rotation;
	Mat translation;
	getExtrinsicsFromHomography(H, rotation, translation);	
	//getExtrinsicsFromPoints(ransacMatches, markerMatch, imageMatch, rotation, translation); // DONT USE THIS METHOD, IT WAS USED TO TEST THE ABOVE BUT IS INFERIOR.

	// The tranlation corresponds to the origin, which is at the corner of the marker
	// but I would like to define the origin so that it is at the center of the marker
	// so I need to offset by half of the size of the marker and need to multiply it by
	// the rotation so that it is in the local coordinate system of the marker.
	double offsetA[3][1] = {{marker.size().width/2}, {marker.size().height/2}, {0}};
	Mat offset(3, 1, CV_64FC1, offsetA);
	translation = translation + rotation*offset;

	// This is the scale the maps from pixel coordinates to our OpenGL world coordinates.
	translation = translation / naturalMarkerScale;
	
	// Turn the intrinsic and extrinsic paramaters into the OpenGL projection and modelview matrices.
	generateProjectionModelview(calibrationMatrix, rotation, translation, ai.projection, ai.modelview);

	ai.liveImage = img;

	return ai;
}


/**
* @brief An alternate method of computing the extrinsics from the RANSAC matches.
* @param ransacMatches The matches found using RANSAC.
* @param markerMatch The matching points from the marker image.
* @param image the matching points from the source iamge.
* @param rotation The extrinsic camera rotation.
* @param translation The extrinsic camera translation.
*
* DONT USE THIS METHOD, use getExtrinsicsFromHomography instead. This is just saved for future debugging etc.
* And also for historys sake, it was laughable at the time that I had written this feature two different ways
* to get the same result that didn't seem to work, even though the both actually did and it was just the display.
*/
void getExtrinsicsFromPoints(vector<uchar> ransacMatches, vector<Point2f> markerMatch, vector<Point2f> imageMatch, cv::Mat& rotation, cv::Mat& translation)
{	
	vector<Point2f> imgPts;
	vector<Point3f> objPts;

	for(int i = 0; i < ransacMatches.size(); i++)
	{
		if(ransacMatches[i] == 1)
		{
			Point2f tempImagePoint = imageMatch[i];
			imgPts.push_back(tempImagePoint);

			Point2f tempObjPoint = markerMatch[i];
			Point3f tempObjPoint3;
			tempObjPoint3.x = tempObjPoint.x;
			tempObjPoint3.y = tempObjPoint.y;
			tempObjPoint3.z = 0;
			objPts.push_back(tempObjPoint3);
		}
		
	}
	
	Mat rotationRodrigues;
	solvePnP(Mat(objPts), Mat(imgPts), calibrationMatrix, calibrationDistortionCoefficients, rotationRodrigues, translation);
	
	Rodrigues(rotationRodrigues, rotation);
	
	// cout << rotation << "\n";
	// cout << translation << "\n";
}
