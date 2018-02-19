#!/bin/sh

export DISPLAY=:0 

service amdmsrt start
service coolfan start

powertop --auto-tune

aticonfig --pplib-cmd="notify psrc dc"

gsettings set org.mate.Marco.general reduced-resources true
gsettings set org.mate.interface gtk-enable-animations false

