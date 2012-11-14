#!/bin/sh

BASEDIR=$(dirname $0)
cd $BASEDIR

# turn the logo red to indicate we're installing
dtool 6 1 0 100
dtool 6 2 0 0

# make an install dir on a partition we know is enough space
rm -Rf /data/install
mkdir /data/install
cp -R support/* /data/install
chmod -R +x /data/install/*

# checkout the latest version from github
rm -Rf /download/boxeehack
cd /download
/data/install/git clone git://github.com/boxeehacks/boxeehack.git
cd /

# copy the hack folder, make the hack run at boot, and clean up
mv /download/boxeehack/hack /data/
rm -Rf /download/boxeehack
cp /data/install/boxeehal.conf /data/etc/
rm -Rf /data/install

# turn the logo back to green
dtool 6 1 0 0
dtool 6 2 0 50

# reboot the box to activate the hack
reboot
