# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The program to use to edit the cache.
CMAKE_EDIT_COMMAND = /usr/bin/cmake-gui

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build

# Include any dependencies generated for this target.
include modules/highgui/CMakeFiles/opencv_highgui.dir/depend.make

# Include the progress variables for this target.
include modules/highgui/CMakeFiles/opencv_highgui.dir/progress.make

# Include the compile flags for this target's objects.
include modules/highgui/CMakeFiles/opencv_highgui.dir/flags.make

modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o: modules/highgui/CMakeFiles/opencv_highgui.dir/flags.make
modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o: ../modules/highgui/src/window.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o"
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui/precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_highgui.dir/src/window.cpp.o -c /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/modules/highgui/src/window.cpp

modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_highgui.dir/src/window.cpp.i"
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui/precomp.hpp" -Winvalid-pch  -E /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/modules/highgui/src/window.cpp > CMakeFiles/opencv_highgui.dir/src/window.cpp.i

modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_highgui.dir/src/window.cpp.s"
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui/precomp.hpp" -Winvalid-pch  -S /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/modules/highgui/src/window.cpp -o CMakeFiles/opencv_highgui.dir/src/window.cpp.s

modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o.requires:
.PHONY : modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o.requires

modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o.provides: modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o.requires
	$(MAKE) -f modules/highgui/CMakeFiles/opencv_highgui.dir/build.make modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o.provides.build
.PHONY : modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o.provides

modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o.provides.build: modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o

modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o: modules/highgui/CMakeFiles/opencv_highgui.dir/flags.make
modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o: ../modules/highgui/src/window_gtk.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o"
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui/precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o -c /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/modules/highgui/src/window_gtk.cpp

modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.i"
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui/precomp.hpp" -Winvalid-pch  -E /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/modules/highgui/src/window_gtk.cpp > CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.i

modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.s"
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui/precomp.hpp" -Winvalid-pch  -S /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/modules/highgui/src/window_gtk.cpp -o CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.s

modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o.requires:
.PHONY : modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o.requires

modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o.provides: modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o.requires
	$(MAKE) -f modules/highgui/CMakeFiles/opencv_highgui.dir/build.make modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o.provides.build
.PHONY : modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o.provides

modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o.provides.build: modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o

# Object files for target opencv_highgui
opencv_highgui_OBJECTS = \
"CMakeFiles/opencv_highgui.dir/src/window.cpp.o" \
"CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o"

# External object files for target opencv_highgui
opencv_highgui_EXTERNAL_OBJECTS =

lib/libopencv_highgui.so.3.0.0: modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o
lib/libopencv_highgui.so.3.0.0: modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o
lib/libopencv_highgui.so.3.0.0: modules/highgui/CMakeFiles/opencv_highgui.dir/build.make
lib/libopencv_highgui.so.3.0.0: lib/libopencv_core.so.3.0.0
lib/libopencv_highgui.so.3.0.0: lib/libopencv_imgproc.so.3.0.0
lib/libopencv_highgui.so.3.0.0: lib/libopencv_imgcodecs.so.3.0.0
lib/libopencv_highgui.so.3.0.0: lib/libopencv_videoio.so.3.0.0
lib/libopencv_highgui.so.3.0.0: ../3rdparty/ippicv/unpack/ippicv_lnx/lib/intel64/libippicv.a
lib/libopencv_highgui.so.3.0.0: lib/libopencv_imgcodecs.so.3.0.0
lib/libopencv_highgui.so.3.0.0: lib/libopencv_imgproc.so.3.0.0
lib/libopencv_highgui.so.3.0.0: lib/libopencv_core.so.3.0.0
lib/libopencv_highgui.so.3.0.0: modules/highgui/CMakeFiles/opencv_highgui.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX shared library ../../lib/libopencv_highgui.so"
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/opencv_highgui.dir/link.txt --verbose=$(VERBOSE)
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui && $(CMAKE_COMMAND) -E cmake_symlink_library ../../lib/libopencv_highgui.so.3.0.0 ../../lib/libopencv_highgui.so.3.0 ../../lib/libopencv_highgui.so

lib/libopencv_highgui.so.3.0: lib/libopencv_highgui.so.3.0.0

lib/libopencv_highgui.so: lib/libopencv_highgui.so.3.0.0

# Rule to build all files generated by this target.
modules/highgui/CMakeFiles/opencv_highgui.dir/build: lib/libopencv_highgui.so
.PHONY : modules/highgui/CMakeFiles/opencv_highgui.dir/build

modules/highgui/CMakeFiles/opencv_highgui.dir/requires: modules/highgui/CMakeFiles/opencv_highgui.dir/src/window.cpp.o.requires
modules/highgui/CMakeFiles/opencv_highgui.dir/requires: modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o.requires
.PHONY : modules/highgui/CMakeFiles/opencv_highgui.dir/requires

modules/highgui/CMakeFiles/opencv_highgui.dir/clean:
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui && $(CMAKE_COMMAND) -P CMakeFiles/opencv_highgui.dir/cmake_clean.cmake
.PHONY : modules/highgui/CMakeFiles/opencv_highgui.dir/clean

modules/highgui/CMakeFiles/opencv_highgui.dir/depend:
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/modules/highgui /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/highgui/CMakeFiles/opencv_highgui.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : modules/highgui/CMakeFiles/opencv_highgui.dir/depend

