from gpiozero import Button
from time import sleep

## map buttons

play_button = Button(4)
pause_button = Button(14)
next_button = Button(15)
previous_button = Button(18)

#adding sleep when button pressed to account for button debouncing

while(1):
    if play_button.is_pressed:
        f = open("remote.txt", "a")
        f.write("play\n")
        f.close()
        sleep(.2)
    if pause_button.is_pressed:
        f = open("remote.txt", "a")
        f.write("pause\n")
        f.close()
        sleep(.2)
    if next_button.is_pressed:
        f = open("remote.txt", "a")
        f.write("next\n")
        f.close()
        sleep(.2)
    if previous_button.is_pressed:
        f = open("remote.txt", "a")
        f.write("previous\n")
        f.close()
        sleep(.2)