#!/bin/sh

modprobe msr

cpufreq-selector -f 1600000

sleep 1

wrmsr -p0 0xC0010064 0x80000100003810 # note: bogus values from memory!
wrmsr -p1 0xC0010064 0x80000100003810
wrmsr -p0 0xC0010065 0x800002c0003c12
wrmsr -p1 0xC0010066 0x800002c0003c12

cpufreq-selector -f 800000

sleep 1

wrmsr -p0 0xC0010066 0x800002c0007432
wrmsr -p1 0xC0010066 0x800002c0007432

cpufreq-selector -g ondemand

sleep 1
