#!/bin/sh

ID=$(ps aux | grep tcpsvd | grep busybox | grep -v grep | awk '{print $2}')
ftp=$(cat /data/etc/ftp);

if [ $ID ]; then
	kill -9 $ID
elif [ ! $ID ] && [ $ftp == "1" ]; then
	if [ ! -d "/data/media" ]; then
		mkdir /data/media
	fi
	
	mount -o bind /tmp/mnt /data/media
	nohup /data/hack/bin/busybox tcpsvd -vE 0.0.0.0 21 /data/hack/bin/busybox ftpd -w /data > /dev/null &
fi
