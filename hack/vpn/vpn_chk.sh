#!/bin/sh
#
# Author: n3!
#

host=`sed -n '/vpn*/,/<\/vpn>/p' /data/.boxee/UserData/guisettings.xml > /tmp/vpn_chk.tmp | grep server /tmp/vpn_chk.tmp | awk -F'>' '{print $2}' | awk -F'<' '{print $1}'`

if [ "$host" = "" ]; then
	rm /data/hack/vpn/vpn.enabled
else
	touch /data/hack/vpn/vpn.enabled
fi

rm /tmp/vpn_chk.tmp
