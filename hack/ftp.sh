#!/bin/sh
tcpsvd -vE 0.0.0.0 21 /data/hack/bin/busybox ftpd -w /data 2> /tmp/ftp.log &

