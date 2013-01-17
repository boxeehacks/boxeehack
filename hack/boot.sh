#!/bin/sh
export PATH=/data/hack/bin:$PATH;
sh /data/hack/writable_etc.sh;
sh /data/hack/skin.sh &
sh /data/hack/splash.sh &
sh /data/hack/visualiser.sh &
sh /data/hack/subtitles.sh &
sh /data/hack/logo.sh &
sh /data/hack/apps.sh &
sh /data/hack/dropbear.sh &
sh /data/hack/plugins.sh &
