#!/bin/sh
mkdir /data/media
mount -o bind /tmp/mnt /data/media
nohup /data/hack/bin/busybox tcpsvd -vE 0.0.0.0 21 /data/hack/bin/busybox ftpd -w /data > /dev/null &

