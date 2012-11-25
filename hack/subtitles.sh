#!/bin/sh
SUBTITLES_ENABLED=`head -n 1 /data/etc/.subtitles_enabled`

if [ "$SUBTITLES_ENABLED" == "1" ]; then

	mount -o bind /data/hack/boxee/scripts/OpenSubtitles /opt/boxee/scripts/OpenSubtitles

else

	umount -f /opt/boxee/scripts/OpenSubtitles

fi
