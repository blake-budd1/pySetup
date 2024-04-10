# Raspodify installation
sudo apt-get -y install curl && curl -sL https://dtcooper.github.io/raspotify/install.sh | sh

# Spotipy installation
pip install spotipy --upgrade --break-system-packages

# OpenCV installation
pip install opencv-python --break-system-packages
pip install opencv-contrib-python --break-system-packages

# SFML Installation
sudo apt-get install libsfml-dev 

# Remote Packages install
sudo apt-get install cec-utils
sudo apt-get install xdotool

# Create the necessary files for file storage on the device
# Add this back eventually if we need it
