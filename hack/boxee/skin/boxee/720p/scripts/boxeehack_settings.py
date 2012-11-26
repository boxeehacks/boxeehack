import os
import xbmc, xbmcgui
import ConfigParser

available_providers = ['Addic7ed', 'BierDopje', 'OpenSubtitles', 'SubsWiki', 'Subtitulos']

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

def defaults_function():
    enable_subs = subtitle_function("get")
    subtitle_provider("get", "default")
    subtitle_provider("get", "tv")
    subtitle_provider("get", "movie")
    xbmc.executebuiltin("Skin.SetString(subtitles-plugin,%s)" % enable_subs ) 
    
def telnet_function(method):
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

def subtitle_function(method):
    subtitles = file_get_contents("/data/etc/.subtitles_enabled")
    if(method == "get"):
	return subtitles

    if subtitles == "1":
        subtitles = "0"
    else:
        subtitles = "1"

    if(method == "set"):
    	file_put_contents("/data/etc/.subtitles_enabled", subtitles)
    	os.system("sh /data/hack/subtitles.sh")
    	xbmc.executebuiltin("Skin.SetString(subtitles-plugin,%s)" % subtitles )    

def subtitle_provider(method, section, provider=None):
    config = ConfigParser.SafeConfigParser({"lang": "All", "plugins" : "BierDopje,OpenSubtitles", "tvplugins" : "BierDopje,OpenSubtitles", "movieplugins" : "OpenSubtitles" })
    if os.path.exists("/data/hack/boxee/scripts/OpenSubtitles/resources/lib/config.ini"):
    	config.read("/data/hack/boxee/scripts/OpenSubtitles/resources/lib/config.ini")
    plugins = config.get("DEFAULT", "plugins")	
    plugin_section = "default"
    config_section = "plugins"
    if(section == "tv"):
	plugins = config.get("DEFAULT", "tvplugins")
	plugin_section = "tv"
	config_section = "tvplugins"
    if(section == "movie"):
	plugins = config.get("DEFAULT", "movieplugins")
	plugin_section = "movie"
	config_section = "movieplugins"
    
    enabled_providers = plugins.split(',')
    if(method == "get"):
	if(provider != None):
		if(provider in enabled_providers):
			return 1
		else:
			return 0

    	for checkprovider in available_providers:
		result = 0
		if(checkprovider in enabled_providers):
			result = 1
		xbmc.executebuiltin("Skin.SetString(subtitles-plugin-%s-%s,%s)" % (plugin_section, checkprovider, result))
    if(method == "set"):
	provider_status = 1
	if(provider in enabled_providers):
        	provider_status = 0
	
	if(provider_status == 1):
		enabled_providers.append(provider)
		xbmc.executebuiltin("Skin.SetString(subtitles-plugin-%s-%s,%s)" % (plugin_section, provider, 1))
	else:
		enabled_providers.remove(provider)
		xbmc.executebuiltin("Skin.SetString(subtitles-plugin-%s-%s,%s)" % (plugin_section, provider, 0))
	config.set("DEFAULT", config_section, ",".join(enabled_providers).strip(','))
     	if os.path.exists("/data/hack/boxee/scripts/OpenSubtitles/resources/lib/config.ini"):
		configfile = open("/data/hack/boxee/scripts/OpenSubtitles/resources/lib/config.ini", "w")
		config.write(configfile)
		configfile.close()
    
def version_function(method):
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
    method = sys.argv[1]
    if sys.argv[2] == "telnet":
        telnet_function(method)
    if sys.argv[2] == "subtitles":
        subtitle_function(method)
    if sys.argv[2] == "version":
        version_function(method)
    if sys.argv[2] == "defaults":
        defaults_function()
    if sys.argv[2] == "subtitles-provider":
        subtitle_provider(method, sys.argv[3], sys.argv[4])
