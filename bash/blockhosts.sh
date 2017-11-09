#!/bin/bash

iptables -F INPUT

for X in $(cat /etc/hosts.deny|tr -d '\t'|grep deny|tr -d ' '|tr -d 'ALL:'|tr -d 'deny'|grep '[0-9]')
do
  echo "Blocking:" $X

  iptables -A INPUT -s $X -j DROP
done

iptables -A INPUT -j RH-Firewall-1-INPUT

iptables -L INPUT

