#!/usr/bin/env python
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import requests
import urllib.request
import cv2
import json
import re
import os

MJ_URL = "http://the-modern-jukebox-react-app.vercel.app/api/queue"
DEVICE_ID = "98bb0735e28656bac098d927d410c3138a4b5bca"
CLIENT_ID = "62d7db029474470d9910002d8e2c71fa"
CLIENT_SECRET = "62d6fbba1a794b55a5be7e83216ddc5f"
CURRENT_SONG_PATH = "../temp_files/current_song.txt"
PREVIOUS_SONG_PATH = "../temp_files/previous_songs.txt"
CURRENT_SLEEP_PATH = "../temp_files/current_sleep.txt"

# Setup spotify for playback
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://localhost:8080",
    scope="user-read-playback-state,user-modify-playback-state",
    cache_path='./tokens.txt'
))

# Force a transfer device to playback on the raspberry pi from Spotify
print("transferring device")
sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

while True:  # Infinite loop for continuous execution
    try:
        # Read the sleep duration from the file
        with open(CURRENT_SLEEP_PATH, "r") as sleep_file:
            sleep_duration = float(sleep_file.readline().strip())

        # Read the URI from the current song file
        with open(CURRENT_SONG_PATH, "r") as file:
            # Read the first line of the file (the URI)
            song_uri = file.readline()
            # Read the last line of the file (the duration in seconds)
            # Remove the new line at the end of the song URI since we read it in from a file
            modified_uri = song_uri.rstrip('\n')

            print(modified_uri)
            print([modified_uri])
        
        # Start playback with the retrieved URI
        sp.start_playback(device_id=DEVICE_ID, uris=[modified_uri])

        # Need to place the current song into the previous songs file
        # Go back into current song file and store each line:
        with open(CURRENT_SONG_PATH, "r") as file:
            lines = file.readlines()
            print("****** Printing lines from current song file ****** \n")
            for line in lines:
                # Strip is necessary to get rid of the new line character
                print(line.strip())

        # Sleep for the song duration (so the whole song plays)
        # sleep(float(lines[7]) - 10)

        # Need to remove the current song from the current_song.txt
        # need to write the first two objects (uri and image (stored on py)) into the previous_songs.txt file
        with open(PREVIOUS_SONG_PATH, "w") as file:
            # These already have new lines at the end
            file.write(lines[0])  # write the song uri
            file.write(lines[1])  # write the path to the album cover

        # Sleep for the specified duration before repeating the process
        sleep(sleep_duration)

    except Exception as ex:
        print("An unexpected error occurred:", str(ex))