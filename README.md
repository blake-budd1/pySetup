The Modern Jukebox

 - Our GUI is innately user-friendly with the current song played being centered on the screen and the largest album cover displayed. Our previous and next songs remain to the left and right of the current song displayed, matching the ordering that would occur when pressing next and previous based on a remote control’s button placement. In addition, we take advantage of the user's innate familiarity with tv remote’s when using the remote controller to navigate our GUI. The current perception for our physical buttons resemble the ordering of how you would press any of the buttons (play, pause, next, previous), with play and pause buttons being green and red to relate to the typical associations of those colors with start and stop.  




- There are three options for navigation. The first option is using a remote made for the TV. This option allows the user to pair any remote to the tv and use the following four buttons to navigate the UI and the song playing on the device: next, previous, pause, play. Additionally, the user may decide to use the website controls, which are present on the front end when the user presses on the currently playing album cover. These controls include the same controls as the remote: previous, next, pause, play. Finally, the user may opt to use the buttons that are connected to the Raspberry Pi GPIO ports. These buttons are the same, with blue being next, yellow being previous, red being pause, and green being play. These buttons function the same as the remote and website buttons, and all of the buttons are written to the same place, where one script reads those controls from that file. Therefore, all of the navigation ends up acting the same way so there is no difference between using one or the other, it all depends on what the user feels most comfortable with using. 

- Directory structure:
- Script that runs all of the necessary components:
- modern_jukebox_v3.sh
- python_scripts
-   queue_handling_v3.sh
-     Handles getting the current song and next song. Behavior is dependent on the controls (either next and previous)
-   spotify_play_v3.sh
-     Handles playback on raspodify, also, handles controls and writting to the correct controller file.
- SFML_programs
-   welcome screen:
-     Welcomes the user to The Modern Jukebox and prompts the user to change the playback device to the 'Raspodify'
-   main_v3.cpp
-     UI that handles current, next, and previous songs.
