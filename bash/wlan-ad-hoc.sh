#!/bin/bash
#
# Wireless Ad-hoc script
#
# http://agentoss.wordpress.com / fredo696@gmail.com
#
# This script will setup your wireless adapter in Ad-Hoc mode
# and start a DHCP server so that other peers (eg. an Android device)
# can receive an IP address and connect to your computer.
#
# After that, you can start a minimal webserver (darkhttpd for example)
# so that you can quickly share some files with minimal effort!
#
# This script must be run as root.
# Tested on Arch Linux.
# Some adaptations may be needed for other Linux systems.
#
# Requirements: iw, ifconfig commands, and dnsmasq.
#
# WARNING : WEP encryption is weak security :)

# User variables
mywlan="wlan0"
myessid="fredo"
mychan="4"
mywepkey="dead-beef-00"
myip="192.168.7.100"
mydhcprange="192.168.7.101,192.168.7.110"

# Main program
echo -n "Stopping wireless connections (if any)... "
# adapt to your system; I use wicd
systemctl stop wicd && echo "OK"
# for networkmanager
#systemctl stop NetworkManager

echo -n "Starting wireless Ad-hoc mode... "
ifconfig $mywlan down || exit 1
iwconfig $mywlan mode ad-hoc || exit 1
iwconfig $mywlan essid $myessid
iwconfig $mywlan channel $mychan
[ "$mywepkey" ] && iwconfig $mywlan key $mywepkey

ifconfig $mywlan $myip
ifconfig $mywlan up && echo "OK"
echo -n "Starting DHCP server ... "
dnsmasq --dhcp-range="$mydhcprange" && echo "OK"

echo "--------------------------------------"
echo "ESSID : $myessid"
[ "$mywepkey" ] && echo "WEP KEY : $mywepkey"
echo "This computer's IP : $myip"
echo "--------------------------------------"

# debug
#iwconfig $mywlan

while true; do
echo -n "Enter 'q' to quit. "
read value
if [ "$value" == "q" ]; then
break
fi
done

echo -n "Killing DHCP server... "
killall dnsmasq && echo "OK"
echo -n "Killing wireless... "
# restoring the wlan interface to "default" mode
ifconfig $mywlan down
iwconfig $mywlan mode managed
iwconfig $mywlan essid off
iwconfig $mywlan key off
echo "OK"
echo "Wireless Ad-hoc mode terminated."
# now you can restart your network manager

exit 0

