import os
import xbmc, xbmcgui

def get_homestart():
    homestart = file_get_contents("/data/etc/.homestart")
    if homestart == "":
        homestart = "Home"
    return homestart

def onload_homestart():
    homestart = file_get_contents("/data/etc/.homestart")
    if homestart == "":
        homestart = "Home"
    if homestart == "Movies":
	xbmc.executebuiltin("ActivateWindow(10481,boxeeui://movies/)")
    if homestart == "TV Shows":
	xbmc.executebuiltin("ActivateWindow(10480,boxeeui://shows/)")
    if homestart == "Music":
	xbmc.executebuiltin("ActivateWindow(10484,boxeeui://music/)")
    if homestart == "Files":
	xbmc.executebuiltin("ActivateWindow(10479)")
    if homestart == "Apps":
	xbmc.executebuiltin("ActivateWindow(10482,boxeeui://apps/)")
    if homestart == "Photos":
	xbmc.executebuiltin("ActivateWindow(10491)")
#    if homestart == "Web":
#	xbmc.executebuiltin("ActivateWindow()")

    return

# Enable/disable the startup functionality
def set_homestart():
	homestart = sys.argv[2]

	file_put_contents("/data/etc/.homestart", homestart)
	xbmc.executebuiltin("Skin.SetString(homestart_plugin,%s)" % homestart ) 
	return

def homestart_next():
	homestart = get_homestart()
	homestart2 = homestart
	if homestart == "Home":
		homestart2 = "Movies"
	if homestart == "Movies":
		homestart2 = "TV Shows"
	if homestart == "TV Shows":
		homestart2 = "Music"
	if homestart == "Music":
		homestart2 = "Files"
	if homestart == "Files":
		homestart2 = "Apps"
	if homestart == "Apps":
		homestart2 = "Photos"
	if homestart == "Photos":
		homestart2 = "Home"
	file_put_contents("/data/etc/.homestart", homestart2)
	xbmc.executebuiltin("Skin.SetString(homestart_plugin,%s)" % homestart2 ) 

def homestart_previous():
	homestart = get_homestart()
	homestart2 = homestart
	if homestart == "Home":
		homestart2 = "Photos"
	if homestart == "Movies":
		homestart2 = "Home"
	if homestart == "TV Shows":
		homestart2 = "Movies"
	if homestart == "Music":
		homestart2 = "TV Shows"
	if homestart == "Files":
		homestart2 = "Music"
	if homestart == "Apps":
		homestart2 = "Files"
	if homestart == "Photos":
		homestart2 = "Apps"
	file_put_contents("/data/etc/.homestart", homestart2)
	xbmc.executebuiltin("Skin.SetString(homestart_plugin,%s)" % homestart2 ) 

# Read file contents into a string
def file_get_contents(filename):
    if os.path.exists(filename):
        fp = open(filename, "r")
        content = fp.read()
        fp.close()
        return content
    return ""

# Write string back to a file
def file_put_contents(filename, content):
    fp = open(filename, "w")
    fp.write(content)
    fp.close()

if (__name__ == "__main__"):
    command = sys.argv[1]
    if command == "set_homestart": set_homestart()
    if command == "onload_homestart": onload_homestart()
    if command == "startup_next": homestart_next()
    if command == "startup_previous": homestart_previous()