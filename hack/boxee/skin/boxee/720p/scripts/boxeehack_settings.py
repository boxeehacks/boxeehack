import os
import xbmc, xbmcgui

def file_get_contents(filename):
  if os.path.exists(filename):
    fp = open(filename, "r")
    content = fp.read()
    fp.close()
    return content
  return ""

def file_put_contents(filename, content):
  fp = open(filename, "w")
  fp.write(content)
  fp.close()

def telnet_function():
    passwd = file_get_contents("/data/etc/passwd")
    kb = xbmc.Keyboard('default', 'heading', True)
    kb.setDefault(passwd) # optional
    kb.setHeading('Enter telnet password') # optional
    kb.setHiddenInput(True) # optional
    kb.doModal()
    if (kb.isConfirmed()):
        passwd = kb.getText()

    if (passwd == ""):
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('Telnet', 'The telnet password must not be empty.')
    else:
        file_put_contents("/data/etc/passwd", passwd)    

def subtitle_function():
    subtitles = file_get_contents("/data/etc/.subtitles_enabled")

    if subtitles == "1":
        subtitles = "0"
    else:
        subtitles = "1"

    xbmc.executebuiltin("Skin.SetString(subtitles-plugin,%s)" % subtitles)
    file_put_contents("/data/etc/.subtitles_enabled", subtitles)

#    dialog = xbmcgui.Dialog()
#    ret = dialog.yesno('Subtitles Plugin', 'Do you want to reboot now?')
#    if ret == 1:
    os.system("sh /data/hack/subtitles.sh")

def livetvcatchup_function():
    livetvcatchup = file_get_contents("/data/etc/.livetvcatchup_enabled")

    if livetvcatchup == "1":
        livetvcatchup = "0"
    else:
        livetvcatchup = "1"

    xbmc.executebuiltin("Skin.SetString(livetvcatchup,%s)" % livetvcatchup)
    file_put_contents("/data/etc/.livetvcatchup_enabled", livetvcatchup)

def version_function():
    import urllib2
    u = urllib2.urlopen('https://raw.github.com/boxeehacks/boxeehack/master/hack/version')
    version_remote = "%s" % u.read()
    version_local = file_get_contents("/data/hack/version")

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

    dialog = xbmcgui.Dialog()
    if hasnew:
        dialog.ok("BoxeeHack Version", "A new version of BoxeeHack is available. Upgrade to %s" % (version_remote))
    else:
        dialog.ok("BoxeeHack Version", "Your BoxeeHack version is up to date.")

if (__name__ == "__main__"):
    if sys.argv[1] == "telnet":
        telnet_function()
    if sys.argv[1] == "subtitles":
        subtitle_function()
    if sys.argv[1] == "livetvcatchup":
        livetvcatchup_function()
    if sys.argv[1] == "version":
        version_function()
