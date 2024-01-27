#!/bin/bash

# Function to run sfml script
run_cpp_program() {
    cd sfml_programs
    g++ -c main.cpp
    g++ main.o -o sfml-app -lsfml-graphics -lsfml-window -lsfml-system
    ./sfml-app
    cd ..
}

# Function to handle cleanup
cleanup() {
    echo "Caught Ctrl+C, cleaning up..."
    # Add cleanup actions here if needed
    exit 0
}

# Trap Ctrl+C signal
trap cleanup SIGINT

# Loop
while true; do
    echo "Running queue Python script"
    cd python_scripts
    python3 queue_handling.py
    cd ..

    echo "Running sfml script"
    run_cpp_program

    echo "Starting playback on Raspberry Pi"
    cd python_scripts
    python3 spotify_play.py
    cd ..

    # Read the sleep duration from the file
    sleep_duration=$(<temp_files/current_sleep.txt)

    # Ensure sleep duration is a non-negative integer
    if [[ $sleep_duration =~ ^[0-9]+$ ]]; then
        usleep "$sleep_duration"
    else
        echo "Invalid sleep duration: $sleep_duration"
        cleanup
    fi
done
