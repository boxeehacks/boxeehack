import os
import xbmc, xbmcgui

def fanart_function():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Clear fanart cache", "Are you sure you want to clear the fanart cache?"):
        pass

def thumbnail_function():
    dialog = xbmcgui.Dialog()
    os.system("rm /data/etc/.fanart")
    if dialog.yesno("Clear thumbnail cache", "Are you sure you want to clear the thumbnail cache?"):
        os.system("find /data/.boxee/UserData/profiles/*/Thumbnails/ -name \*.tbn | xargs rm")
        xbmc.executebuiltin("Notification(,Clearing thumbnail cache,3000)")

if (__name__ == "__main__"):
    section = sys.argv[1]

    if section == "fanart":
        fanart_function()
    if section == "thumbnail":
        thumbnail_function()
