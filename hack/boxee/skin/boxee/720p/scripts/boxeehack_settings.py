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

if (__name__ == "__main__"):
    if sys.argv[1] == "telnet":
        telnet_function()
    if sys.argv[1] == "subtitles":
        subtitle_function()

#if ( __name__ == "__main__" ):
#    if len(sys.argv[ 1 ]) > 0:
#        if sys.argv[1] == "telnet":
#            telnet_function()
#        elif sys.argv[1] == "exit":
#            exit_function()
#    else:
#        xbmc.log( "No Arguments sent", xbmc.LOGNOTICE )
