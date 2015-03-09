/** @file AugmentedReality.hpp
* @author Ashley Stacey
* @note Copyright © Ashley Stacey 2011
* @version 1.0.2
* @date Created: 15/06/2011
* @date Modified: 10/08/2011
* @brief Augmented Reality program for assigment for Computer Vision.
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


#include "opencv/cv.h"
#include "opencv/highgui.h"

#include "GL/glut.h"
//#include "GL/freeglut.h"

#include <ctime>

#include <iostream>
#include <queue>
#include <vector>


enum DisplayMethod		// Used to represent what display method should be used.
{
	DisplayMethod_GLUT,
	DisplayMethod_OPEN_CV
};

enum SelectionMode		// Used to indicate which selection mode we are using.
{
	SelectionMode_Points,
	SelectionMode_Region
};

enum AugmentationMode	// Used to indicate what augmentation method is required.
{
	AugmentationMode_NONE,
	AugmentationMode_IMAGE,
	AugmentationMode_SELECTION,
	AugmentationMode_3D
};

enum AugmentationModel	// Used to represent which model should be used.
{
	AugmentationModel_Teapot_Static,
	AugmentationModel_Teapot_Dynamic,
	AugmentationModel_Tower_Static,
};

struct AugmentationInformation  // Used to hold information about the augmentation.
{
	cv::Mat liveImage;

	AugmentationMode augmentationMode;
	AugmentationModel augmentationModel;

	cv::Mat projection;
	cv::Mat modelview;
};



void debugInit();

int main(int args, char** argv);

cv::Mat grabFrame(bool flushBuffer = false, bool lastFrame = false);
AugmentationInformation processFrame(int method, cv::Mat rawCapturedImage);

void initialiseGLUT();
void initialiseOpenGL();
void displayGLUT();

void displayOpenCV(cv::Mat augmentedImage);

void renderBackgroundGL(const cv::Mat& image);
void drawFPS(float fps);
void renderSceneGL(AugmentationModel m);
void drawStaticTeapotGL();
void drawDynamicTeapotGL();
void drawStaticTowerGL();

GLfloat* convertMatrixType(const cv::Mat& m);

void clearSelection();
void selectPoint(int x, int y);
void selectRegion(int x1, int y1, int x2, int y2);
void drawSelectionMarker(float size, float locationX, float locationY);
void drawSelectionRegion(float locationX1, float locationY1, float locationX2, float locationY2);
void drawSelection();

bool keypress(unsigned char key, int x, int y);
void mouseClick(int x, int y);
void mouseDrag(bool pressedValid, bool pressed, int x, int y);
void keyboardGLUT(unsigned char key, int x, int y);
void mouseGLUT(int button, int state, int x, int y);
void mouseMotionGLUT(int x, int y);

void toggleUseHeldImage();
void setHoldImage();
void toggleSubPixelAccuracy();
void changeNaturalImageMarker();

void saveHeldImage();

void addToCalibrationImages();
std::string intToString(int i);
void saveCalibrationImages();
void loadCalibrationImages();

void calibrate(bool subPixel = true);

void buildChessboardCornerPoints(std::vector<cv::Point3f>* corners, float scale);

void improveCornerAccuracy(const cv::Mat& image, std::vector<cv::Point2f>& corners);

void getExtrinsicsFromHomography(cv::Mat H, cv::Mat& rotation, cv::Mat& translation);
void generateProjectionModelview(const cv::Mat& calibration, const cv::Mat& rotation, const cv::Mat& translation, cv::Mat& projection, cv::Mat& modelview);

void drawHomography(cv::Mat& image, cv::Mat& H, cv::Size s, cv::Scalar colour, int thickness = 1, int lineType = 8, int shift = 0);

float calcDistance(cv::Point2f p1, cv::Point2f p2);
int clamp(int value, int min, int max);
cv::Mat selectionTransform(const cv::Mat& image, bool maintainSize);

AugmentationInformation augmentationDoNothing(const cv::Mat& image);
AugmentationInformation augmentationChessPlanar(const cv::Mat& image, bool subPixel, bool overlayImage, bool modulate = false);
AugmentationInformation augmentationChessSurface(const cv::Mat& image, bool subPixel, bool overlayImage, bool modulate = false);
AugmentationInformation augmentationCalibrationImages(float frequency);
AugmentationInformation augmentationUndistort(const cv::Mat& image);
AugmentationInformation augmentationCaptureMarker(const cv::Mat& image);
AugmentationInformation augmentationChess3D(cv::Mat& image, bool subPixel);
AugmentationInformation augmentationNaturalMarkers1(const cv::Mat& image, bool displayKeypoints, bool displayMatches, bool displayRansac);
