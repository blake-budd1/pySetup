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

def get_current_song():
    try:
        # Get the queue stored at MJ_URL
        get_list = requests.get(MJ_URL)
        get_list.raise_for_status()

        data = get_list.json()

        if data:
            current_item = data[0]
            duration_ms = current_item["duration"] / 1000

            # Save the album cover image
            image = re.findall("[^/]+(?=/$|$)", current_item["trackCover"])[0] + ".JPEG"
            urllib.request.urlretrieve(current_item["trackCover"], os.path.join("../album_covers", image))
            img = cv2.imread(os.path.join("../album_covers", image))

            # Write information to the file holding the data for the current song to be played
            with open(CURRENT_PATH, "w") as file:
                file.write(current_item["uri"] + "\n")
                file.write(os.path.join("/home/blake/Desktop/testing/album_covers", image) + "\n")
                file.write(current_item["userAccessToken"] + "\n")
                file.write(current_item["trackName"] + "\n")
                file.write(current_item["trackArtist"] + "\n")
                file.write(current_item["trackCover"] + "\n")
                file.write(str(current_item["duration"]) + "\n")
                file.write(str(duration_ms) + "\n")

            # Write the duration_sec to the file
            with open(CURRENT_SLEEP_PATH, "w") as file:
                file.write(str(duration_ms))

            return data

    except requests.exceptions.HTTPError as e:
        print("Error:", e.response.text)
    except Exception as ex:
        print("An unexpected error occurred:", str(ex))

    return None

def update_album_cover(data):
    try:
        if data:
            # Remove the current song to be played
            updated_data = data[1:]

            # Delete the existing queue from the front-end queue
            delete_response = requests.delete(MJ_URL)
            delete_response.raise_for_status()

            # Wait for the deletion to be confirmed
            while True:
                try:
                    # Attempt to get the queue again
                    get_list = requests.get(MJ_URL)
                    get_list.raise_for_status()
                    new_data = get_list.json()

                    # Check if the new queue is empty
                    if not new_data:
                        break  # Exit the loop if the new queue is empty

                    # Wait for a short time before checking again
                    sleep(1)
                except requests.exceptions.HTTPError as e:
                    print("Error getting updated queue:", e.response.text)

            # Put the updated data back to the front-end
            if updated_data:
                for item in updated_data:
                    post_data = {"message": item}
                    post_response = requests.post(POST_URL, json=post_data, headers={'Content-Type': 'application/json'})

                    if post_response.status_code == 200:
                        print("Put the updated queue back to the front-end.")
                    else:
                        print(f"Failed to put the updated queue. Status Code: {post_response.status_code}")
                        print(post_response.text)

            else:
                print(f"Failed to delete the current queue. Status Code: {delete_response.status_code}")
                print(delete_response.text)

            # Post the current playing song to the api/addPlaying
            curr_play_ur = {"message": data[0]}
            post_response = requests.post(CURR_URL, json=curr_play_ur, headers={'Content-Type': 'application/json'})
            post_response.raise_for_status()

            print("Updated the currently playing song on the front-end.\n")

    except requests.exceptions.HTTPError as e:
        print("Error:", e.response.text)
    except Exception as ex:
        print("An unexpected error occurred:", str(ex))

# Infinite loop for continuous execution
while True:
    data = get_current_song()
    update_album_cover(data)
    sleep_duration = float(open(CURRENT_SLEEP_PATH, "r").read().strip())
    print("sleeping for : " + str(sleep_duration - 5)+ "\n")
    sleep(sleep_duration - 5)