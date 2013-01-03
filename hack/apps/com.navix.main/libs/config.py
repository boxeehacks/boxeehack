from default import *
from tools import *

#Module specific Imports
import marshal
import binascii

######
### CONFIG
######
### Sets base config on startup
######

class Navi_VARS:
    def __init__(self):
        #App location
        self.rootDir  = ROOT
        self.dataDir  = os.path.join(self.rootDir, "data")
        self.tempDir  = xbmc.translatePath('special://temp')
        self.appid    = os.path.basename(self.rootDir)
        self.parking  = {}

        #Load settings options
        self.options = json_loads(path=os.path.join(self.dataDir, 'settings', 'options.json'))

        #Get Media dir
        if IsBoxee():
            self.mediaDir = 'special://home/apps/%s/skin/Boxee Skin NG/media/' % self.appid
        if IsXBMC():
            self.mediaDir = 'special://home/addons/%s/resources/skins/Default/media/' % self.appid

        #Check if embedded
        if IsBoxee():
            import mc
            try:    self.embedded = mc.IsEmbedded()
            except: self.embedded = False
        else:
            self.embedded = False

        #Load settings.json
        if self.embedded:
            import mc
            try:
                settings = marshal.loads(binascii.unhexlify(mc.GetApp().GetLocalConfig().GetValue('settings')))
            except:
                mc.GetApp().GetLocalConfig().SetValue('settings', '')
                settings = ''
        else:
            settings = json_loads(path=os.path.join(self.dataDir, 'settings', 'settings.json'))

        if settings:
            self._settings = settings.keys()
            for item in self._settings:
                vars(self)[item] = settings[item]
        else:
            self.loadDefaults()

        #Load language
        languages = json_loads(path=os.path.join(self.dataDir, 'languages', str(self.language)))
        self.local = {}
        for id, value in languages.items():
            self.local[id] = value.encode('utf-8')
        
        if self.url_download_location == 'not set' and not self.embedded:
            self.url_download_location = os.path.join(self.dataDir, 'download')

        #Load scrapers.json
        Log(self, 'NAVI-X: Loading sources from %s' % SOURCES)
        try:
            source_json = urlopen(self, SOURCES, {'action':'read'})['content']
            self.sources = json_loads( string=source_json )
            self.sources['scrapers']
        except:
            Log(self, 'NAVI-X: Failed fetching external sources - loading default')
            self.sources = json_loads(path=os.path.join(self.dataDir, 'settings', 'sources.json'))

        self.getOS()
        self.compile()

    ### Save settings
    def save(self):
        data = {}
        for key in self._settings:
            data[key] = vars(self)[key]
            
        if self.embedded:
            import mc
            mc.GetApp().GetLocalConfig().SetValue('settings', binascii.hexlify(marshal.dumps(data)))
        else:
            json_dumps(data, os.path.join(self.dataDir, 'settings', 'settings.json'))

    ### Determine os
    def getOS(self):
        platform_tag = sys.platform
        if 'linux' in platform_tag:
            self.os = "linux"
        elif 'win32' in platform_tag:
            self.os = "windows"
        elif 'darwin' in platform_tag:
            self.os = "osx"

    ### Pre-Init compiles for speed
    def compile(self):
        self.regex = {
            'item_name':re.compile('(\[.*?\])'),
            'plx_name':re.compile('name=(.*?)\\n'),
            'js_name':re.compile('name\:\"(.*?)\"'),
            'js_id':re.compile('\'(.*?)\'\:\{'),
            'del_html_tags':re.compile(r'<.*?>')
            }
            
    ### Load defaults
    def loadDefaults(self):
        settings = json_loads(path=os.path.join(self.dataDir, 'settings', 'settings_default.json'))
        self._settings = settings.keys()
        for item in self._settings:
            vars(self)[item] = settings[item]
        self.save()







