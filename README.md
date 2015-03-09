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
These steps have been tested for Ubuntu 14.04 but should work with other distros as well.
#### Required Packages
1. GCC 4.4.x or later
2. CMake 2.8.7 or higher
3. Git
4. GTK+2.x or higher, including headers (libgtk2.0-dev)
5. pkg-config
5. Python 2.6 or later and Numpy 1.5 or later with developer packages (python-dev, python-numpy)
6. ffmpeg or libav development packages: libavcodec-dev, libavformat-dev, libswscale-dev
7. [optional] libtbb2 libtbb-dev
8. [optional] libdc1394 2.x
9. [optional] libjpeg-dev, libpng-dev, libtiff-dev, libjasper-dev, libdc1394-22-dev
The packages can be installed using a terminal and the following commands or by using Synaptic Manager:

[compiler] `sudo apt-get install build-essential`   
[required] `sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev`   
[optional] `sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev`   

#### Getting OpenCV Source Code

You can use the latest stable OpenCV version or you can grab the latest snapshot from our Git repository.

Getting the Latest Stable OpenCV Version
Go to our downloads page.
Download the source archive and unpack it.
Getting the Cutting-edge OpenCV from the Git Repository
Launch Git client and clone OpenCV repository. If you need modules from OpenCV contrib repository then clone it too.

For example

`cd ~/<my_working_directory>`  
`git clone https://github.com/Itseez/opencv.git`   
`git clone https://github.com/Itseez/opencv_contrib.git`  

####Building OpenCV from Source Using CMake

1. Create a temporary directory, which we denote as <cmake_build_dir>, where you want to put the generated Makefiles, project files as well the object files and output binaries and enter there.
For example  
`cd ~/opencv`  
`mkdir build`  
`cd build`  
2. Configuring. Run cmake [some optional parameters] path to the OpenCV source directory  
For example  
`cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..`
or `cmake-gui`  
   * set full path to OpenCV source code, e.g. /home/user/opencv
   * set full path to <cmake_build_dir>, e.g. /home/user/opencv/build
   * set optional parameters
   * run: “Configure”
   * run: “Generate”
3. Description of some parameters
   * build type: CMAKE_BUILD_TYPE=Release\Debug
   * to build with modules from opencv_contrib set OPENCV_EXTRA_MODULES_PATH to <path to opencv_contrib/modules/>
   * set BUILD_DOCS for building documents
   * set BUILD_EXAMPLES to build all examples
4. Building python. Set the following python parameters:
   * PYTHON2(3)_EXECUTABLE = <path to python>
   * PYTHON_INCLUDE_DIR = /usr/include/python<version>
   * PYTHON_INCLUDE_DIR2 = /usr/include/x86_64-linux-gnu/python<version>
   * PYTHON_LIBRARY = /usr/lib/x86_64-linux-gnu/libpython<version>.so
   * PYTHON2(3)_NUMPY_INCLUDE_DIRS = /usr/lib/python<version>/dist-packages/numpy/core/include/

5. Build. From build directory execute make, recomend to do it in several threads
For example  
`make -j7 # runs 7 jobs in parallel`   

6. `sudo make install`
