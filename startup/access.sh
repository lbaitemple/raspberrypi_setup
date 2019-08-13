#!/bin/bash

#acc=`ifconfig  | grep wlan0 | cut -d':' -f 6-7 | sed s/://`
acc=`ip addr show $(awk 'NR==3{print $1}' /proc/net/wireless | tr -d :) | awk '/ether/{print $2}' | cut -d':' -f 5-7 | sed s/:// `
pi_acc=`echo Pi3-AC-${acc^^}`
cmd=`sudo /snap/bin/wifi-ap.config set wifi.ssid=${pi_acc}`
echo "DONE"
