#!/bin/bash

# Run the first python script to get the current song and handle updating the queue
echo "Running python script to update queue"
cd python_scripts
python3 queue_handling.py

# Run the spotify_play script to start playback on the raspberry pi
python3 spotify_play.py&

# Run the C++ script
cd ..
cd sfml_programs
g++ -c main.cpp
g++ main.o -o sfml-app -lsfml-graphics -lsfml-window -lsfml-system
./sfml-app

echo "Scripts executed successfully."
exit 0
