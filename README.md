BoxeeHack
=========

The BoxeeBox is quite a capable media player. At its core it is a modified version of XBMC with a number social media sharing features added on. However those modifications also limit what you can do with the Box, and removes some of the standard XBMC features.

Recently a hack was discovered that allows for full root access to the box:
http://www.gtvhacker.com/index.php/Boxee

This project is an attempt at returning some of the missing features and opening up a development path for creating new features and fixing existing annoyances.

What does it do?
----------------

  - Root access telnet support
  - FTP server
  - Improved buffering for Full HD videos
  - Music icon added to the main screen and menu
  - Fan Art on movie details page
  - Updated busybox, and added git, nano and sqlite3 tools

Installing
----------

The installer for this is not yet finished. In the future you should be able to run the following command on your Mac or Linux desktop machine:

curl -L https://raw.github.com/boxeehacks/boxeehack/master/install/install.sh

It will guide you through the steps needed to prepare a USB stick for hacking the box. However for now you will have to do that yourself. Afterwards simply copy the "hack" folder to your /data/ folder on the BoxeeBox and add "; sh /data/hack/boot" to the end of your workgroup name in the samba server section of the Boxee settings.

See: http://forums.boxee.tv/showthread.php?t=63248 for additional help and information.