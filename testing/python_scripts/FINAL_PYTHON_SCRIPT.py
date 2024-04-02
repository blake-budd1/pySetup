
######################################################## NOTES ########################################################
# Doing it this way and having only one python script to handle both the queue and spotify makes it so there are never
# any overlaps with reading and writing from the same file. 
# Additionally, with the SFML C++ program, there are no overlaps there either since the python program now gets
# a lock when it is writing to or reading a file. Basically, anytime a file is accessed, the script aquires a lock on it
# so that the OS doesn't give permissions to any other script or program that can interfer. 

# Furthermore, this way, there will always be populated data in the files before trying to read from the files when needed. 
# Also, it was updated so that if there is no new song on the queue by the time it gets polled, then it will wait until 
# there is a song so that the program doesn't behave randomly but rather waits until the data is there from the front-end. 
#########################################################################################################################


import requests
import json
import time
from time import sleep
import urllib.request
import cv2
import re
import os
import fcntl # For locks on files
import spotipy
from spotipy.oauth2 import SpotifyOAuth




# Storage for the current, next, and previous songs
CURRENT_SONG_PATH = "../temp_files/current_song.txt"
PREVIOUS_SONG_PATH = "../temp_files/previous_songs.txt"
NEXT_SONG_PATH = "../temp_files/next_song.txt"
# Attempting to add a next songs file to be the opposite of the previous songs file
NEXT_SONGS_HANDLER_PATH = "../temp_files/next_songs.txt"

# Storage for system controllers and handling
CURRENT_SLEEP_PATH = "../temp_files/current_sleep.txt"
CONTROLLER_PATH = "../temp_files/remote.txt"
HARDWARE_ID_PATH = "../temp_files/hardware_id.txt"
SYSTEM_QUEUE_CONTROLLER = "../temp_files/system_queue_controller.txt"
SYSTEM_SFML_CONTROLLER = "../temp_files/system_sfml_controller.txt"

# Spotify defines, if needed, change these to the new spotify developer account (only need these three things)
DEVICE_ID = "98bb0735e28656bac098d927d410c3138a4b5bca"
CLIENT_ID = "62d7db029474470d9910002d8e2c71fa"
CLIENT_SECRET = "62d6fbba1a794b55a5be7e83216ddc5f"


# Function used to aquire a lock on a file so that it ensures no file is being read and written to at the same time
def aquire_lock(file):
    start_time = time.time()
    while True:
        try:
            fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except (IOError, BlockingIOError):
            if time.time() - start_time >= 10:
                return False
            else:
                time.sleep(0.1)  # Wait for a short time before retrying


# Function used to release a lock once file operations are complete
def release_lock(file):
    fcntl.flock(file, fcntl.LOCK_UN)


# Used to read the hardware ID of the device (used to lock a session to one hardware)
def getHardwareID():
    # Need to read the file holding the hardware id
    with open(HARDWARE_ID_PATH, "r") as file:
        if aquire_lock(file):
            hardwareID = file.readline()
            release_lock(file)
    file.close()
    return hardwareID

hardwareID = getHardwareID()

# Linkts to interact with front-end, if needed, change these. Should be api/<page>
MJ_URL = "http://the-modern-jukebox-react-app.vercel.app/api/" + hardwareID + "/queue"
CONTROL_URL = "http://the-modern-jukebox-react-app.vercel.app/api/" + hardwareID + "/controls"
POST_URL = "https://the-modern-jukebox-react-app.vercel.app/api/" + hardwareID + "/addQueue"
CURR_URL = "https://the-modern-jukebox-react-app.vercel.app/api/" + hardwareID + "/addPlaying"

print("mj url: " + MJ_URL)

# This will read the file that handles all input commands (ie. pause, play, next, previous)
def readController():
    command = ""
    with open(CONTROLLER_PATH, "r") as controller_file:
            controller = controller_file.readlines()
            controller_file.close()
    if(controller):
        command = controller[0].strip()
        with open(CONTROLLER_PATH, 'w') as controller_file:
            controller_file.writelines((controller[1:]))
            controller_file.close()
        print("controller = ", command)
    return command

# This is used to update the controls on the front end to match anything that 
def postControlToWebsite(command):
    # curr_play_ur = {"message": data[0]}
    # post_response = requests.post(CURR_URL, json=curr_play_ur, headers={'Content-Type': 'application/json'})
    # post_response.raise_for_status()
    controls = {"play": False, "pause": False, "next": False, "previous": False }
    if(command == "pause"):
        controls = {"play": False, "pause": True, "next": False, "previous": False }
    elif (command == "play"):
        controls = {"play": True, "pause": False, "next": False, "previous": False }

    response = requests.post(CONTROL_URL, json = controls)

# This will try to see if user added something to the queue after we have already updated SFML and there was no next song
# If that is the case, this will update that file nad update the SFML controller to update with the new song
def AttemptToUpdateNextSong():
    # Try to get the queue:
    getList = requests.get(MJ_URL)
    getList.raise_for_status()
    queue = getList.json()
    queueSize = len(queue)
    
    nextSongAvailable = False
    
    if queueSize > 0 :
        nextSongAvailable = True
        nextSong = queue[0]
        image = re.findall("[^/]+(?=/$|$)", nextSong["trackCover"])[0] + ".JPEG"
        urllib.request.urlretrieve(nextSong["trackCover"], os.path.join("../album_covers", image))
        img = cv2.imread(os.path.join("../album_covers", image))
        
        duration_ms = nextSong["duration"] / 1000 
        # Write it to the nextSong file:
        with open(NEXT_SONG_PATH, "w") as file:
            if aquire_lock(file):
                file.write(nextSong["uri"] + "\n")
                file.write(os.path.join("/home/blake/Desktop/testing/album_covers", image) + "\n")
                file.write(nextSong["userAccessToken"] + "\n")
                file.write(nextSong["trackName"] + "\n")
                file.write(nextSong["trackArtist"] + "\n")
                file.write(nextSong["trackCover"] + "\n")
                file.write(str(nextSong["duration"]) + "\n")
                file.write(str(duration_ms) + "\n")
                release_lock(file)
            else:
                print("Could not access next_song.txt file to write the updated next song. \n")
                
    
        # Need to post the queue back to the front end: (This should stop it from checking again once we recognize there is something on the queue again)
        for item in queue:
            postData = {"message":item}
            postResponse = requests.post(POST_URL, json=postData, headers={'Content-Type':'application/json'})
            
            # Sanity check
            if postResponse.status_code != 200:
                print("Error posting updated queue back to front end: ", postResponse.status_code)
        return True
    else:
        return False
                

# Need to poll the front-end for the current song (and next song if it is available)
# If it is not available yet, keep polling so this stays here
def Start():
    # This is ran on startup, it will be the first function that is ran and the function
    # that is ran when there is no next or previous song that needs to be added from the buttons

    # Set this to 0 at start so it always trys to get the new queue
    # If the new queue is still 0, then it will sleep for a second and try again
    queueSize = 0
    # Place holder for when queue is read
    # queue = []
    while queueSize == 0:
        getList = requests.get(MJ_URL)
        getList.raise_for_status()
        queue = getList.json()
        queueSize = len(queue)
        print("qeueuSize: " + str(queueSize))
        if queueSize == 0:
            sleep(2)
            print("queue is empty\n")
        else:
            break

    print("We have a queue")             
    # Get the first song to handle
    songZero = queue[0]
    
    # Handle getting the album cover and saving it            
    image = re.findall("[^/]+(?=/$|$)", songZero["trackCover"])[0] + ".JPEG"
    urllib.request.urlretrieve(songZero["trackCover"], os.path.join("../album_covers", image))
    img = cv2.imread(os.path.join("../album_covers", image))
    
    # Calculate the duration in ms:
    duration_ms = songZero["duration"] / 1000
    
    
    # Write the current song data into the correct file:
    with open(CURRENT_SONG_PATH, "w") as file:
        if aquire_lock(file):
            file.write(songZero["uri"] + "\n")
            file.write(os.path.join("/home/blake/Desktop/testing/album_covers", image) + "\n")
            file.write(songZero["userAccessToken"] + "\n")
            file.write(songZero["trackName"] + "\n")
            file.write(songZero["trackArtist"] + "\n")
            file.write(songZero["trackCover"] + "\n")
            file.write(str(songZero["duration"]) + "\n")
            file.write(str(duration_ms) + "\n")
            release_lock(file)
    file.close()

    print("Wrote current song to file\n")

    # Write the current songs duration to the appropriate text file
    with open(CURRENT_SLEEP_PATH, "w") as file:
        file.write(str(songZero["duration"]/1000))
    file.close()

    # check if we have a next song we need to handle a second song
    if queueSize >= 2:
        nextSong = queue[1]
        # Write next song as well
        image_next = re.findall("[^/]+(?=/$|$)", nextSong["trackCover"])[0] + ".JPEG"
        urllib.request.urlretrieve(nextSong["trackCover"], os.path.join("../album_covers", image_next))
        img_next = cv2.imread(os.path.join("../album_covers", image_next))
        
        # Write the next song to the file
        
        nextSong_duration_ms = nextSong["duration"] / 1000
        with open(NEXT_SONG_PATH, "w") as file:
            file.write(nextSong["uri"] + "\n")
            file.write(os.path.join("/home/blake/Desktop/testing/album_covers", image_next) + "\n")
            file.write(nextSong["userAccessToken"] + "\n")
            file.write(nextSong["trackName"] + "\n")
            file.write(nextSong["trackArtist"] + "\n")
            file.write(nextSong["trackCover"] + "\n")
            file.write(str(nextSong["duration"]) + "\n")
            file.write(str(nextSong_duration_ms) + "\n")
        file.close()
        
        # Testing: Also write it to the next song file: (might not need to do this here, it is updated when needed later (could be the cause of the song showing up twice))
        # with open(NEXT_SONGS_HANDLER_PATH, "w") as file:
        #     file.write(nextSong["uri"] + "\n")
        #     file.write(os.path.join("/home/blake/Desktop/testing/album_covers", image_next) + "\n")
        #     file.write(nextSong["userAccessToken"] + "\n")
        #     file.write(nextSong["trackName"] + "\n")
        #     file.write(nextSong["trackArtist"] + "\n")
        #     file.write(nextSong["trackCover"] + "\n")
        #     file.write(str(nextSong["duration"]) + "\n")
        #     file.write(str(nextSong_duration_ms) + "\n")
        # file.close()
        
    else:
        # Need to clear the nextSong file:
        print("clearing next song file because there is no next song on front-end queue")
        file = open(NEXT_SONG_PATH, "w")
        file.truncate(0)
        file.close()    

        
    # Need to post the modified queue back to the front end after we have taken it and handled what needed to be done:
    updatedQueue = queue[1:]
    
    # Need to remove the old queue:
    removeQueueResponse = requests.delete(MJ_URL)
    removeQueueResponse.raise_for_status()
    
    # Need to make sure that the old queue is gone:
    while True:
        try:
            queueCheck = requests.get(MJ_URL)
            queueCheck.raise_for_status()
            tempQueue = queueCheck.json()
            if not tempQueue:
                break
            sleep(1)
        except requests.exceptions.HTTPError as e:
            print("Error removing queue from the front end:", e.response.text)
            
    # Once this is completed, the queue is deleted and good to place new queue onto
    if updatedQueue:
        for item in updatedQueue:
            postData = {"message":item}
            postResponse = requests.post(POST_URL, json=postData, headers={'Content-Type':'application/json'})
            
            # Sanity check
            if postResponse.status_code != 200:
                print("Error posting updated queue back to front end: ", postResponse.status_code)
    
    # Need to post the current playing song to the front-end 
    currSongFrontEnd = {"message": queue[0]}
    postResponse = requests.post(CURR_URL, json=currSongFrontEnd, headers={'Content-Type': 'application/json'})
    postResponse.raise_for_status()
    
    # Update the SFML file by writing to it's controller file
    updateSFML()

# This reads the queue controller and returns it (will be play, pause, next, or previous)
def handleController():
    command = ""
    # First read the controller:
    with open(CONTROLLER_PATH, "r") as file:
        content = file.readlines()
    file.close() # Close the file
    
    if (content):
        command = content[0].strip()
        with open(CONTROLLER_PATH, "w") as file:
            file.writelines(content[1:])
            file.close()   
    return command # return the command read from the queue_controller file
 
 
 # Update the the next song files

# Used to update the next songs file in the case of a previous
def UpdateNextSongFile():
    with open(CURRENT_SONG_PATH, "r") as file:
        if aquire_lock(file):
            currentLines = file.readlines()
            release_lock(file)
    file.close()
    
    with open(NEXT_SONGS_HANDLER_PATH, "r") as file:
        if aquire_lock(file):
            nextLines = file.readlines()
            release_lock(file)
    file.close()
    
    if len(nextLines) == 39:
        nextLines = nextLines[:-8]
        i = 0
        for item in currentLines:
            nextLines.insert(i, item)
            i += 1
    else:
        i = 0
        for item in currentLines:
            nextLines.insert(i, item)
            i += 1
    
    # Write back to the next_songs_file: 
    with open(NEXT_SONGS_HANDLER_PATH, "w") as file:
        if aquire_lock(file):
            for line in nextLines:
                file.write(line)
        release_lock(file)
    file.close()
 
# Used to check if there are previous songs to go to 
def previousSongsCheck():
    with open(PREVIOUS_SONG_PATH, "r") as file:
        data = file.readlines()
    file.close()
    
    if not data:
        return False
    else:
        return True  
 
# This will handle updating the files based off the control passed in (ie. next or previous)        
# def queueFileController(command, previousCount):
#     print("previousCount: " + str(previousCount))
#     if command == "next" and previousCount == 0:
#         Start() # Does the same process as starting it, goes and gets the queue and removes the first. Writes first and second to current and next song files
    
#     elif command == "next" and previousCount != 0:
      
#         # Need to read the lines in the next song handler file:
#         with open(NEXT_SONGS_HANDLER_PATH, "r") as file:
#             next_content = file.readlines()
#         file.close()
        
#         # This grabs the first next song that should be playing right now  
#         new_current_song = next_content[:8]
        
#         # Write the updated next songs back
#         with open(NEXT_SONGS_HANDLER_PATH, "w") as file:
#             file.writelines(next_content[8:])
#         file.close()
        
#         # Move the next song to the current song
#         with open(CURRENT_SONG_PATH, "w") as file:
#             file.writelines(new_current_song)
#         file.close()
        
#         # Write the current song sleep to the file
#         with open(CURRENT_SLEEP_PATH, "w") as file:
#             file.write(new_current_song[7])
#         file.close()
        
        
#         updateSFML()
            
#     elif command == "previous":
#         # Adding this to see if it will put all fo them in the next_song_handler_file:
#         UpdateNextSongsFile()
#         with open(PREVIOUS_SONG_PATH, "r") as prev_file:
#             prev_content = prev_file.readlines()
#             prev_file.close()
#         # Store the previous song
#         print("previous songs: " , prev_content)
#         prev_song = prev_content[:8]
#         print("updated previous songs: ",prev_content[7:])

#         # Rewrite previous song data without the new current song
#         with open(PREVIOUS_SONG_PATH, "w") as prev_file:
#             prev_file.writelines(prev_content[8:])
#             prev_file.close()

#         # Read in the current song and update it to be next song
#         with open(CURRENT_SONG_PATH, "r") as curr_file:
#             curr_song = curr_file.readlines()
#             curr_file.close()

#         # Clear the current song file
#         with open(CURRENT_SONG_PATH, "w") as curr_file:
#             curr_file.truncate(0)
#             curr_file.close()
#         # write the new current song to its file
#         with open(CURRENT_SONG_PATH, "w") as curr_file:
#             curr_file.writelines(prev_song)
#             curr_file.close()
#         with open(CURRENT_SLEEP_PATH, "w") as sleep_file:
#             sleep_file.write(prev_song[7]) # This should be 7 now with the duration_ms added back in
#             sleep_file.close()
#         # Store the next song to use the next loop
#         with open(NEXT_SONG_PATH, "r") as next_file:
#             next_song = next_file.readlines()
#             print("next_song data: ", next_song)
#             next_file.close()
#         # Write the old current song as the next song:
#         with open(NEXT_SONG_PATH, "w") as next_file:
#             next_file.writelines(curr_song)
#             next_file.close()
            
#         # Update the SFML in here since the "next" updates in the Start function already
#         updateSFML()
        
    
#     return previousCount


# This function should take the current song and place it in the next song (when previous occurs)
# Therefore, when doing a next after previous we should be able to get the next song by reading the first 8 of the next_song_handler_path
def UpdateNextSongsFile():
    
    with open(CURRENT_SONG_PATH, "r") as file:
        if aquire_lock(file):
            linesCurr = file.readlines()
            release_lock(file)
        file.close()
        
            
    with open(NEXT_SONGS_HANDLER_PATH, "r") as file:
        if aquire_lock(file):
            linesNext = file.readlines()
            release_lock(file)
        file.close()
    
    if len(linesNext) == 39:
        linesNext = linesNext[:-8]
        i = 0 
        for item in linesCurr:
            linesNext.insert(i, item)
            i += 1
    else:
        i = 0
        for item in linesCurr:
            linesNext.insert(i, item)
            i += 1
    
    with open(NEXT_SONGS_HANDLER_PATH, "w") as file:
        if aquire_lock(file):
            for line in linesNext:
                file.write(line)
            release_lock(file)
        file.close()
    


# Handle all the queue controlling
def queueFileController(command, previousCount):
    if command == "next" and previousCount == 0:
        print("normal next song\n")
        Start() # This gets the next song from the queue
       
       # Start handles writing next_song.txt to next_songs.txt
        
    elif command == "next" and previousCount != 0:
        # Dont think i need this because this moves current song to next_songs on a previous
        
        # UpdateNextSongFile()
        # next song 0 - 8 are the new current song
        with open(NEXT_SONGS_HANDLER_PATH, "r") as file:
            newCurrent = file.readlines()
        file.close()
        
        newCurrentSong = newCurrent[:8]
        
        with open(NEXT_SONGS_HANDLER_PATH, "w") as file:
            file.writelines(newCurrent[8:])
        file.close()
        
        with open(CURRENT_SONG_PATH, "w") as file:
            file.writelines(newCurrentSong)
        file.close()
        
         # Write the current song sleep to the file
        with open(CURRENT_SLEEP_PATH, "w") as file:
            file.write(newCurrentSong[7])
        file.close()
        
        previousCount -= 1
        
        with open(NEXT_SONGS_HANDLER_PATH, "r") as file:
            nextContent = file.readlines()
        file.close()
        
        with open(NEXT_SONG_PATH, "w") as file:
            file.writelines(nextContent[:8])
       
        
        updateSFML()
        
    elif command == "previous":
        
        # Check to see if there are any previous songs to go to:
        previousSongsAvailable = previousSongsCheck()
        if not previousSongsAvailable:
            print("no previous songs to go to")
            previousCount = 0
            return previousCount
        
        # If there are previous songs: 
        UpdateNextSongFile()
        
        with open(PREVIOUS_SONG_PATH, "r") as file:
            previousContent = file.readlines()
        file.close()
        
        previousToCurrentSong = previousContent[:8]
        
        with open(PREVIOUS_SONG_PATH, "w") as file:
            file.writelines(previousContent[8:])
        file.close()
        
        with open(CURRENT_SONG_PATH, "w") as file:
            file.truncate(0)
        file.close()
        
        with open(CURRENT_SONG_PATH, "w") as file:
            file.writelines(previousToCurrentSong)
        file.close()
        
        # write the new current sleep
        with open(CURRENT_SLEEP_PATH, "w") as file:
            file.write(previousToCurrentSong[7])
        file.close()
        
        # Need to write the first next song to the next song file for the SFML
        with open(NEXT_SONGS_HANDLER_PATH, "r") as file:
            nextContent = file.readlines()
        file.close()
        
        with open(NEXT_SONG_PATH, "w") as file:
            file.writelines(nextContent[:8])
       
    
        updateSFML()
        
    return previousCount



# This will update the files after spotify has finished playing a song (call this once playback is finished)
def updateSpotifyFiles():
    
    # Read in the current song file that will be moved to the previous song file
    with open(CURRENT_SONG_PATH, "r") as file:
        if aquire_lock(file):
            lines = file.readlines()
            # TODO: Might need to strip here - Dont think i do yet because we are writing and reading from the text file and new lines are gonna have to be there
            release_lock(file)       
    file.close()
    
    # Write the lines to the previous songs file
    with open(PREVIOUS_SONG_PATH, "r") as file:
        if aquire_lock(file):
            lines_previous = file.readlines()
            release_lock(file)
    file.close()
    
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
        if aquire_lock(file):
            for line in lines_previous:
                file.write(line)
            release_lock(file)
    file.close()    
    


    
    
# This reads in the file storing the sleep time
def readCurrentSleep():
    with open(CURRENT_SLEEP_PATH, "r") as file:
        if aquire_lock(file):
            current_sleep_time = float(file.readline().strip())
            release_lock(file)
    file.close()
    print("Read current sleep and got: "  + str(current_sleep_time))
    return current_sleep_time


    

# This returns the 'sp', which is used for spotify controls
def spotifySetup():
    # This will handle the spotify_play.py script in this script
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://localhost:8080",
    scope="user-read-playback-state,user-modify-playback-state",
    cache_path='./tokens.txt'
    ))
    
    sp.transfer_playback(device_id=DEVICE_ID, force_play=True)
    
    # Return sp so it can be referenced later in main
    return sp
    

# This returns the modified song URI that spotify uses, it takes the one in the file and strips it of the new line
def modifyURI():
    with open(CURRENT_SONG_PATH, "r") as file:
        if aquire_lock(file):
            modifiedURI = file.readline()
            release_lock(file)
            modifiedURI = modifiedURI.rstrip('\n')
    file.close()
    return modifiedURI


def updateSFML():

    # # Write the new command to the system controller
    # with open(SYSTEM_SFML_CONTROLLER, "w") as file:
        
    #     file.write("update")

    # file.close()
    # print("Wrote update to sfml in the python script\n")
    
    # 3/21 update: ( HAS NOT BEEN TESTED YET BUT THIS SHOULD MAKE SURE THAT THE SFML PROGRAM IS NOT READING IT WHILE IT WRITES)
    with open(SYSTEM_SFML_CONTROLLER, "w") as file:
        if aquire_lock(file):
            file.write("update")
            release_lock(file)
        else:
            lock = False
            while lock == False:
                if (lock == False):
                    lock = aquire_lock(file)
    print("Updated SFML and have finished writing it to the file as of now in python \n")
                


# This is the main program, it will handle everything
def main():
    print("Starting the main.py script\n")
    
    # This instantiates 'sp' which is the spotipy object used to control spotify api
    sp = spotifySetup()
    
    # This gets the current song and the next song (if queue empty it waits in this)
    Start()
    
    # This keeps track of how many previous songs we need to handle (should remain zero unless a previous has been pressed and not handled yet)
    previousCount = 0

    # Need to loop here, this will run the entire time the device has power and be the main functionality of hardware
    while True:
        # Read the sleep for the current song
        current_sleep_time = readCurrentSleep()

        # This goes into the current_song.txt file and strips the uri of it's new line so we can pass it into playback
        currentURI = modifyURI()
        print("modified uri: " + currentURI)
        # Start the spotify playback of the 'currentURI'
        sp.start_playback(device_id=DEVICE_ID, uris=[currentURI])

        print("playback has started\n")
    
        nextSongBool = True # assume next song is populated
    
        # Read the next song file, check if it is empty:
        with open(NEXT_SONG_PATH, "r") as file:
            data = file.readlines()
            file.close()
            print("next song data: ", str(data))
        if not data:
            # If next song is empty, set bool to false
            print("Set nextSongBool to false\n")
            nextSongBool = False
        
        # Set a counter to tell when we should try to get next song: 
        nextSongGet = 0
            
    
        # This is the starting time once the song starts playing
        startTime = time.time()
        
        # These variables are for handling restarting playback once paused
        timeAtPause = 0
        pausedOffset = 0
        
        command = handleController()
        if (command != ""):
            print("command : " + command)        
        # This is to loop and read the remote.txt file, this handles all input from user for controlling device
        while True:
            # This is polling the controller while the song is playing to look for user input
            command = handleController()
            elapsedTime = time.time() - startTime
            
            # Need to check if the elapsed_time is greater than the song time plus any addition from pausing
            if elapsedTime >= current_sleep_time + pausedOffset or command == "next":
                # This moves the song that is in the current_song.txt file into the previous_songs.txt file
                updateSpotifyFiles()
                break
            
            elif elapsedTime - pausedOffset < current_sleep_time and command == "pause":
                # Pause the playback on the device
                sp.pause_playback(device_id=DEVICE_ID)
                
                # Keep track of the moment in the song the user paused
                timeAtPause = elapsedTime
                
                # Keep track of how long the song stays paused
                currTime = time.time()
                # Debugging
                print("paused\n")
                
                # Wait until the user plays the song again
                while command != "play":
                    command = handleController()
                    
                sp.start_playback(device_id=DEVICE_ID, uris = [currentURI], position_ms=(timeAtPause*1000))
                
                # Handle all the timing issues to add to the elapsed time
                timePlayed = time.time()
                pausedOffset += timePlayed - currTime
        
            elif command == "previous":
                # Increment the amount of previous and change the boolean to show that a previous is being handled next
                previousCount += 1
                # updateSpotifyFiles()
                break
                
                # This should be updated to include a sanity check to see if there are previous songs to go to
                # If there is then increment previousCount and break
                # otherwise, just ignore it and continue with the loop (ie. the control is already removed and we do not need to break or do anything)
        
        
            # This just checks if we need to update the nextSong  - Currently being tested. 
            if nextSongGet == 300 and nextSongBool == False:
                nextSongBool == AttemptToUpdateNextSong()
                if nextSongBool == True:
                    print("Updating with a new next song\n")
                    nextSongGet = 0
                    updateSFML()
            else:
                nextSongGet = nextSongGet + 1 # otherwise, increment next songGet counter  (this gives us control over the amount of gets that are occuring on front-end)
            
        
        print("Song over, moving to next song\n")
        
        # Need to update the files:
        previousCount = queueFileController(command, previousCount)        
        

# This is the main code to run, need to call main()               
main()    
                
                
                
                
# TODO: Something weird is happening where sfml isn't clearing the sfml controller file and it get's stuck in a loop updating
# TODO: In SFML make sure it is clearing the file properly and no where in here is getting stuck writing to the file

# TODO: If there is no next song while the song is playing, see if we can get the next song every 10 seconds ? or so seconds (will still post whole queue back to front-end so all the next works properly)
