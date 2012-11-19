#!/bin/sh
if ifconfig | grep "ppp0" ; then
	ifconfig eth0 mtu 1460
	ifconfig ppp0 mtu 1400
else
	ifconfig eth0 mtu 3000
fi
