#!/bin/sh
#####################################################
# VPN Script for the Boxee Box v 1.0                #
# Author: n3!                                       #
#####################################################

# Extracts VPN details from the guisettings.xml file and stores them into the following variables below.

host=`sed -n '/vpn*/,/<\/vpn>/p' /data/.boxee/UserData/guisettings.xml > /tmp/vpn.tmp | grep server /tmp/vpn.tmp | awk -F'>' '{print $2}' | awk -F'<' '{print $1}'`
username=`sed -n '/vpn*/,/<\/vpn>/p' /data/.boxee/UserData/guisettings.xml > /tmp/vpn.tmp | grep account /tmp/vpn.tmp | awk -F'>' '{print $2}' | awk -F'<' '{print $1}'`
password=`sed -n '/vpn*/,/<\/vpn>/p' /data/.boxee/UserData/guisettings.xml > /tmp/vpn.tmp | grep password /tmp/vpn.tmp | awk -F'>' '{print $2}' | awk -F'<' '{print $1}'`
dgateway=`grep gateway /data/.boxee/UserData/guisettings.xml | awk -F'>' '{print $2}' | awk -F'<' '{print $1}'`

# Checks to see if there is a current VPN connection and if it finds one it disconnects you.

status=`ifconfig |grep ppp | busybox awk '{ print $1 }'`

if [ "$status" = "" ]; then
        pppd pty "pptp $host --nolaunchpppd" file /etc/ppp/options.pptp user $username password $password
        sleep 3
        ppp=`ifconfig |grep -A 6 ppp[01] |grep addr: | cut -f 2 -d ":" | cut -f 1 -d " "`
        if [ "$ppp" = "" ]; then
                echo "Failed!"
        else
                dgateway=`ip route  | grep default | grep "eth[01]" | cut -f 3 -d " " > /data/hack/vpn/.gw`
                route del default
                route add default gw $ppp
                ifconfig ppp0 mtu 1400
                touch /tmp/vpn.up
        fi

else
        dgw=`cat /data/hack/vpn/.gw`
        killall pptp
        route add default gw $dgw
        rm /tmp/vpn.up

fi
rm /tmp/vpn.tmp
