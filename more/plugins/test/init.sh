#!/bin/sh

BASEDIR=`dirname $0`

if [ "$1" == "start" ]; then
    chmod +x ${BASEDIR}/bin/test_plugin
	echo "Test Plugin Started"
elif [ "$1" == "stop" ]; then
	echo "Test Plugin Stopped"
else
	echo "What now?"
fi
