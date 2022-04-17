#!/bin/bash 
# Q&D code to close the door (it's identical to open the door, really is toggle the door state)
# Using old code
#/usr/bin/python /home/pi/Projects/piswitch/pypiswitch2.py &
# format
# written | read, input(n), value
# [w]|[r],[jav]|[dan],[0-2],[0]|[1]
echo 'r,mjo,4,1' >> /home/pi/Projects/piswitch/command.csv
#exit
