#!/bin/sh

# turn the logo red to indicate we're installing
dtool 6 1 0 100
dtool 6 2 0 0

# download the latest version from github
rm -Rf /download/boxeehack-master
rm /download/boxeehack.zip
cd /download
/bin/busybox wget http://nodeload.github.com/boxeehacks/boxeehack/zip/master -O boxeehack.zip
/bin/busybox unzip boxeehack.zip
cd /

# copy the hack folder, make the hack run at boot, and clean up
rm -Rf /data/hack
mv /download/boxeehack-master/hack /data/

rm -Rf /download/boxeehack-master
rm /download/boxeehack.zip

cp /data/hack/advancedsettings.xml /data/.boxee/UserData/advancedsettings.xml
cp /data/hack/boxeehal.conf /data/etc/boxeehal.conf

# turn the logo back to green
dtool 6 1 0 0
dtool 6 2 0 50

# reboot the box to activate the hack
reboot
