#!/bin/sh

if [ ! -f "/data/etc/utorrent" ]; then
  echo "1" > /data/etc/utorrent
  chmod 777 /data/etc/utorrent
fi

if [ ! -d "/media/BOXEE/downloads" ]; then
  	mkdir /media/BOXEE/downloads
	chmod 777 /media/BOXEE/downloads
fi

ID=$(ps aux | grep utorrent | grep ld-linux.so.2 | grep -v grep | awk '{print $2}')
utorrent=$(cat /data/etc/utorrent);

if [ $ID ]; then
	kill -9 $ID
elif [ ! $ID ] && [ $utorrent == "1" ]; then
	p=/data/hack/utorrent
	rm $p/settings.*
	export HOME=$p
	export PATH=$p:$p/lib:/data/hack/lib:/opt/local/bin:/usr/local/bin:/usr/bin:/bin:/opt/local/sbin:/usr/local/sbin:/usr/sbin:/sbin:/scripts
	export LD_LIBRARY_PATH=$p/lib:/data/hack/lib:.:/data/hack/bin:/opt/local/lib:/usr/local/lib:/usr/lib:/lib:/lib/gstreamer-0.10:/opt/local/lib/qt
	$p/lib/ld-linux.so.2 $p/utserver -settingspath $p/ -configfile $p/utserver.conf -daemon > /data/hack/utorrent/server.log 2> /dev/null &
fi
