#!/bin/sh
mkdir /data/hack/splash/Fonts/
cp -R /opt/boxee/media/Fonts/* /data/hack/splash/Fonts/
mount -o bind /data/hack/splash /opt/boxee/media
