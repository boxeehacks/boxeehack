#!/bin/sh
chmod +x /data/hack/ppp/*
mkdir /data/hack/ppp_mnt
cp -R /etc/ppp/* /data/hack/ppp_mnt/
cp -R /data/hack/ppp/* /data/hack/ppp_mnt/
mount -o bind /data/hack/ppp_mnt /etc/ppp
