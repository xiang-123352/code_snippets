#!/bin/sh

start_cmd="echo start_cmd"
stop_cmd="stop_cmd"

dbus-monitor --session "type='signal',interface='org.gnome.ScreenSaver',member='ActiveChanged'"|while read line
do 
  if [ x"$(echo "$line" | grep 'boolean true')" != x ]
  then 
    # runs once when screensaver comes on...
    $start_cmd
  fi
  
  if [ x"$(echo "$line" | grep 'boolean false')" != x ] ; then 
    # runs once when screensaver goes off...
    $stop_cmd
  fi
done

