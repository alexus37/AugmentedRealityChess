# AugmentedRealityChess
The goal of this project is to create a augmented reality board game
## How to run the Kinect on Ubuntu 14.04 

### Install OpenNI 
This is required for the kinect interface   
`sudo apt-get install git-core cmake freeglut3-dev pkg-config build-essential libxmu-dev libxi-dev libusb-1.0-0-dev doxygen graphviz mono-complete`  
Now clone the code and set it up  
`$ mkdir ~/kinect`  
`$ cd ~/kinect`   
`$ git clone https://github.com/OpenNI/OpenNI.git`   
    
This thing has a bizarre install scheme. Do the following:  
`cd OpenNI/Platform/Linux/CreateRedist/`   
`chmod +x RedistMaker`   
`./RedistMaker`
Now this creates some distribution. One of the two following cases should work. Else just look for a damn compiled binary, extract it and install it.    
Case 1:   
`$ cd Final`  
`$ tar -xjf OpenNI-Bin-Dev-Linux*bz2`  
`$ cd OpenNI- ...`   
`$ sudo ./install.sh`   

### Install SensorKinect 
Yet another library for the Kinect
`$ cd ~/kinect/`   
`$ git clone git://github.com/ph4m/SensorKinect.git`   
Once you have the lib, go ahead and compile it in the same bizarre manner as OpenNI (well atleast they are consistent).   
`$ cd SensorKinect/Platform/Linux/CreateRedist/ `   
`$ chmod +x RedistMaker`   
`$ ./RedistMaker`   
Done compiling. Now install this.  
`$ cd Final`  
`$ tar -xjf Sensor ...`  
`$ cd Sensor ...`  
`$ sudo ./install.sh`  
### Set up OpenCV
Install a bunch of related libraries.

`sudo apt-get install build-essential cmake cmake-qt-gui qt5-default libvtk6-dev zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libjasper-dev libopenexr-dev libgdal-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libfaac-dev libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine-dev libtbb-dev python-dev python-tk python-numpy python3-dev python3-tk python3-numpy`   
Download [OpenCV]("http://opencv.org/")   
Extract then build   
`$ cd opencv-2 ...`   
`$ mkdir build`   
`$ cmake-gui ..`   
Next you will need to use the gui to configure cmake flags for OpenCV  
Note that you should check just about every option in the cmake gui list (ones that make sense of course)   
This is annoying because OpenCV will take hours to compile and if you miss one flag, you might have to re-do everything.  
After the cmake set up, compile the code  
`$ make -j`   
Once you are done with the build, install it   
`$ sudo make install`   