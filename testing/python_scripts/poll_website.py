import requests
import json
import time

website = "https://the-modern-jukebox-react-app.vercel.app/api/controls"

previous = "null"

while(1):
    time.sleep(3)
    r = requests.get(website)
    
    if(previous != r.text and r.text != "null"):
        previous = r.text
        # controls = json.loads(r.text)
        controls = r.json()
        if(controls["play"]):
            f = open("../remote.txt", "a")
            f.write("play\n")
            f.close()
        elif(controls["pause"]):
            f = open("../remote.txt", "a")
            f.write("pause\n")
            f.close()
        elif(controls["next"]):
            f = open("../remote.txt", "a")
            f.write("next\n")
            f.close()
        elif(controls["previous"]):
            f = open("../remote.txt", "a")
            f.write("previous\n")
            f.close()
        r = requests.delete(website)
