# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.25

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
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
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/alexacole/Documents/pySetup

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/alexacole/Documents/pySetup/build

# Include any dependencies generated for this target.
include CMakeFiles/sfml_programs.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/sfml_programs.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/sfml_programs.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/sfml_programs.dir/flags.make

CMakeFiles/sfml_programs.dir/main.cpp.o: CMakeFiles/sfml_programs.dir/flags.make
CMakeFiles/sfml_programs.dir/main.cpp.o: /home/alexacole/Documents/pySetup/main.cpp
CMakeFiles/sfml_programs.dir/main.cpp.o: CMakeFiles/sfml_programs.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/alexacole/Documents/pySetup/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/sfml_programs.dir/main.cpp.o"
	/usr/bin/aarch64-linux-gnu-g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/sfml_programs.dir/main.cpp.o -MF CMakeFiles/sfml_programs.dir/main.cpp.o.d -o CMakeFiles/sfml_programs.dir/main.cpp.o -c /home/alexacole/Documents/pySetup/main.cpp

CMakeFiles/sfml_programs.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/sfml_programs.dir/main.cpp.i"
	/usr/bin/aarch64-linux-gnu-g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/alexacole/Documents/pySetup/main.cpp > CMakeFiles/sfml_programs.dir/main.cpp.i

CMakeFiles/sfml_programs.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/sfml_programs.dir/main.cpp.s"
	/usr/bin/aarch64-linux-gnu-g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/alexacole/Documents/pySetup/main.cpp -o CMakeFiles/sfml_programs.dir/main.cpp.s

# Object files for target sfml_programs
sfml_programs_OBJECTS = \
"CMakeFiles/sfml_programs.dir/main.cpp.o"

# External object files for target sfml_programs
sfml_programs_EXTERNAL_OBJECTS =

sfml_programs: CMakeFiles/sfml_programs.dir/main.cpp.o
sfml_programs: CMakeFiles/sfml_programs.dir/build.make
sfml_programs: CMakeFiles/sfml_programs.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/alexacole/Documents/pySetup/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable sfml_programs"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/sfml_programs.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/sfml_programs.dir/build: sfml_programs
.PHONY : CMakeFiles/sfml_programs.dir/build

CMakeFiles/sfml_programs.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/sfml_programs.dir/cmake_clean.cmake
.PHONY : CMakeFiles/sfml_programs.dir/clean

CMakeFiles/sfml_programs.dir/depend:
	cd /home/alexacole/Documents/pySetup/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/alexacole/Documents/pySetup /home/alexacole/Documents/pySetup /home/alexacole/Documents/pySetup/build /home/alexacole/Documents/pySetup/build /home/alexacole/Documents/pySetup/build/CMakeFiles/sfml_programs.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/sfml_programs.dir/depend
