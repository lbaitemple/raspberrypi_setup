#!/bin/sh

acc=`ifconfig  | grep wlan0 | cut -d':' -f 6-7 | sed s/://`
pi_acc="Pi3-AC-$acc"
cmd=`/snap/bin/wifi-ap.config set wifi.ssid=$pi_acc`
echo "DONE"
