#!/usr/bin/env python
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
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
CONTROLLER_PATH = "../remote.txt"
SYSTEM_QUEUE_CONTROLLER = "../system_queue_controller.txt"
SYSTEM_SFML_CONTROLLER = "../system_sfml_controller.txt"

def readController():
    command = ""
    with open(CONTROLLER_PATH, "r") as controller_file:
            controller = controller_file.readlines()
            if(controller):
                command = controller[0].strip()
                with open(CONTROLLER_PATH, 'w') as controller_file:
                    controller_file.writelines((controller[1:]))
                print("controller = ", command)
    return command

def writeToSystemController(command, file_path):
    # Clear the system controller
    with open(file_path,"w") as file:
        file.truncate(0)
    # Write the new command to the system controller
    with open(file_path, "w") as file:
        file.write(command)
    print("wrote: ", command, "to system controller")



def updateFiles(lines):
    # Write the lines to the previous songs file
    with open(PREVIOUS_SONG_PATH, "r") as file:
        lines_previous = file.readlines()
        
    if len(lines_previous) == 39:
        # remove the last 8 (the oldest previous song)
        lines_previous = lines_previous[:-8]
        # insert the new lines at the beginning:
        i = 0
        for item in lines:
            lines_previous.insert(i, item)
            i += 1
    else:
        i = 0
        for item in lines:
            lines_previous.insert(i, item)
            i += 1
    with open(PREVIOUS_SONG_PATH, "w") as file:
        # These already have new lines at the end
        print("writing to previous song file\n")
        for line in lines_previous:
            file.write(line)
        
f = open(PREVIOUS_SONG_PATH, "a")
f.close()
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

        print("sleep_duration: ", sleep_duration)

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
            # Testing the read lines: 
            for line in lines:
                # Strip is necessary to get rid of the new line character
                print(line.strip())


        # Sleep for the specified duration before repeating the process
        # sleep(sleep_duration)
        start_time = time.time()
        # Read contents of controller file into controller:
        time_at_pause = 0
        paused_offset = 0
        command = readController()
        while True:
            elapsed_time = time.time() - start_time
            

            # Read in the controller:
            # Read 
            # check if elapsed_time >= sleep_time, if yes break
            if elapsed_time >= sleep_duration + paused_offset:
                updateFiles(lines)
                writeToSystemController("next", SYSTEM_QUEUE_CONTROLLER)
                # updateFiles(lines)
                break
            elif (elapsed_time - paused_offset < sleep_duration and command == "pause"):
                print("paused\n")
                time_at_pause = elapsed_time
                time_paused = time.time()
                sp.pause_playback(device_id = DEVICE_ID)
                while command != "play":
                    command = readController()
                # Restart playback at the correct time:
                print("played")
                time_played = time.time()
                paused_offset += time_played - time_paused
                print("paused_offset: " , paused_offset)
                print("new sleep duration: ", sleep_duration + paused_offset)
                sp.start_playback(device_id = DEVICE_ID, uris=[modified_uri], position_ms=(time_at_pause*1000))
            elif command == "next":
                updateFiles(lines)
                writeToSystemController("next", SYSTEM_QUEUE_CONTROLLER)
                # updateFiles(lines)
                break# This will break out of the loop
            elif command == "previous":
                # updateFiles(lines)
                writeToSystemController("previous", SYSTEM_QUEUE_CONTROLLER)
                break
            command = readController()
            time.sleep(1)

        # Move the current song to the previous songs file
        print("song over, updating files\n")
        sleep(2)
        print("files should be updated, resuming playback with new song \n")
        
        

    except Exception as ex:
        print("An unexpected error occurred:", str(ex))
