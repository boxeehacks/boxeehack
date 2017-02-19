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
  - Music icon added to the main screen and menu
  - Fan Art on movie details page
  - Fan Art on tv show overview page
  - 3D Movie overlay icon
  - Music / Concert overlay icon
  - Extra view mode for movies (small posters)
  - Mark all TV Show episodes watched or unwatched with one button
  - Custom browser home page
  - More music visualisers (+ customisable)
  - Updated busybox, and added git, nano and sqlite3 tools
  - Improved buffering for Full HD videos
  - Tweaked MTU if you're using a VPN/PPP connection
  - Rewritten subtitle system (BierDopje, OpenSubtitles, Subtitulos, SubsWiki, Addic7ed)
  - Special BoxeeHack settings menu
  - Reboot option
  - No more forced updates
  - Check for new versions

Requirements
------------

Of course you'll need a Boxee Box for this, and you'll also need an empty USB stick.

Also make sure you are on the latest firmware (1.5.1), since this hack has only been tested with that version. Particularly some skin features are used that will probably not work on older Boxee builds, and even may leave your box in an unbootable state, requiring you to do a factory reset.

This exact version can be downloaded at, and installed through the recovery mode:

http://dl.boxee.tv/version/dlink.dsm380/1.5.1.23735/boxee.iso

Installing
----------

Installing is very simple. Get a USB stick and format it. Name the new volume BOXEE. Then download the zip from github and put the contents of the "install" folder on the USB stick. In the stick's root there should be these entries:
  - install.sh
  - debug.sh
  - uninstall.sh
  - support

On your BoxeeBox go to Settings -> Network -> Servers. Check "Enable Windows file sharing" and in the "Host Name" field enter "boxeebox; sh /media/BOXEE/install.sh". As soon as you back out of that menu you should see the Boxee logo on your BoxeeBox turn red. This means it's installing. This should take a while, because it's downloading the hack including the modified skin. After it's done the Boxee UI should restart and your new features await!

See: http://www.youtube.com/watch?v=6YrjAqPqM30 for a video walkthrough of the process on the Boxee Box
See: http://boxeed.in/forums/viewforum.php?f=5 for additional help and information.
See: http://boxeed.in/ for other info.

If for some reason the hack disappears (which is still an issue with this version), just go into Settings -> Network -> Servers again and enter "boxeebox; sh /data/hack/boot.sh". After another reboot the hack should work (again).

Uninstall
---------

There are two ways to disable this hack if you want to. The quick way is to go into Settings -> Network -> Servers, and enter a new hostname (which now contains the hack), just remove everything in the edit field and type e.g. boxeebox. Then switch the boxee box off and back on again. You now no longer have the hack running, and everything should be back to normal.

You can also reenable it by adding in: "; sh /data/hack/boot.sh;" into that same hostname field again in the future.

If you want to completely uninstall you can run the uninstaller on your USB stick. Just go into Settings -> Network -> Servers, and change your hostname into "boxeebox; sh /media/BOXEE/uninstall.sh".

If you want to you can also uninstall manually:

Log in to the boxee box over telnet with: telnet [your-boxee-ip] 2323
Type in the password "secret"
Edit the boxeehal.conf file in /data/etc/boxeehal.conf using either vi or nano and remove the hack from the password field (or use the earlier instructions to disable the hack, however without rebooting).
Then remove the hack with: rm -Rf /data/hack
