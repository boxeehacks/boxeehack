#!/bin/sh

# turn the logo red to indicate we're installing
dtool 6 1 0 100
dtool 6 2 0 0

# make an install dir on a partition we know is enough space
mkdir /data/install
cp support/* /data/install
chmod -R +x /data/install/*

cd /download
/data/install/git clone git://github.com/boxeehacks/boxeehack.git
cd /

mv /download/boxeehack/hack /data/
rm -Rf /download/boxeehack
cp /data/install/boxeehal.conf /data/etc/
rm -Rf /data/install

/data/hack/boot.sh
killall Boxee

dtool 6 1 0 0
dtool 6 2 0 50
