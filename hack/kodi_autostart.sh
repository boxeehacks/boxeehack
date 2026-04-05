#!/bin/sh
# kodi_autostart.sh — Auto-start Kodi when SD card is detected at boot.
# Scans /tmp/mnt/ for kodi.bin; UUID-independent.
#
# Place this file on the Boxee Box at: /data/hack/kodi_autostart.sh
# Then add this line to /data/hack/boot.sh:
#   sh /data/hack/kodi_autostart.sh &

LOG=/tmp/kodi_autostart.log
echo "$(date): kodi_autostart.sh started" > $LOG

# Wait up to 60 seconds for the Kodi SD card to be automounted
KODI_DIR=""
for i in $(seq 1 60); do
    for dir in /tmp/mnt/*/; do
        if [ -x "${dir}kodi.bin" ]; then
            KODI_DIR="${dir%/}"
            break 2
        fi
    done
    sleep 1
done

if [ -z "$KODI_DIR" ]; then
    echo "$(date): kodi.bin not found in /tmp/mnt/ — Kodi SD card not present." >> $LOG
    exit 1
fi

echo "$(date): Found Kodi at $KODI_DIR" >> $LOG

# Let the system settle before killing Boxee
sleep 3

killall Boxee BoxeeLauncher BoxeeHal 2>/dev/null
sleep 2

cd "$KODI_DIR" || exit 1

export HOME=/data
export KODI_HOME="$KODI_DIR"
export PYTHONHOME="$KODI_DIR/python2.7"
export PYTHONPATH="$KODI_DIR/python2.7:$KODI_DIR/python2.7/lib-dynload"
export LD_LIBRARY_PATH="$KODI_DIR/lib:$KODI_DIR:/opt/local/lib:/opt/boxee/lib:$LD_LIBRARY_PATH"

echo "$(date): Starting Kodi from $KODI_DIR (HOME=$HOME)" >> $LOG
exec ./kodi.bin >> $LOG 2>&1
