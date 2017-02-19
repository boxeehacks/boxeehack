#!/bin/sh
cp /data/hack/misc/advancedsettings.xml /.boxee/UserData/
rm -Rf /.boxee/UserData/Thumbnails/
killall Boxee
