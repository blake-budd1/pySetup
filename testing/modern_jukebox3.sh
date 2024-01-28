#!/bin/bash

rm -f /home/blake/Desktop/testing/temp_files/*.txt
rm -f /home/blake/Desktop/testing/album_covers/*.JPEG

# Function to run sfml script
run_cpp_program() {
    cd /home/blake/Desktop/testing/sfml_programs
    g++ -c main2.cpp
    g++ main2.o -o sfml-app -lsfml-graphics -lsfml-window -lsfml-system
    ./sfml-app
}

cleanup()
{
    echo "caught ctrl+c, cleaning up"
    exit 0
}

cd /home/blake/Desktop/testing/python_scripts
python3 queue_handling2.py  &


run_cpp_program &


cd /home/blake/Desktop/testing/python_scripts
python3 spotify_play2.py &

trap cleanup SIGINT
