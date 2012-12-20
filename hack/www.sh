#!/bin/sh

ID=$(ps aux | grep httpd | grep busybox | grep -v grep | awk '{print $2}')

www=$(cat /data/etc/www);

if [ $ID ]; then
	kill -9 $ID
elif [ ! $ID ] && [ $www == "1" ]; then
	/data/hack/bin/busybox httpd -p 80 -h /data/hack/www -c /data/hack/httpd.conf &
fi
