#!/bin/sh

for f in /download/*; do
	if [ ${f} != "/download/xbmc" ]; then
		if ! [ -h "${f}" ]; then
			echo "Removing ${f}"
			rm -fr "${f}"
		fi
	fi
done
