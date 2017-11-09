#!/bin/bash
# script to toggle wifi modes if connection is lost
##command i want to change in gconf
# you must edit this string to be exactly the one you have fouund in your gconf-editor
mycommand="gconftool-2 --type string --set /system/networking/connections/1/802-11-wireless/mode "
##possible modes
# mymode="adhoc"
# mymode="infrastructure"
#
#
sleep 10s
while [ 1 ]
do
	# ping to a text file
	myping=$(ping -c 1 google.com)
	echo $myping > $HOME/.myping
	if grep "1 received" $HOME/.myping
	then
		echo "up" > $HOME/.myupdown
	else
		echo "down" > $HOME/.myupdown
		if grep "adhoc" $HOME/.mymode
		then
			mymode="infrastructure"
			$mycommand$mymode
			echo "infrastructure" > $HOME/.mymode
		else
			mymode="adhoc"
			$mycommand$mymode
			echo "adhoc" > $HOME/.mymode
		fi
		mydate=$(date +%c)
		echo "$mydate $mycommand$mymode" >> $HOME/mylog
	fi
	sleep 40s
done
exit
