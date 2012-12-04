#! /bin/sh

INIFILE="$(pwd)/server/server.ini"
DOCROOT="$(pwd)/app/"
ROUTER="$(pwd)/server/router.php"
HOST=0.0.0.0
PORT=80

PHP=$(which php)

if [ $? != 0 ] ; then
	echo "Unable to find PHP"
	exit 1
fi

$PHP -S $HOST:$PORT -c $INIFILE -t $DOCROOT $ROUTER
