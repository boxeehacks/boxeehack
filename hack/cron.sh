#!/bin/sh

# env EDITOR=nano crontab -e


if [ -d "/data/hack/var" ]; then
	echo ""
else
	cp -r /var /data/hack/
	mkdir /data/hack/var/spool
	mkdir /data/hack/var/spool/cron
	mkdir /data/hack/var/spool/cron/crontabs

	echo "* * * * * echo "hello" >> /data/hack/hello.txt" >> /data/hack/var/spool/cron/crontabs/root
fi

mount -o bind /data/hack/var /var
