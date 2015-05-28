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

You can use the OpenCV versio 2.4.9.

For example

`cd ~/<my_working_directory>`  
`git clone https://github.com/Itseez/opencv.git`   
`git clone https://github.com/Itseez/opencv_contrib.git`  

####Building OpenCV 2.4.9 from Source Using CMake

1. Create a temporary directory, which we denote as <cmake_build_dir>, where you want to put the generated Makefiles, project files as well the object files and output binaries and enter there.
For example  
`cd ~/opencv2.4.9`  
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

### Install Ros
1. Installation  
1.1. Configure your Ubuntu repositories Configure your Ubuntu repositories to allow "restricted," "universe," and "multiverse." You can follow the Ubuntu guide for instructions on doing this.  
1.2. Setup your sources.list
Setup your computer to accept software from packages.ros.org. ROS Jade ONLY supports Trusty (14.04), Utopic (14.10) and Vivid (15.04) for debian packages.`sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list`  
1.3. Set up your keys
`sudo apt-key adv --keyserver hkp://pool.sks-keyservers.net --recv-key 0xB01FA116`  
1.4. Installation
 First, make sure your Debian package index is up-to-date:
`sudo apt-get update`
If you are using Ubuntu Trusty **14.04.2** and experience dependency issues during the ROS installation, you may have to install some additional system dependencies.
**/!\ Do not install these packages if you are using 14.04, it will destroy your X server:**
`sudo apt-get install xserver-xorg-dev-lts-utopic mesa-common-dev-lts-utopic libxatracker-dev-lts-utopic libopenvg1-mesa-dev-lts-utopic libgles2-mesa-dev-lts-utopic libgles1-mesa-dev-lts-utopic libgl1-mesa-dev-lts-utopic libgbm-dev-lts-utopic libegl1-mesa-dev-lts-utopic`
**/!\ Do not install the above packages if you are using 14.04, it will destroy your X server**
Alternatively, try installing just this to fix dependency issues:
`sudo apt-get install libgl1-mesa-dev-lts-utopic`
Desktop-Full Install: (Recommended) : ROS, rqt, rviz, robot-generic libraries, 2D/3D simulators, navigation and 2D/3D perception
sudo apt-get install ros-jade-desktop-full
or click here
Desktop Install: ROS, rqt, rviz, and robot-generic libraries
`sudo apt-get install ros-jade-desktop`
ROS-Base: (Bare Bones) ROS package, build, and communication libraries. No GUI tools.
`sudo apt-get install ros-jade-ros-base`
Individual Package: You can also install a specific ROS package (replace underscores with dashes of the package name):
`sudo apt-get install ros-jade-PACKAGE`
e.g.
`sudo apt-get install ros-jade-slam-gmapping`
To find available packages, use:
`apt-cache search ros-jade`   
1.5. Initialize rosdep
Before you can use ROS, you will need to initialize rosdep. rosdep enables you to easily install system dependencies for source you want to compile and is required to run some core components in ROS.
`sudo rosdep init
rosdep update`  
1.6. Environment setup
It's convenient if the ROS environment variables are automatically added to your bash session every time a new shell is launched:

`echo "source /opt/ros/jade/setup.bash" >> ~/.bashrc
source ~/.bashrc`
If you have more than one ROS distribution installed, ~/.bashrc must only source the setup.bash for the version you are currently using.

If you just want to change the environment of your current shell, you can type:

`source /opt/ros/jade/setup.bash`  
1.7. Getting rosinstall
rosinstall is a frequently used command-line tool in ROS that is distributed separately. It enables you to easily download many source trees for ROS packages with one command.

To install this tool on Ubuntu, run:

`sudo apt-get install python-rosinstall`
Build farm status
The packages that you installed were built by ROS build farm. 

### Install PyOpenGL
To be able to run the animations you new to have PyOpenGL, the quickest way to install it 
is using pip   
`$ pip install PyOpenGL PyOpenGL_accelerate`


### Set up Augmented Reality Chess
To run the source code properly a specific file structure is needed.      

1. Create a catkin workspace `cd ~; mkdir ~/catkin_ws`
2. Clone the ros part of the implementation in this directory `git clone https://github.com/alexus37/ROSARCHESS.git`
3. Clone the rendering part in an arbitary folder and link the path in the file catkin_ws/src/kinect_io/scripts/listener.py `git clone https://github.com/alexus37/AugmentedRealityChess.git`
4. Calibrate the Kinect camera using the `ros CALI BLA` to create the a cali.yml file
5. Calibrate the IR camera and create the a cali.yml file


### Run the game
1. Run the roscore `roscore`
2. Open a new terminal and run openNi to be able to interact with the kinnect `ROS BLAA`
3. Open a new terminal and run ros_arsys to be able to track the markers `ROS BLAA`
4. connecte via ssh to connect to the thermal camera. `shh px4@192.168.1.2`
5. Also run the roscore on the IR cam `roscore`
6. Run the command `rosrun px4 px4`
7. Launch the video stream `roslauch VIDEO BLA`
8. Open a new terminal on your machine and run the listener `ros launch BLA LISTNER`
