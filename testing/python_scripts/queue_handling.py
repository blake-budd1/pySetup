import requests
import json
from time import sleep
import urllib.request
import cv2
import re
import os


MJ_URL = "https://the-modern-jukebox-react-app.vercel.app/api/queue"
POST_URL = "https://the-modern-jukebox-react-app.vercel.app/api/addQueue"
CURR_URL = "https://the-modern-jukebox-react-app.vercel.app/api/addPlaying"
CURRENT_PATH = "../temp_files/current_song.txt"
CURRENT_SLEEP_PATH = "../temp_files/current_sleep.txt"

try:
    # get the queue stored at MJ_URL
    get_list = requests.get(MJ_URL)
    # Debug print the queue
    get_list.raise_for_status()

    # retrieve the data from the response
    data = get_list.json()
    
    # Get the current song (the one poped off the queue)
    current = data.copy()
    if data:
        current_item = current.pop(0)
        uri = current_item["uri"]
        user_access_token = current_item["userAccessToken"]
        track_name = current_item["trackName"]
        track_artist = current_item["trackArtist"]
        track_cover = current_item["trackCover"]
        duration_ms = current_item["duration"]
        duration_sec = duration_ms/1000

        # Save the album cover image:
        image = re.findall("[^/]+(?=/$|$)", track_cover)[0]
        image += ".JPEG"
        urllib.request.urlretrieve(track_cover, image)
        img = cv2.imread(image)
    

        image_file_path = "../album_covers"
        os.chdir(image_file_path)  # save the image to image_file_path
        # Save the image
        cv2.imwrite('../album_covers/' + image, img)        
        os.chdir("../python_scripts") # set working directory back to where this script is located
    
        # Write that information to the file holding the data for the current song to be played
        with open(CURRENT_PATH, "w"):
            pass
            print("cleared contents of current_song.txt\n")
        with open(CURRENT_PATH, "w") as file:
            file.write(uri + "\n")
            file.write("/home/blake/Desktop/testing/album_covers/" + image + "\n")
            file.write(user_access_token + "\n")
            file.write(track_name + "\n")
            file.write(track_artist + "\n")
            file.write(track_cover + "\n")
            file.write(str(duration_ms) + "\n")
            file.write(str(duration_sec) + "\n")        
        with open(CURRENT_SLEEP_PATH, "w") as file:
            pass
            print("Cleared the current duration of song\n")
        with open(CURRENT_SLEEP_PATH, "w") as file:
            file.write(str(duration_sec))

    if data:
        # print the current data
        print("Current Queue:", data)

        # remove the current song to be played (create a copy to avoid modifying the original)
        updated_data = data[1:]

        # This is the new queue without the currently playing song
        print("Updated Data:", updated_data)
        print("\n")

        # delete the existing queue from the front-end queue
        delete_response = requests.delete(MJ_URL)
        if delete_response.status_code == 200: # sanity check for the HTTP request: DELETE
            print("Deleted the current queue.")
            # wait for the deletion to be confirmed
            while True:
                try:
                    # attempt to get the queue again
                    get_list = requests.get(MJ_URL)
                    get_list.raise_for_status()
                    new_data = get_list.json()

                    # check if the new queue is empty
                    if not new_data:
                        break  # exit the loop if the new queue is empty

                    # wait for a short time before checking again
                    sleep(1)
                except requests.exceptions.HTTPError as e:
                    print("Error getting updated queue:", e.response.text)

            # put the updated data back to the front-end
            # put the updated data back to the front-end
        if updated_data:
            try:
                print(f"URL: {POST_URL}")
                # Iterate through updated_data and post to the queue
                for item in updated_data:
                    post_data = {"message": item}

                    post_response = requests.post(POST_URL, json=post_data, headers={'Content-Type': 'application/json'})

                    if post_response.status_code == 200:
                        print("Put the updated queue back to the front-end.")
                    else:
                        print(f"Failed to put the updated queue. Status Code: {post_response.status_code}")
                        print(post_response.text)
            except requests.exceptions.HTTPError as e:
                print("Error putting data:", e.response.text)
        

        else:
            print(f"Failed to delete the current queue. Status Code: {delete_response.status_code}")
            print(delete_response.text)

        # Post the current playing song to the api/addPlaying
        curr_play_ur = {"message":current_item}
        post_response = requests.post(CURR_URL, json=curr_play_ur, headers={'Content-Type': 'application/json'})
        print("Updated the currently playing song on the front-end.\n")
    else:
        print("Queue is empty. \n")

except requests.exceptions.HTTPError as e:
    print("Error:", e.response.text)
    
    
    
    
    
    
    