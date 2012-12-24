#!/bin/sh
VALID_PASSWORD=`head -n 1 /data/etc/passwd`

THEPATH='/data/hack/bin:/opt/local/bin:/usr/local/bin:/usr/bin:/bin:/opt/local/sbin:/usr/local/sbin:/usr/sbin:/sbin:/scripts'

for f in /data/plugins/*; do
	if [ -d ${f}/bin ]; then
		THEPATH="${f}/bin:${THEPATH}"
	fi
done

export PATH="${THEPATH}"
export LD_LIBRARY_PATH='.:/data/hack/lib:/opt/local/lib:/usr/local/lib:/usr/lib:/lib:/lib/gstreamer-0.10:/opt/local/lib/qt'
export HOME='/data/hack'
export ENV='/data/etc/.profile'

read -s -p "Password: " PASSWORD

echo ""
if [ "$PASSWORD" == "$VALID_PASSWORD" ]; then
        echo "-------------------"
        echo " Welcome to Boxee+ "
        echo "-------------------"

	cd /data/hack

        /bin/sh
else
        echo "Incorrect password"       
fi
