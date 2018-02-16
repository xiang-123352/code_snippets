#!/bin/bash

package=ssmtp

apt-cache depends "$package" | grep Depends: >> deb.list

sed -i -e 's/[<>|:]//g' deb.list

sed -i -e 's/Depends//g' deb.list

sed -i -e 's/ //g' deb.list

filename="deb.list"

while read -r line
do
    name="$line"
    apt-get download "$name"
done < "$filename"

apt-get download "$package"
