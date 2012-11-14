#!/bin/sh
cp /data/hack/advancedsettings.xml /.boxee/UserData/
rm -Rf /.boxee/UserData/Thumbnails/
#rm -Rf /.boxee/UserData/profiles/[user]/Thumbnails/
killall Boxee

