#!/bin/sh

BASEDIR=`dirname $0`

touch $BASEDIR/install.log

# turn the logo red to indicate we're installing
echo "Changing Logo: Red" > $BASEDIR/install.log
dtool 6 1 0 100
dtool 6 2 0 0

# cleanup some old stuff first
echo "Cleaning up old Mounts (ignore failures)" >> $BASEDIR/install.log
umount -f /opt/boxee/skin
umount -f /opt/boxee/media/boxee_screen_saver
umount -f /opt/boxee/skin/boxee/720p
umount -f /opt/boxee/visualisations/projectM

echo "$BASEDIR/hack" >> $BASEDIR/install.log

if [ -d "$BASEDIR/hack" ];
then
	echo "Hack Directory found on USB drive" >> $BASEDIR/install.log
    # install the version from the USB drive
	rm -Rf /data/hack
    cp -R "$BASEDIR/hack" /data/
	ver_2=$(awk '{print $1}' "$BASEDIR/hack/version")
	echo "Version: $ver_2" >> $BASEDIR/install.log
else
	echo "Hack folder not found, proceeding to download"
    # download the latest version
    rm -Rf /download/boxeehack-master
    rm /download/boxeehack.zip
    cd /download
	echo "Downloading boxeehack.zip" >> $BASEDIR/install.log
    /opt/local/bin/curl -L http://boxeed.in/boxeeplus/boxeehack.zip -o boxeehack.zip
	echo "Downloading boxeehack.md5" >> $BASEDIR/install.log
    /opt/local/bin/curl -L http://boxeed.in/boxeeplus/boxeehack.md5 -o boxeehack.md5
    md5_1=$(md5sum boxeehack.zip | awk '{print $1}')
    md5_2=$(awk '{print $1}' "boxeehack.md5")
	echo "MD5 of zip: $md5_1" >> $BASEDIR/install.log
	echo "MD5 needed: $md5_2" >> $BASEDIR/install.log
    if [ "$md5_1" != "$md5_2" ] ; then
        echo "MD5s do not match, aborting" >> $BASEDIR/install.log
		dtool 6 1 0 0
		dtool 6 2 0 50
        exit
    fi

	# Extract the archive
	echo "Unzipping boxeehack.zip" >> $BASEDIR/install.log
    /bin/busybox unzip boxeehack.zip

	ver_2=$(awk '{print $1}' "/download/boxeehack-master/hack/version")
	echo "Version of unzipped: $ver_2" >> $BASEDIR/install.log
	
    # copy the hack folder, and clean up
	echo "Copying the hack folder" >> $BASEDIR/install.log
    rm -Rf /data/hack
    cp -R /download/boxeehack-master/hack /data/

	echo "Cleaning Up" >> $BASEDIR/install.log
    rm -Rf /download/boxeehack-master
    rm /download/boxeehack.zip
	rm /download/boxeehack.md5
fi

# Verify that we did extract correctly
echo "Verifying the extraction" >> $BASEDIR/install.log
ver_1=$(awk '{print $1}' "/data/hack/version")
echo "Extracted Version: $ver_1" >> $BASEDIR/install.log
if [ "$ver_1" != "$ver_2" ] ; then
    echo "Extracted versions do not match" >> $BASEDIR/install.log
	dtool 6 1 0 0
	dtool 6 2 0 50
    exit
fi

# make everything runnable
chmod -R +x /data/hack/*.sh
chmod -R +x /data/hack/bin/*

# stop Boxee from running and screwing things up
echo "Killing Boxee processes" >> $BASEDIR/install.log
killall U99boxee; killall BoxeeLauncher; killall run_boxee.sh; killall Boxee; killall BoxeeHal

# run the hack at next boot
echo "Making changes to XML files" >> $BASEDIR/install.log
mv /data/hack/advancedsettings.xml /data/.boxee/UserData/advancedsettings.xml
/bin/busybox sed -i 's/"hostname":"\([^;]*\);.*","p/"hostname":"\1","p/g' /data/etc/boxeehal.conf
/bin/busybox sed -i 's/<hostname>\([^;]*\);.*<\/hostname>/<hostname>\1<\/hostname>/g' /data/.boxee/UserData/guisettings.xml
/bin/busybox sed -i 's/","password/;sh \/data\/hack\/boot.sh","password/g' /data/etc/boxeehal.conf
/bin/busybox sed -i "s/<\/hostname>/;sh \/data\/hack\/boot.sh\<\/hostname>/g" /data/.boxee/UserData/guisettings.xml
/bin/busybox sed -i "s/<enabled>false/<enabled>true/g" /data/.boxee/UserData/guisettings.xml
		
touch /data/etc/boxeehal.conf
touch /data/.boxee/UserData/guisettings.xml

# set a password if one does not yet exist
if ! [ -f /data/etc/passwd ]; then
	echo "secret" > /data/etc/passwd
fi

# turn the logo back to green
echo "Changing Logo: Green" >> $BASEDIR/install.log
sleep 5
dtool 6 1 0 0
dtool 6 2 0 50

echo "Rebooting" >> $BASEDIR/install.log
# reboot the box to activate the hack
rm /download/install.sh; reboot
