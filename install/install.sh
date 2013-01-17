#!/bin/sh

BASEDIR=`dirname $0`

# turn the logo red to indicate we're installing
dtool 6 1 0 100
dtool 6 2 0 0

# stop Boxee from running and screwing things up
killall U99boxee; killall BoxeeLauncher; killall run_boxee.sh; killall Boxee; killall BoxeeHal

# stop dropbear
killall dropbear

# cleanup some old stuff first
umount -f /opt/boxee/skin
umount -f /opt/boxee/media/boxee_screen_saver
umount -f /opt/boxee/skin/boxee/720p
umount -f /opt/boxee/visualisations/projectM
umount -f /etc

echo $BASEDIR/hack

if [ -d "$BASEDIR/hack" ];
then
    # install the version from the USB drive
    rm -Rf /data/hack
    cp -R "$BASEDIR/hack" /data/
else
    # download the latest version from github
    rm -Rf /download/boxeehack-master
    rm /download/boxeehack.zip
    cd /download
    /opt/local/bin/curl -L https://github.com/boxeehacks/boxeehack/archive/master.zip -o boxeehack.zip
    /bin/busybox unzip boxeehack.zip

    # copy the hack folder, and clean up
    rm -Rf /data/hack
    cp -R /download/boxeehack-master/hack /data/

    rm -Rf /download/boxeehack-master
    rm /download/boxeehack.zip
fi

# make everything runnable
chmod -R +x /data/hack/*.sh
chmod -R +x /data/hack/bin/*

# run the hack at next boot
mv /data/hack/advancedsettings.xml /data/.boxee/UserData/advancedsettings.xml
/bin/busybox sed -i 's/"hostname":"\([^;]*\);.*","p/"hostname":"\1","p/g' /data/etc/boxeehal.conf
/bin/busybox sed -i 's/<hostname>\([^;]*\);.*<\/hostname>/<hostname>\1<\/hostname>/g' /data/.boxee/UserData/guisettings.xml
/bin/busybox sed -i 's/","password/;sh \/data\/hack\/boot.sh","password/g' /data/etc/boxeehal.conf
/bin/busybox sed -i "s/<\/hostname>/;sh \/data\/hack\/boot.sh\<\/hostname>/g" /data/.boxee/UserData/guisettings.xml
touch /data/etc/boxeehal.conf
touch /data/.boxee/UserData/guisettings.xml

# Make root home directory
mkdir -p /data/root
chmod 0644 /data/root

# Copy /etc to make it writable
if [ ! -d /data/hack-etc ];
then
    cp -ar /etc /data/hack-etc
    cp -ar /data/hack/etc/* /data/hack-etc/
    chmod +x /data/hack-etc/ppp/* # vpn fixes from network.sh
fi;

# fix possibly broken dropbear links
ln -s dropbearmulti /data/hack/bin/dropbearkey
ln -s dropbearmulti /data/hack/bin/dropbear
ln -s dropbearmulti /data/hack/bin/dbclient
ln -s dropbearmulti /data/hack/bin/scp

# turn the logo back to green
sleep 5
dtool 6 1 0 0
dtool 6 2 0 50

# reboot the box to activate the hack
rm /download/install.sh; reboot
