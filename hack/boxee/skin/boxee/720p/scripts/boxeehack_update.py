import time
import os,sys
import xbmc, xbmcgui, mc
import subprocess
import common
import time
import urllib2


# Get the remote version number from github
def get_remote_version():
	u = urllib2.urlopen('http://dl.boxeed.in/version')
	version_remote = "%s" % u.read()
	return version_remote

# Get the version number for the locally installed version
def get_local_version():
	version_local = common.file_get_contents("/data/hack/version")
	return version_local

# Check for newer version
def check_new_version():
	version_remote = get_remote_version()
	version_local = get_local_version()
	
	version_remote_parts = version_remote.split(".")
	version_local_parts = version_local.split(".")

	hasnew = 0
	if version_remote_parts[0] > version_local_parts[0]:
		hasnew = 1
	elif version_remote_parts[0] == version_local_parts[0]:
		if version_remote_parts[1] > version_local_parts[1]:
			hasnew = 1
		elif version_remote_parts[1] == version_local_parts[1]:
			if version_remote_parts[2] > version_local_parts[2]:
				hasnew = 1
	issame = 0
	if version_remote_parts[0] == version_local_parts[0]:
		if version_remote_parts[1] == version_local_parts[1]:
			if version_remote_parts[2] == version_local_parts[2]:
				issame = 1

	dialog = xbmcgui.Dialog()
	if hasnew:
		if dialog.yesno("BOXEE+HACKS Version", "A new version of BOXEE+ is available. Upgrade to %s now?" % (version_remote)):
			update()
	elif issame:
		dialog.ok("BOXEE+HACKS Version", "Your BOXEE+ version is up to date.")
	else:
		dialog.ok("BOXEE+HACKS Version", "Hi there Doc Brown. How's the future?")


def update():
	version_remote = get_remote_version()

	os.system("dtool 6 1 0 100")
	os.system("dtool 6 2 0 0")

	mc.ShowDialogNotification("Beginning Upgrade")
	if os.path.exists("/media/BOXEE/hack"):
		mc.ShowDialogNotification("Found USB Drive with Boxee+")
		ev = common.file_get_contents("/media/BOXEE/hack/version")

		xbmc.executebuiltin("Notification(,Installing Boxee+,60000)")
		mc.ShowDialogWait()
		os.system("rm -Rf /data/hack")
		os.system("cp -R /media/BOXEE/hack /data/")
		os.system("chmod -R +x /data/hack/*.sh")
		os.system("chmod -R +x /data/hack/bin/*")
		mc.HideDialogWait()

	else:
		# Clean Up to Ensure we have Disk Space
		cleanupdownload()

		xbmc.executebuiltin("Notification(,Downloading Boxee+,120000)")

		mc.ShowDialogWait()
		os.system("/opt/local/bin/curl -L http://dl.boxeed.in/boxeehack.zip -o /download/boxeehack.zip")
		os.system("/opt/local/bin/curl -L http://dl.boxeed.in/boxeehack.md5 -o /download/boxeehack.md5")
		dm = common.file_get_contents("/download/boxeehack.md5")
		os.system("md5sum /download/boxeehack.zip | awk '{ print $1 }'> /download/boxeehack.md52")
		tm = common.file_get_contents("/download/boxeehack.md5")
		mc.HideDialogWait()
		if dm != tm or tm == "":
			os.system("dtool 6 1 0 0")
			os.system("dtool 6 2 0 50")
			xbmc.executebuiltin("Notification(,Download Failed - Aborting,60000)")
			return
		mc.ShowDialogNotification("Download Complete")
		time.sleep(2)

		xbmc.executebuiltin("Notification(,Extracting Archive,120000)")
		mc.ShowDialogWait()
		os.system("/bin/busybox unzip /download/boxeehack.zip -d /download/")
		mc.HideDialogWait()

		mc.ShowDialogNotification("Extraction Complete")
		time.sleep(2)

		mc.ShowDialogNotification("Verifying Extraction")
		ev = common.file_get_contents("/download/boxeehack-master/hack/version")
		if ev != version_remote:
			os.system("dtool 6 1 0 0")
			os.system("dtool 6 2 0 50")
			xbmc.executebuiltin("Notification(,Extraction Failed - Aborting,60000)")
			return
		time.sleep(2)

		xbmc.executebuiltin("Notification(,Installing Boxee+,60000)")
		mc.ShowDialogWait()
		os.system("rm -Rf /data/hack")
		os.system("cp -R /download/boxeehack-master/hack /data/")
		os.system("chmod 777 /data/hack/*.sh")
		os.system("chmod 777 /data/hack/bin/*")
		mc.HideDialogWait()

	mc.ShowDialogNotification("Verifying Installation")
	hv = common.file_get_contents("/data/hack/version")
	if ev != hv:
		os.system("dtool 6 1 0 0")
		os.system("dtool 6 2 0 50")
		xbmc.executebuiltin("Notification(,Installation Failed - Aborting,60000)")
		return
	time.sleep(2)

	mc.ShowDialogNotification("Cleaning Up")
	cleanupdownload()
	time.sleep(2)

	os.system("dtool 6 1 0 0")
	os.system("dtool 6 2 0 50")

	# No need to redo all the settings since Boxee+ is already running

	xbmc.executebuiltin("Notification(,Rebooting,120000)")
	os.system("reboot")


def cleanupdownload():
	os.system("rm -fr /download/boxeehack-master")
	os.system("rm -fr /download/boxeehack.zip")
	os.system("rm -fr /download/boxeehack.md5")
	os.system("rm -fr /download/boxeehack.md52")



if (__name__ == "__main__"):
	command = sys.argv[1]
	if command == "version": check_new_version()
