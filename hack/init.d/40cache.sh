#!/bin/sh
for m in /tmp/mnt/*; do
	if [ -d ${m}/cache ]; then
		for p in /data/.boxee/UserData/profiles/*; do
			b=`basename ${p}`
			if [ ! -d ${m}/cache/${b}/Thumbnails ]; then
				mkdir -p ${m}/cache/${b}/Thumbnails
				mkdir -p ${m}/cache/${b}/Thumbnails/Music
				mkdir -p ${m}/cache/${b}/Thumbnails/Pictures
				mkdir -p ${m}/cache/${b}/Thumbnails/Programs
				mkdir -p ${m}/cache/${b}/Thumbnails/Video
			fi
			if [ -d ${m}/cache/${b}/Thumbnails ]; then
				find ${p}/Thumbnails/ -name \*.tbn | xargs rm
				mount -o bind ${m}/cache/${b}/Thumbnails ${p}/Thumbnails
			fi
		done
		break
	fi
done
