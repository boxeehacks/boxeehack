#!/bin/sh

BASEDIR=`dirname $0`

# turn the logo red to indicate we're installing
dtool 6 1 0 100
dtool 6 2 0 0

# stop Boxee from running and screwing things up
killall U99boxee; killall BoxeeLauncher; killall run_boxee.sh; killall Boxee; killall BoxeeHal

# cleanup some old stuff first
umount -f /opt/boxee/skin
umount -f /opt/boxee/media/boxee_screen_saver
umount -f /opt/boxee/skin/boxee/720p
umount -f /opt/boxee/visualisations/projectM

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

# set a password if one does not yet exist
if ! [ -f /data/etc/passwd ]; then
	echo "secret" > /data/etc/passwd
fi

# turn the logo back to green
sleep 5
dtool 6 1 0 0
dtool 6 2 0 50

# reboot the box to activate the hack
rm /download/install.sh; reboot
