#!/bin/sh

## Stop native webserver

killall -9 thttpd_wrapper
killall -9 thttpd

## Start non-native webserver

/data/hack/bin/busybox httpd -p 80 -h /data/hack/www -c /data/hack/httpd.conf &

