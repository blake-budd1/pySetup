#!/bin/bash
# function to run sfml script
run_cpp_program()
{
    cd sfml_programs
    g++ -c main.cpp
    g++ main.o -o sfml-app -lsfml-graphics -lsfml-window -lsfml-system
    ./sfml-app
}

# Loop
while true; do
    echo "running queue pythons script\n"
    cd python_scripts
    python3 queue_handling.py &

    echo "running sfml script\n"
    cd ..
    run_cpp_program &
    

    echo "starting playback on raspberry pi. \n"
    cd ../python_scripts
    python3 spotify_play.py &

    cd ../temp_files
    sleep_duration=$(<current_sleep.txt)
    usleep "$((sleep_duration))"
done