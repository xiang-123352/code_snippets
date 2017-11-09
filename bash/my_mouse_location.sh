#!/bin/bash
#Author: Kris Occhipinti (A.K.A. Metalx1000)
#Description: Gets your mouse location and echos "top left" when the cursor is moved to the top left of the screen.
#April. 2010
#http://www.BASHscripts.info
#GPL v3

while [ 1 ];
do
	m=`xdotool getmouselocation|sed 's/x:\(.*\) y:\(.*\) screen:.*/\1, \2/'`
	if [ "$m" = "0, 0" ];
	then
		echo "top left"
	fi
done