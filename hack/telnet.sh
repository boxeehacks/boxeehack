#!/bin/sh

ID=$(ps aux | grep telnet | grep busybox | grep -v grep | awk '{print $2}')
telnet=$(cat /data/etc/telnet);

if [ $ID ]; then
	kill -9 $ID
elif [ ! $ID ] && [ $telnet == "1" ]; then
	/data/hack/bin/busybox telnetd -p 2323 -l /data/hack/shell.sh &
fi
