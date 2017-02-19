#!/bin/sh
space=`df 2>/dev/null | grep /data | grep Glob | awk '{ print $4 }'`
if [ $space -lt 25000 ]; then
	find /data/.boxee/UserData/profiles/*/Thumbnails/ -name \*.tbn | xargs rm
fi
