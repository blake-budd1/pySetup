#!/bin/bash

#rm -f /home/blake/Desktop/testing/temp_files/*.txt
rm -f /home/blake/Desktop/testing/album_covers/*.JPEG
# cd temp_files
# > current_sleep.txt
# > current_song.txt
# > previous_song.txt
# > next_song.txt

./clearFiles.sh

# Function to run sfml script
run_cpp_program() {
    cd /home/blake/Desktop/testing/sfml_programs
    g++ -c main2_v3.cpp
    g++ main2_v3.o -o sfml-app -lsfml-graphics -lsfml-window -lsfml-system
    ./sfml-app
}

cleanup()
{
    echo "caught ctrl+c, cleaning up"
    exit 0
}

cd /home/blake/Desktop/testing/python_scripts
python3 queue_handling_v3.py  &

# Run welcome screen
cd /home/blake/Desktop/testing/sfml_programs
g++ -c welcomeScreen.cpp
g++ welcomeScreen.o -o sfml-welcome -lsfml-graphics -lsfml-window -lsfml-system
./sfml-welcome



sleep 2
run_cpp_program &


cd /home/blake/Desktop/testing/python_scripts
python3 spotify_play_v3.py &

# bash script that needs to be ran to get the information for the remote.

# & runs it in it's own thread. 
python3 poll_website.py&
python3 buttons.py&
cd ../
cec-client | ./cecremote.sh&

trap cleanup SIGINT
