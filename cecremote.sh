#!/bin/bash
datlastkey=$(date +%s%N)
strlastkey=""
strlastid=""
intkeychar=0
intmsbetweenkeys=2000 #two presses of a key sooner that this makes it delete previous key and write the next one (a->b->c->1->a->...)
intmousestartspeed=10 #mouse starts moving at this speed (pixels per key press)
intmouseacc=10 #added to the mouse speed for each key press (while holding down key, more key presses are sent from the remote)
intmousespeed=10

> remote.txt #delete content of txt file before running

while read oneline
do
    #echo $oneline
    keyline=$(echo $oneline | grep " key ")
    #echo $keyline #--- debugAllLines
    if [ -n "$keyline" ]; then
        datnow=$(date +%s%N)
        datdiff=$((($datnow - $datlastkey) / 1000000)) #bla bla key pressed: previous channel (123)
        strkey=$(grep -oP '(?<=sed: ).*?(?= \()' <<< "$keyline") #bla bla key pres-->sed: >>previous channel<< (<--123)
        strstat=$(grep -oP '(?<=key ).*?(?=:)' <<< "$keyline") #bla bla -->key >>pressed<<:<-- previous channel (123)
        strpressed=$(echo $strstat | grep "pressed")
        strreleased=$(echo $strstat | grep "released")
        if [ -n "$strpressed" ]; then
            strid=$(grep -oP '(\[ ).*?(\])' <<< "$keyline") # get the id from the debug line to ingnore dupe detection.
            #echo $keyline --- debug
            if [ "$strkey" = "$strlastkey" ] && [ "$datdiff" -lt "$intmsbetweenkeys" ]; then
                intkeychar=$((intkeychar + 1)) #same key pressed for a different char
            else
                intkeychar=0 #different key / too far apart
            fi
            datlastkey=$datnow
            strlastkey=$strkey
            if [ "$strid" != "$strlastid" ]; then
                case "$strkey" in
                    "up")
                        intpixels=$((-1 * intmousespeed))
                        xdotool mousemove_relative -- 0 $intpixels #move mouse up
                        intmousespeed=$((intmousespeed + intmouseacc)) #speed up
                        echo Key Pressed: up
                        ;;
                    "down")
                        intpixels=$(( 1 * intmousespeed))
                        xdotool mousemove_relative -- 0 $intpixels #move mouse down
                        intmousespeed=$((intmousespeed + intmouseacc)) #speed up
                        echo Key Pressed: down
                        ;;
                    "left")
                        intpixels=$((-1 * intmousespeed))
                        xdotool mousemove_relative -- $intpixels 0 #move mouse left
                        intmousespeed=$((intmousespeed + intmouseacc)) #speed up
                        printf "left\n" >> remote.txt
                        ;;
                    "right")
                        intpixels=$(( 1 * intmousespeed))
                        xdotool mousemove_relative -- $intpixels 0 #move mouse right
                        intmousespeed=$((intmousespeed + intmouseacc)) #speed up
                        printf "right\n" >> remote.txt
                        ;;
                    "select")
                        xdotool click 1 #left mouse button click
                        printf "select\n" >> remote.txt
                        ;;
                    "return")
                        xdotool key "Alt_L+Left" #WWW-Back
                        ;;
                    "exit")
                        echo Key Pressed: EXIT
                        ;;
                    "rewind")
                        printf "rewind\n" >> remote.txt
                        ;;
                    "pause")
                        printf "pause\n" >> remote.txt
                        ;;
                    "Fast forward")
                        printf "fast forward\n" >> remote.txt
                        ;;
                    "play")
                        printf "play\n" >> remote.txt
                        ;;
                    "stop")
                        ## with my remote I only got "STOP" as key released (auto-released), not as key pressed; see below
                        echo Key Pressed: STOP
                        ;;
                    *)
                        echo Unrecognized Key Pressed: $strkey ; CEC Line: $keyline
                        ;;

                esac
            #else
                #echo Ignoring key $strkey with duplicate id $strid
            fi
            # store the id of the keypress to check for duplicate press count.
            strlastid=$strid
        fi
        if [ -n "$strreleased" ]; then
            #echo $keyline --- debug
            case "$strkey" in
                "stop")
                    echo Key Released: STOP
                    ;;
                "up")
                    intmousespeed=$intmousestartspeed #reset mouse speed
                    ;;
                "down")
                    intmousespeed=$intmousestartspeed #reset mouse speed
                    ;;
                "left")
                    intmousespeed=$intmousestartspeed #reset mouse speed
                    ;;
                "right")
                    intmousespeed=$intmousestartspeed #reset mouse speed
                    ;;
            esac
        fi
    fi
done