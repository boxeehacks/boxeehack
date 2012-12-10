#!/bin/sh
mkdir /data/hack/ppp_mnt
cp -R /etc/ppp/* /data/hack/ppp_mnt/
cp -R /data/hack/ppp/* /data/hack/ppp_mnt/
mount -o bind /data/hack/ppp /etc/ppp
