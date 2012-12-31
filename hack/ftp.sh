#!/bin/sh
nohup /data/hack/bin/busybox tcpsvd -vE 0.0.0.0 21 /data/hack/bin/busybox ftpd -w / > /dev/null &

