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
NEXT_PATH = "../temp_files/next_song.txt"
PREVIOUS_PATH = "../temp_files/previous_songs.txt"
CURRENT_SLEEP_PATH = "../temp_files/current_sleep.txt"
SYSTEM_QUEUE_CONTROLLER = "../system_queue_controller.txt"
SYSTEM_SFML_CONTROLLER = "../system_sfml_controller.txt"

def readController():
    sleep(5)
    command = ""
    with open(SYSTEM_QUEUE_CONTROLLER, "r") as controller_file:
            controller = controller_file.readlines()
            controller_file.close()
    if(controller):
        command = controller[0].strip()
        with open(SYSTEM_QUEUE_CONTROLLER, 'w') as controller_file:
            controller_file.writelines((controller[1:]))
            controller_file.close()
        print("controller in queue handling = ", command)
    return command

def writeToSystemController(command, file_path):
    # Clear the system controller
    with open(file_path,"w") as file:
        file.truncate(0)
        file.close()
    # Write the new command to the system controller
    with open(file_path, "w") as file:
        file.write(command)
        file.close()
    print("wrote: ", command, "to system controller")

# updated on 2/24 to post new song to front end when something other than time ran out
def updateCurrentFrontendSong():
    sleep(15)
    # Need to go through the current_song file, (this is called after that all is handled properly)
    # curr_play_ur = {"message": data[0]}
    #         post_response = requests.post(CURR_URL, json=curr_play_ur, headers={'Content-Type': 'application/json'})
    #         post_response.raise_for_status()
    with open(CURRENT_PATH, "r") as file:
        lines = [line.strip() for line in file]
    file.close()
    # if(lines):
    #     lines_to_post = lines[:-1] # remove the last line   
    
    data = {
        "uri":lines[1],
        "userAccessToken":lines[2],
        "duration":lines[6],
        "trackName":lines[3],
        "trackArtist":lines[4],
        "trackCover":lines[5]
    }
    
    json_data =json.dumps({"message":data})
    headers = {'Content-type':'application/json'}
    response = requests.post(CURR_URL, json=json_data, headers=headers)
    # response = requests.post(CURR_URL, json =data)
    response.raise_for_status()

def checkEmpty(file):
    with open(file, 'r') as file_obj:
        first_char = file_obj.read(1)
        file_obj.close()
        if not first_char:
            return True # True means file is empty
        else:
            return False
        

def get_current_song():
    try:
        # Get the queue stored at MJ_URL
        get_list = requests.get(MJ_URL)
        get_list.raise_for_status()

        data = get_list.json()
        # for item in data:
        #     print(item)
        if data:
            data_size  = len(data)
            
            print(data_size)
            current_item = data[0]
            if data_size > 1:
                next_item = data[1]
            else:
                print("no next song \n")
            duration_ms = current_item["duration"] / 1000

            # Save the album cover image
            image = re.findall("[^/]+(?=/$|$)", current_item["trackCover"])[0] + ".JPEG"
            urllib.request.urlretrieve(current_item["trackCover"], os.path.join("../album_covers", image))
            img = cv2.imread(os.path.join("../album_covers", image))

            if data_size > 1:
            # Save the next album cover image
                image_next = re.findall("[^/]+(?=/$|$)", next_item["trackCover"])[0] + ".JPEG"
                urllib.request.urlretrieve(next_item["trackCover"], os.path.join("../album_covers", image_next))
                img_next = cv2.imread(os.path.join("../album_covers", image_next))
            

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
                file.close()
            # Write information to the file holding the data for the next song to be played
            if data_size > 1:
                print("writing next song data with 2\n")
                with open(NEXT_PATH, "w") as file:
                    file.write(next_item["uri"] + "\n")
                    file.write(os.path.join("/home/blake/Desktop/testing/album_covers", image_next) + "\n")
                    file.write(next_item["userAccessToken"] + "\n")
                    file.write(next_item["trackName"] + "\n")
                    file.write(next_item["trackArtist"] + "\n")
                    file.write(next_item["trackCover"] + "\n")
                    file.write(str(next_item["duration"]) + "\n")
                    file.write(str(duration_ms) + "\n")
                    file.close()
            else:
                open(NEXT_PATH, 'w').close()                   
            # Write the duration_sec to the file
            with open(CURRENT_SLEEP_PATH, "w") as file:
                file.write(str(duration_ms))
            return data
        else:
            # Shoudl clear the current song and next song (if there are no songs on the queue)
            open(CURRENT_PATH, 'w').close()
            open(NEXT_PATH, 'w').close()

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
            
    except requests.exceptions.HTTPError as e:
        print("Error:", e.response.text)
    except Exception as ex:
        print("An unexpected error occurred:", str(ex))

# Infinite loop for continuous execution
#while True:
    # Initial data when system is powered on
data = get_current_song() # Handles reading and writing the current_song and the next_song (if available)
update_album_cover(data)
writeToSystemController("update", SYSTEM_SFML_CONTROLLER)
    # sleep_duration = float(open(CURRENT_SLEEP_PATH, "r").read().strip())
    # print("sleeping for : " + str(sleep_duration - 5)+ "\n")
    # sleep(sleep_duration - 5)
prev_handled = False
prev_count = 0
next_song = ""
while True:
    # Read the controller to see what the next thing to do it
    queue_command = readController()
    
    # If command is next, and no previous songs are left to handle:
    if queue_command == "next" and prev_handled == False:
        print("in next and prev_handled = false")
        data = get_current_song()
        update_album_cover(data)
        writeToSystemController("update", SYSTEM_SFML_CONTROLLER)
    elif queue_command == "next" and prev_handled == True:
        print("in next and prevHandled = True")
        # Set the current song to the next song
        with open(NEXT_PATH, "r") as next_file:
            next_song_local = next_file.readlines()
            next_file.close()
        # Set the current song to be the song in next_song (old current song)
        with open(CURRENT_PATH, "w") as curr_file:
            curr_file.writelines(next_song_local)
            curr_file.close()
        # Set the next song to be the next song before the previous
        with open(NEXT_PATH, "w") as next_file:
            next_file.writelines(next_song)
            next_file.close()
        prev_count -= 1
        # Note that we are done handling previous
        if prev_count == 0:
            prev_handled = False
        # Need to write the new current sleep time
        with open(CURRENT_SLEEP_PATH, "w") as sleep_file:
            sleep_file.write(next_song_local[7])
            sleep_file.close()
        
        # Tell SFML to update
        writeToSystemController("update", SYSTEM_SFML_CONTROLLER)

        # Update front end song
        # updateCurrentFrontendSong()

        # clear next song so the next previous can use is
        next_song = ""
        
    elif queue_command == "previous":
        # need to replace the current song with the previous song
        # Read in the previous song file (the most recent one) and remove it from the file
       
            
        with open(PREVIOUS_PATH, "r") as prev_file:
            prev_content = prev_file.readlines()
            prev_file.close()
        # Store the previous song
        print("previous songs: " , prev_content)
        prev_song = prev_content[:8]
        print("updated previous songs: ",prev_content[8:])

        # Rewrite previous song data without the new current song
        with open(PREVIOUS_PATH, "w") as prev_file:
            prev_file.writelines(prev_content[8:])
            prev_file.close()

        # Read in the current song and update it to be next song
        with open(CURRENT_PATH, "r") as curr_file:
            curr_song = curr_file.readlines()
            curr_file.close()

        # Clear the current song file
        with open(CURRENT_PATH, "w") as curr_file:
            curr_file.truncate(0)
            curr_file.close()
        # write the new current song to its file
        with open(CURRENT_PATH, "w") as curr_file:
            curr_file.writelines(prev_song)
            curr_file.close()
        with open(CURRENT_SLEEP_PATH, "w") as sleep_file:
            sleep_file.write(prev_song[7])
            sleep_file.close()
        # Store the next song to use the next loop
        with open(NEXT_PATH, "r") as next_file:
            next_song = next_file.readlines()
            print("next_song data: ", next_song)
            next_file.close()
        # Write the old current song as the next song:
        with open(NEXT_PATH, "w") as next_file:
            next_file.writelines(curr_song)
            next_file.close()
        # Set prev_handled = False (we will have to skip getting the queue one more time because we already have the next song)
        prev_handled = True
        prev_count += 1

        
        # Tell sfml to update
        writeToSystemController("update", SYSTEM_SFML_CONTROLLER)
        # Update the song on front end
        # updateCurrentFrontendSong()

        
        


