#!/bin/bash

PLAYLIST=~/DVB-C_playlist.m3u
SOURCEFILE=~/channels.conf

echo "#EXTM3U" > $PLAYLIST

while read LINE
do
  name=$(echo $LINE | awk -v FS=":" '{print $1}')
  programm=$(echo $LINE | awk -v FS=":" '{print $10}')
  frequency=$(echo $LINE | awk -v FS=":" '{print $2 "000"}')
  srate=$(echo $LINE | awk -v FS=":" '{print $5 "000"}')
  modulation=$(echo $(echo $LINE | awk -v FS=":" '{print $3}') | awk -v FS="M" '{print $2}')

  echo "#EXTINF:0,$name" >> $PLAYLIST
  echo "#EXTVLCOPT:dvb-adapter=0" >> $PLAYLIST
  echo "#EXTVLCOPT:dvb-frequency=$frequency" >> $PLAYLIST
  echo "#EXTVLCOPT:dvb-srate=$srate" >> $PLAYLIST
  echo "#EXTVLCOPT:dvb-modulation=$modulation" >> $PLAYLIST
  echo "#EXTVLCOPT:program=$programm" >> $PLAYLIST
  echo "dvb://" >> $PLAYLIST
done<$SOURCEFILE
