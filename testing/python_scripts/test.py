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
CLIENT_ID="62d7db029474470d9910002d8e2c71fa"
CLIENT_SECRET="62d6fbba1a794b55a5be7e83216ddc5f"

# using to check if the data has anything in it once we did the get
while True:
    try:
        get_list = requests.get(MJ_URL) # perform the get on the website above
        response = requests.delete(MJ_URL)
        print(get_list)
        get_list.raise_for_status()
        
        # handle data being returned in json format
        data = get_list.json()
        temp_data = get_list.content
        print(data)
        print("temp data lenght: ", len(data))
    except requests.exceptions.HTTPError as e:
        print(e.response.text)
        
    while len(data) != 0:
        try:
            print("made it here\n")
        
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                        client_secret=CLIENT_SECRET,
                                                        redirect_uri="http://localhost:8080",
                                                        scope="user-read-playback-state,user-modify-playback-state",
                                                        cache_path='./tokens.txt'))
                                                    
            
            print("transfering device")
            sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

            # always using data[0], just removing after done with until list is empty
            # parse the current song in queue
            data_now = data.pop(0)
            print("data-now: ", data_now)
            print(len(data))
            
            uri = data_now["uri"]
            user_access_token = data_now["userAccessToken"]
            track_name = data_now["trackName"]
            track_artist = data_now["trackArtist"]
            track_cover = data_now["trackCover"]
            duration_ms = data_now["duration"]
            duration_sec = duration_ms/1000
            
            print("uri: ", uri)
            print("[uri]: ", [uri])
            print("user access: ", user_access_token)
            print("track name: ", track_name)
            print("track artist: ", track_artist)
            print("duration sec: ", duration_sec)
            
            
            
            print("track cover ", track_cover)
            
#             # deal with image processing:
#             # get image name
            image = re.findall("[^/]+(?=/$|$)", track_cover)[0]
            image += ".JPEG"
            print("image::::" , image)
            urllib.request.urlretrieve(track_cover, image)
            
            # load image
            im = cv2.imread(image)
           
            # improve image resolution
            hires = cv2.pyrUp(im)
            hires2 = cv2.pyrUp(hires)
            hires3 = cv2.pyrUp(hires2)

            cv2.namedWindow("Album", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("Album", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            # first step for image to start showing
            cv2.imshow("Album", hires3)
            # starting playing the song on the device in DEVIE_ID
            sp.start_playback(device_id=DEVICE_ID, uris=[uri])
            # allow the image to start showing
            cv2.waitKey(1)
            # sleep for the duration of the song
            sleep(duration_sec)
            # close window
            cv2.destroyAllWindows()
            # delete the image from the os
            os.remove(image)
            
    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
        except Exception as e:
            print(e)
            pass

        finally:
            print("Cleaning  up...")