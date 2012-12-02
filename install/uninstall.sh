#!/bin/sh

# turn the logo red to indicate we're installing
dtool 6 1 0 100
dtool 6 2 0 0

# stop Boxee from running and screwing things up
killall U99boxee
killall run_boxee.sh
killall BoxeeLauncher
killall BoxeeHal
killall Boxee

# remove all traces of the install
umount -f /opt/boxee/skin
umount -f /opt/boxee/media/boxee_screen_saver
umount -f /opt/boxee/skin/boxee/720p
rm /data/.boxee/UserData/advancedsettings.xml
/bin/busybox sed -i 's/"hostname":"\([^;]*\);.*","p/"hostname":"\1","p/g' /data/etc/boxeehal.conf
/bin/busybox sed -i 's/<hostname>\([^;]*\);.*<\/hostname>/<hostname>\1<\/hostname>/g' /data/.boxee/UserData/guisettings.xml
rm -Rf /data/hack

# on uninstall we also remove the password
rm /data/etc/passwd

# turn the logo back to green
dtool 6 1 0 0
dtool 6 2 0 50

# reboot the box to active finalize the uninstall
reboot
