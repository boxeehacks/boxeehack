#!/bin/sh
VALID_PASSWORD="secret"

export LD_LIBRARY_PATH='.:/data/hack/lib:/opt/local/lib:/usr/local/lib:/usr/lib:/lib:/lib/gstreamer-0.10:/opt/local/lib/qt'
export PATH='/data/hack/bin:/opt/local/bin:/usr/local/bin:/usr/bin:/bin:/opt/local/sbin:/usr/local/sbin:/usr/sbin:/sbin:/scripts'

read -s -p "Password: " PASSWORD

echo ""
if [ "$PASSWORD" == "$VALID_PASSWORD" ]; then
        echo "---------------------"
        echo " Welcome to BoxeeBox "
        echo "---------------------"
        sh
else
        echo "Incorrect password"       
fi
