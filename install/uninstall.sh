#!/bin/sh

# turn the logo red to indicate we're installing
dtool 6 1 0 100
dtool 6 2 0 0

# remove all traces of the install
rm /data/.boxee/UserData/advancedsettings.xml
rm /data/etc/boxeehal.conf
rm -Rf /data/hack

# reboot the box to active finalize the uninstall
reboot
