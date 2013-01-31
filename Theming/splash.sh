#!/bin/sh
mkdir /data/hack/boxee/skin/ExampleTheme/splash/Fonts/
cp -R /opt/boxee/media/Fonts/* /data/hack/boxee/skin/ExampleTheme/splash/Fonts/
mount -o bind /data/hack/boxee/skin/ExampleTheme/splash /opt/boxee/media
#change the words 'ExampleTheme' to the name of your theme remember it is case sensitive.