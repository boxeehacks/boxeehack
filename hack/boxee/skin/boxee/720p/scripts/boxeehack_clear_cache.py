import os,mc
import xbmc, xbmcgui

def fanart_function():
    if mc.ShowDialogConfirm("Clear fanart cache", "Are you sure you want to clear the fanart cache?", "Cancel", "OK"):
        pass

def thumbnail_function():
    if mc.ShowDialogConfirm("Clear thumbnail cache", "Are you sure you want to clear the thumbnail cache?", "Cancel", "OK"):
        os.system("rm /data/etc/.fanart")
        os.system("find /data/.boxee/UserData/profiles/*/Thumbnails/ -name \*.tbn | xargs rm")
        mc.ShowDialogNotification("Clearing thumbnail cache")

if (__name__ == "__main__"):
    section = sys.argv[1]

    if section == "fanart":
        fanart_function()
    if section == "thumbnail":
        thumbnail_function()
