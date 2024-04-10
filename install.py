# Raspodify installation
sudo apt-get -y install curl && curl -sL https://dtcooper.github.io/raspotify/install.sh | sh

# Spotipy installation
pip install spotipy
pip install spotipy --upgrade

# OpenCV installation
pip install opencv-python
pip install opencv-contrib-python

# SFML Installation
sudo apt-get install libsfml-dev

# Remote Packages install
sudo apt-get install cec-utils
sudo apt-get install xdotool

# Creating the directory structure for the project:
mkdir -p /home/pi/modern_jukebox
mkdir -p /home/pi/modern_jukebox/temp_files
mkdir -p /home/pi/modern_jukebox/python_files
mkdir -p /home/pi/modern_jukebox/c_files

# Create the necessary files for file storage on the device
cd /home/pi/modern_jukebox/temp_files
touch current_song.txt next_song.txt next_songs.txt previous_songs.txt sfml_controller.txt
