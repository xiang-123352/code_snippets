#!/bin/bash

# Author	: Imri Paloja
# Version	: 2.0

mkdir /tmp/add-ppa/

wget --quiet "http://ppa.launchpad.net/$(echo $1 | sed -e 's/ppa://g')/ubuntu/dists" -O /tmp/add-ppa/support.html

grep "$(lsb_release -sc)" "/tmp/add-ppa/support.html" >> /tmp/add-ppa/found.txt

cat /tmp/add-ppa/found.txt | sed 's|</b>|-|g' | sed 's|<[^>]*>||g' >> /tmp/add-ppa/stripped_file.txt

if [[ -s /tmp/add-ppa/stripped_file.txt ]] ; then

echo "$(lsb_release -sc) is supported"

echo "Adding it to your sources list"
sudo add-apt-repository $1

echo "Refreshing your sources list"
sudo apt-get update 

# Searching for the needed files, and installing them

wget --quiet "http://ppa.launchpad.net/$(echo $1 | sed -e 's/ppa://g')/ubuntu/dists/$(lsb_release -sc)/main/binary-amd64/Packages" -O /tmp/add-ppa/packages.html

grep "Package:" "/tmp/add-ppa/packages.html" >> /tmp/add-ppa/packages.txt

cat /tmp/add-ppa/packages.txt | sed ':a;N;$!ba;s/\n/ /g' >> /tmp/add-ppa/packages_stripped_file.txt

cat /tmp/add-ppa/packages_stripped_file.txt | sed 's|Package:||g' >> /tmp/add-ppa/packages_stripped_file2.txt

sudo apt-get install $(grep -vE "^\s*#" /tmp/add-ppa/packages_stripped_file2.txt  | tr "\n" " ")

else

echo "$(lsb_release -sc) is not supported"

fi;

#Cleanup

rm -r /tmp/add-ppa/