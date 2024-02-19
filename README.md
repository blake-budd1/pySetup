chmod modern_jukebox3.sh
/modern_jukebox3.sh

This will run the scripts and allow for all three scripts to work at the same time to display the song using sfml, get the current song from queue, and start the playback on the raspberry pi device. 

TODO: in queue: if the queue is empty then empty the current_song.txt


have both pi scripts poll file that says either next or previous, when one or the other, do that. 
If neither of those, scripts don't run. i.e.) still playing or paused. 
