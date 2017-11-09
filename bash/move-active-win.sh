#!/bin/bash

# Can get from wmctrl -d
S_W=1680
S_H=1050

# Get info of current active window

win_id=$(xprop -root | sed '/_NET_ACTIVE_WINDOW(WINDOW)/ {s/.*\(0x[a-z0-9]\+\)/\1/;q} ; d')

read win_x win_y <<< "$(xwininfo -id $win_id | sed '/Absolute/ {s/[ :a-z-]//gi;p} ; d' | tr '\n' ' ')"
read win_w win_h <<< "$(xwininfo -id $win_id | sed '/\(Width\|Height\)/ {s/[ :a-z-]//gi;p} ; d' | tr '\n' ' ')"
read b_left _ b_top _ <<< "$(xprop -id $win_id | sed '/FRAME.*CARDINAL/ {s/[_=(),a-z]//gi;q} ; d')"

# Remove window decoration
((win_x-=b_left))
((win_y-=b_top))

case "$1" in
  u|up)
    ((win_y-=S_H))
    ((win_y < 0)) && exit 1
    ;;
  d|down)
    ((win_y+=S_H))
    ((win_y >= 2*S_H)) && exit 1
    ;;
  l|left)
    ((win_x-=S_W))
    ((win_x < 0)) && exit 1
    ;;
  r|right)
    ((win_x+=S_W))
    ((win_x >= 2*S_W)) && exit 1
    ;;
  *)
    exit 1
    ;;
esac

# Somehow, the window gets taller in Fluxbox after moves, has to supply height instead of -1
wmctrl -i -r $win_id -e "0,$win_x,$win_y,-1,$win_h"

