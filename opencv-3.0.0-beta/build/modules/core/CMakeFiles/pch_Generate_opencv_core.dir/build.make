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

# Utility rule file for pch_Generate_opencv_core.

# Include the progress variables for this target.
include modules/core/CMakeFiles/pch_Generate_opencv_core.dir/progress.make

modules/core/CMakeFiles/pch_Generate_opencv_core: modules/core/precomp.hpp.gch/opencv_core_Release.gch

modules/core/precomp.hpp.gch/opencv_core_Release.gch: ../modules/core/src/precomp.hpp
modules/core/precomp.hpp.gch/opencv_core_Release.gch: modules/core/precomp.hpp
modules/core/precomp.hpp.gch/opencv_core_Release.gch: lib/libopencv_core_pch_dephelp.a
	$(CMAKE_COMMAND) -E cmake_progress_report /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating precomp.hpp.gch/opencv_core_Release.gch"
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/core && /usr/bin/cmake -E make_directory /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/core/precomp.hpp.gch
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/core && /usr/bin/c++ -O3 -DNDEBUG -DNDEBUG -fPIC -DOPENCV_NOSTL -isystem"/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/3rdparty/include/opencl/1.2" -isystem"/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/3rdparty/ippicv/unpack/ippicv_lnx/include" -isystem"/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build" -isystem"/usr/include" -isystem"/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/3rdparty/include/opencl/1.2" -isystem"/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/3rdparty/ippicv/unpack/ippicv_lnx/include" -isystem"/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build" -isystem"/usr/include" -I"/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/modules/core/include" -I"/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/modules/core/src" -isystem"/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/core" -I"/home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/modules/core/include" -isystem"/usr/include" -D__OPENCV_BUILD=1 -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -Wno-narrowing -Wno-delete-non-virtual-dtor -fdiagnostics-show-option -Wno-long-long -pthread -fomit-frame-pointer -msse -msse2 -msse3 -ffunction-sections -fvisibility=hidden -fvisibility-inlines-hidden -DCVAPI_EXPORTS -x c++-header -o /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/core/precomp.hpp.gch/opencv_core_Release.gch /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/core/precomp.hpp

modules/core/precomp.hpp: ../modules/core/src/precomp.hpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating precomp.hpp"
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/core && /usr/bin/cmake -E copy /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/modules/core/src/precomp.hpp /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/core/precomp.hpp

pch_Generate_opencv_core: modules/core/CMakeFiles/pch_Generate_opencv_core
pch_Generate_opencv_core: modules/core/precomp.hpp.gch/opencv_core_Release.gch
pch_Generate_opencv_core: modules/core/precomp.hpp
pch_Generate_opencv_core: modules/core/CMakeFiles/pch_Generate_opencv_core.dir/build.make
.PHONY : pch_Generate_opencv_core

# Rule to build all files generated by this target.
modules/core/CMakeFiles/pch_Generate_opencv_core.dir/build: pch_Generate_opencv_core
.PHONY : modules/core/CMakeFiles/pch_Generate_opencv_core.dir/build

modules/core/CMakeFiles/pch_Generate_opencv_core.dir/clean:
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/core && $(CMAKE_COMMAND) -P CMakeFiles/pch_Generate_opencv_core.dir/cmake_clean.cmake
.PHONY : modules/core/CMakeFiles/pch_Generate_opencv_core.dir/clean

modules/core/CMakeFiles/pch_Generate_opencv_core.dir/depend:
	cd /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/modules/core /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/core /home/ax/ownCloud/SS15/ETH/3DPhotography/AugmentedRealityChess/opencv-3.0.0-beta/build/modules/core/CMakeFiles/pch_Generate_opencv_core.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : modules/core/CMakeFiles/pch_Generate_opencv_core.dir/depend

