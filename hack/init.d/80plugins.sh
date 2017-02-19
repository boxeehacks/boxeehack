#!/bin/sh

mkdir -p /data/plugins/

for f in /data/plugins/*; do
	if [ -f ${f}/init.sh ]; then
		chmod +x ${f}/init.sh
		${f}/init.sh start
	fi
done
