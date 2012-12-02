#!/bin/sh

# turn the logo red to indicate we're installing
dtool 6 1 0 100
dtool 6 2 0 0

# download the latest version from github
rm -Rf /download/boxeehack-master
rm /download/boxeehack.zip
cd /download
/opt/local/bin/curl -L https://github.com/boxeehacks/boxeehack/archive/master.zip -o boxeehack.zip
/bin/busybox unzip boxeehack.zip

# copy the hack folder, make the hack run at boot, and clean up
umount -f /opt/boxee/skin
umount -f /opt/boxee/skin/boxee/720p
rm -Rf /data/hack
mv /download/boxeehack-master/hack /data/
chmod -R +x /data/hack/*.sh
chmod -R +x /data/hack/bin/*

rm -Rf /download/boxeehack-master
rm /download/boxeehack.zip

mv /data/hack/advancedsettings.xml /data/.boxee/UserData/advancedsettings.xml
/bin/busybox sed -i 's/"hostname":"\(.*\);.*","p/"hostname":"\1","p/g' /data/etc/boxeehal.conf
/bin/busybox sed -i 's/<hostname>\(.*\)<\/hostname>/<hostname>\1<\/hostname>/g' /data/.boxee/UserData/guisettings.xml
/bin/busybox sed -i 's/","password/;sh \/data\/boot\/hack.sh","password/g' /data/etc/boxeehal.conf 
/bin/busybox sed -i "s/<\/hostname>/;sh \/data\/hack\/boot.sh\<\/hostname>/g" /data/.boxee/UserData/guisettings.xml 

if ! [ -f /data/etc/passwd ]; then
	echo "secret" > /data/etc/passwd
fi

# turn the logo back to green
dtool 6 1 0 0
dtool 6 2 0 50

# reboot the box to activate the hack
sleep 3
rm /download/install.sh; reboot

#/data/hack/bin/busybox telnetd -p 2323 -l /data/hack/shell.sh &
