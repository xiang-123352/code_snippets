#!/bin/sh

PLUGIN="/usr/lib/flashplugin-installer/libflashplayer.so"
PID=$(lsof -t $PLUGIN)
FD=$(lsof -p $PID|grep Flash|awk '{print $4}'|sed 's/u$//')

cp /proc/$PID/fd/$FD "$1"

