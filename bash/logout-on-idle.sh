#!/bin/bash
# Written by cz0 2010, adapted by dror 2013 
# Distributed under the terms of the GNU General Public License v2 

HALFHOUR=1800000
IDLETIME=`xprintidle`
QDBUS="/usr/bin/qdbus" 

if [ $IDLETIME -gt $HALFHOUR ]
then 
    logger timeout of $HALFHOUR expired. idle is $IDLETIME
    KDEPID=$(ps aux | grep 'startkde' | grep -v 'grep' | awk '{print $2}') 
    KDEUSER=$(ps u $KDEPID | grep 'startkde' | awk '{print $1}') 

# If the DBUS_SESSION_BUS_ADDRESS environment variable is not already set correctly 
# then set it by finding the environment file for the startkde process in proc and 
# parsing it to get get the correct setting. 

    if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then 
        ENVIRON_FILE=/proc/$(ps h --ppid $KDEPID -o pid | awk '{print $1}')/environ 
        CURRENT_DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS $ENVIRON_FILE | sed -e 's/DBUS_SESSION_BUS_ADDRESS=//') 
        export DBUS_SESSION_BUS_ADDRESS=$CURRENT_DBUS_SESSION_BUS_ADDRESS
    fi 
    $QDBUS org.kde.ksmserver /KSMServer logout 1 0 2 
else
    logger timeout is $HALFHOUR not expired $IDLETIME 
fi

