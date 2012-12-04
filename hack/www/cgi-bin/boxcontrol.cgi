#!/bin/sh

echo "Content-type: text/html"
echo ""

VAR=$QUERY_STRING

case $VAR in
	ftp)
		RUN=$(ps aux | grep 'ftp' | grep -v 'grep' | grep -v 'sh boxcontrol.cgi' | awk '{print $2}')
		if [ "$RUN" == "" ]
		then
			sh /data/hack/ftp.sh
			echo "ftp Running"
		else
			kill -9 $RUN
			echo "ftp Stopped"
		fi
	;;
	
	telnetd)
		RUN=$(ps aux | grep 'telnetd' | grep -v 'grep' | grep -v 'sh boxcontrol.cgi' | awk '{print $2}')
	
		if [ "$RUN" == "" ]
		then 	
			sh /data/hack/telnet.sh
			echo "telnetd Running"
		else
			kill -9 $RUN
			echo "telnetd Stopped"
		fi
	;;
	
	www)
		RUN=$(ps aux | grep 'httpd' | grep -v 'grep' | grep -v 'sh boxcontrol.cgi' | awk '{print $2}')
	
		if [ "$RUN" == "" ]
		then 	
			sh /data/hack/www.sh
			echo "www Running"
		else
			kill -9 $RUN
			echo "www Stopped"
		fi
	;;	
	
	reboot)
		reboot
	;;	
	
	poweroff)
		poweroff
	;;
	
	ledoff)
		printf "\xAA\x06\x35\x30\x30\x33\x30\x30\x35\x33" > /dev/ttyS1
	;;
	
	red)
		printf "\xAA\x06\x35\x30\x30\x33\x30\x30\x35\x33" > /dev/ttyS1
		printf "\xAA\x06\x35\x30\x30\x31\x36\x34\x42\x35" > /dev/ttyS1
	;;
	
	green)
		printf "\xAA\x06\x35\x30\x30\x33\x30\x30\x35\x33" > /dev/ttyS1
		printf "\xAA\x06\x35\x30\x30\x32\x36\x34\x42\x36" > /dev/ttyS1
	;;
	
	yellow)
		printf "\xAA\x06\x35\x30\x30\x33\x30\x30\x35\x33" > /dev/ttyS1
		printf "\xAA\x06\x35\x30\x30\x31\x36\x34\x42\x35" > /dev/ttyS1
		printf "\xAA\x06\x35\x30\x30\x32\x36\x34\x42\x36" > /dev/ttyS1
	;;
	
	bGreen)
		printf "\xaa\x08\x35\x30\x30\x32\x30\x33\x34\x42\x41\x30" > /dev/ttyS1	
	;;	
	
	*)
	
	;;
esac
