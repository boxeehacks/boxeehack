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
/bin/busybox sed -i "s/;sh \/media\/BOXEE\/install.sh//g" /data/etc/boxeehal.conf 
/bin/busybox sed -i "s/; sh \/media\/BOXEE\/install.sh//g" /data/etc/boxeehal.conf
/bin/busybox sed -i "s/;sh \/data\/hack\/boot.sh//g" /data/etc/boxeehal.conf 
/bin/busybox sed -i "s/; sh \/data\/hack\/boot.sh//g" /data/etc/boxeehal.conf 
/bin/busybox sed -i "s/;sh \/media\/BOXEE\/install.sh//g" /data/.boxee/UserData/guisettings.conf 
/bin/busybox sed -i "s/; sh \/media\/BOXEE\/install.sh//g" /data/.boxee/UserData/guisettings.conf
/bin/busybox sed -i "s/;sh \/data\/hack\/boot.sh//g" /data/.boxee/UserData/guisettings.conf 
/bin/busybox sed -i "s/; sh \/data\/hack\/boot.sh//g" /data/.boxee/UserData/guisettings.conf 
/bin/busybox sed -i "s/\"hostname\":\"boxeebox/\"hostname\":\"boxeebox;sh \/data\/hack\/boot.sh/g" /data/etc/boxeehal.conf 
/bin/busybox sed -i "s/\>boxeebox\</\>boxeebox;sh \/data\/hack\/boot.sh\</g" /data/.boxee/UserData/guisettings.xml 

if ! [ -f /data/etc/passwd ]; then
	echo "secret" > /data/etc/passwd
fi

# turn the logo back to green
dtool 6 1 0 0
dtool 6 2 0 50

# reboot the box to activate the hack
sleep 3
reboot

#/data/hack/bin/busybox telnetd -p 2323 -l /data/hack/shell.sh &
