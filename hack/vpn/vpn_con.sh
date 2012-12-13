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
	ppp=`ip route | grep "ppp[01]" | cut -f 1 -d " "`
	route del default
	route add default gw $ppp
	touch /tmp/vpn.up

# First make sure the ppp connection actually exists, and then wait till it
# is actually up (detected by checking when its default MTU gets set)

	RESULT=""
	while [ "${RESULT}" == ""];
	do
	  sleep 1
	  PPP="`ifconfig -a | grep -A 6`"
	  if [ "${PPP}" == "" ]; then
	    RESULT="fail"
	  else
	    RESULT="`ifconfig -a | grep -A 6 ppp0 | grep MTU:1496`"
	  fi
	done

# If the connection is up, and it didn't fail then we change the MTU
	if [ "${RESULT}" != "fail" ]; then
	#  ifconfig eth0 mtu 1460
	  ifconfig ppp0 mtu 1400
	fi

else

	killall pptp
	route add default gw $dgateway	
	rm /tmp/vpn.up

# Wait and make sure the PPP connection is down again first
	PPP="`ifconfig -a | grep -A 6`"
	while [ "${PPP}" != "" ];
	do
	  sleep 1
	  PPP="`ifconfig -a | grep -A 6`"
	done

	ifconfig eth0 mtu 1500

fi
rm /tmp/vpn.tmp
