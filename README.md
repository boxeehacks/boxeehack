BoxeeHack
=========

The BoxeeBox is quite a capable media player. At its core it is a modified version of XBMC with a number social media sharing features added on. However those modifications also limit what you can do with the Box, and removes some of the standard XBMC features.

Recently a hack was discovered that allows for full root access to the box:
http://www.gtvhacker.com/index.php/Boxee

This project is an attempt at returning some of the missing features and opening up a development path for creating new features and fixing existing annoyances.

What does it do?
----------------

  - Root access telnet support (password is "secret")
  - FTP server
  - Improved buffering for Full HD videos
  - Music icon added to the main screen and menu
  - Fan Art on movie details page
  - Updated busybox, and added git, nano and sqlite3 tools

Installing
----------

Installing is very simple. Get a USB stick and format it. Name the new volume BOXEE. Then download the zip from github and put the contents of the "install" folder on the USB stick. In the stick's root there should be two entries:
  - install.sh
  - support

On your BoxeeBox go to Settings -> Network -> Servers. Check "Enable Windows file sharing" and in the "Share Workgroup" field enter "; sh /media/BOXEE/install.sh". As soon as you back out of that menu you should see the Boxee logo on your BoxeeBox turn red. This means it's installing. This should take a while, because it's downloading the hack including the modified skin. After it's done the Boxee UI should restart and your new features await!

See: http://forums.boxee.tv/showthread.php?t=63248 for additional help and information.

