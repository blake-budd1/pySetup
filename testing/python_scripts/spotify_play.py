#!/usr/bin/env python
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import requests
import urllib.request
import cv2
import json
#import screeninfo
#import pyautogui
import re
import os
# Current issue is this is empty, returning 200 code but still has nothing in it
MJ_URL = "http://the-modern-jukebox-react-app.vercel.app/api/queue"
# chrome 
# DEVICE_ID="4edff9361f1dc0e531dd37586d86707511975dbd" # raspodify device ID (works on hotspot right now)
# raspodify
DEVICE_ID="98bb0735e28656bac098d927d410c3138a4b5bca"

# This device id is going to change once I reflashed the OS for raspberry pi.
CLIENT_ID="62d7db029474470d9910002d8e2c71fa"
CLIENT_SECRET="62d6fbba1a794b55a5be7e83216ddc5f"
CURRENT_SONG_PATH = "../temp_files/current_song.txt"
PREVIOUS_SONG_PATH = "../temp_files/previous_songs.txt"


# Setup spotify for playback
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                    client_secret=CLIENT_SECRET,
                                                    redirect_uri="http://localhost:8080",
                                                    scope="user-read-playback-state,user-modify-playback-state",
                                                    cache_path='./tokens.txt'))
# Force a transfer device to playback on the raspberry pi from Spotify
print("transfering device")
sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

# Read in the URI that is in the temp file ("current_song.txt")

######## NOTE: This assumes the last line ends with a new character (if not, update in PyScriptOne_Final.py)

with open(CURRENT_SONG_PATH, "r") as file:
    # Read the first line of the file (the URI)
    song_uri = file.readline()
    # Read the last line of the file (the duration in seconds)
    # Remove the new line at the end of the song URI since we read it in from a file
    modified_uri = song_uri.rstrip('\n')

    print(modified_uri)
    print([modified_uri])
sp.start_playback(device_id = DEVICE_ID, uris = [modified_uri])


# Need to place the current song into the previous songs file
# Go back into current song file and store each line:
with open(CURRENT_SONG_PATH, "r") as file:
    lines = file.readlines()
    print("****** Printing lines from currentsong file ****** \n")
    for line in lines:
        # Strip is necessary to get rid fo the new line character
        print(line.strip())


# sleep for the song duration (so the whole song plays)
sleep(float(lines[7]) - 10)
# Need to remove the current song from the current_song.txt
# need to write the first two objects (uri and image (stored on py)) into the previous_songs.txt file
with open(PREVIOUS_SONG_PATH, "w") as file:
    # These already have new lines at the end
    file.write(lines[0]) # write the song uri
    file.write(lines[1]) # write the path to the album cover
