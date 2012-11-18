#!/bin/sh

BASEDIR=`dirname $0`

# turn the logo orange to indicate we're running
dtool 6 1 0 50
dtool 6 2 0 50

# run the telnet server
$BASEDIR/support/busybox telnetd -p 2323 -l sh &
