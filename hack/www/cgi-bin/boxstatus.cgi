#!/bin/sh

echo "Content-type: text/html"
echo ""

VAR=$QUERY_STRING

STATUS=$(ps aux | grep $VAR | grep -v 'grep' | grep -v 'sh fBoxStatus.cgi' | awk '{print $2}')

if [ "$STATUS" == "" ]
then
	echo $VAR " Stopped"
else
	echo $VAR " Running"
fi
