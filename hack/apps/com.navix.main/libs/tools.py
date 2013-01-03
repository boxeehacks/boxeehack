from default import *

#Module specific Imports
import socket
import urllib2

import time
import datetime
import traceback
import mimetypes
import tempfile
import bz2
import binascii
import stat

try: import json
except: import simplejson as json
try: import cStringIO as StringIO
except: import StringIO

from operator import itemgetter, attrgetter

try:    from hashlib import md5
except: from md5 import md5

import marshal

### prints info to log if mode in debug
def Log(app, string):
    if app.debug:
        print string

### function to retreive http data
def urlopen(app, url, args={}):
    rdefaults={
        'agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4',
        'referer': '',
        'cookie': '',
        'action':'',
        'method': 'get',
        'postdata': '',
        'headers': {},
    }

    for ke in rdefaults:
        try:
            args[ke]
        except KeyError:
            args[ke]=rdefaults[ke]

    socket.setdefaulttimeout(float(app.url_open_timeout))

    if url.find(app.url_navi_server) != -1:
        if args['cookie'] >''  and args['cookie'][-2:] != '; ':
            args['cookie'] = '%s; ' % args['cookie']
        args['cookie'] = args['cookie'] + 'platform=%s; nxid=%s' % (PLATFORM, app.api.user_id, )

    try:
        hdr = {'User-Agent':args['agent'], 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer':args['referer'], 'Cookie':args['cookie']}
    except:
        print "Unexpected error:", sys.exc_info()[0]

    for ke in args['headers']:
        try:
            hdr[ke] = args['headers'][ke]
        except:
            print "Unexpected error:", sys.exc_info()[0]

    result ={
      	'headers':'',
      	'geturl':url,
      	'cookies':'',
        'content':''
        }

    try:
        cookieprocessor = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookieprocessor)
        urllib2.install_opener(opener)

        if args['method'] == 'get':
            req = urllib2.Request(url=url, headers = hdr)
        else:
            req = urllib2.Request(url, args['postdata'], hdr)

        response = urllib2.urlopen(req)

        cookies={}
        for c in cookieprocessor.cookiejar:
            cookies[c.name]=c.value

        result['headers'] = response.info()
        result['geturl'] = response.geturl()
        result['cookies'] = cookies
    except urllib2.URLError, e:
        app.gui.ShowDialogNotification('Error: %s' % e.reason)
        response = StringIO.StringIO('')
    except:
        Log(app, traceback.format_exc() )
        response = StringIO.StringIO('')

    if args['action'] == 'read':
        result['content'] = response.read()
        response.close()
    else:
        result['content'] = response
    return result


### Check if string is UTF-8 encoded
def checkUTF8(string):
    try:    return string.encode('utf-8')
    except: return str(string)

### Force string to be HEX
def forceHEX(string):
    return binascii.hexlify(string)

### get warning tags from item to output to INFO DIALOG
def checkStreamTags(app, item):
    path = item.path
    tags = []
    info = [key for key in app.navi_streaminfo.keys() if key in path]
    if len(info) > 0:
        tags.extend(app.navi_streaminfo[info[0]])
    if item.subtitle != '':
        tags.append('subtitle')
    return tags

### return unique values from list
def unique(inlist):
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques

### Get sublist from list of dicts based on keys
def select_sublist(list_of_dicts, **kwargs):
    return [dict(d) for d in list_of_dicts
            if all(d.get(k)==kwargs[k] for k in kwargs)]

### Checks if playlist item is recently updated
def process_date(datestring):
    if datestring == '' or len(datestring.split('-')) < 3:
        return ''
    try:
        item = datetime.datetime(*time.strptime(datestring,"%Y-%m-%d")[0:5])
        now = datetime.datetime.today()
        delta = now - item
        if delta.days < 2: return 'icons/new.png'
        else: return ''
    except: return ''

### Sort list of dicts based on key
def sort_dict(list, key, arg=False):
    return sorted(list, key=itemgetter(key), reverse=arg)

### Sort list of instances based on attribute
def sort_instance(list, key, arg=False):
    return sorted(list, key=attrgetter(key), reverse=arg)

### Load json file from hdd
def json_loads(**kwargs):
    try:
        if kwargs.get('string', False):
            data = json.loads(kwargs['string'])
        else:
            file = open(kwargs['path'], 'r')
            data = json.load(file)
            file.close()
        return data
    except:
        msg = 'NAVI-X: JSON syntax error '
        if not kwargs.get('string', False): msg = msg + os.path.basename(kwargs['path'])
        print msg
        traceback.print_exc()
        return {}

### Write json file to hdd
def json_dumps(data, path):
    try:
        file = open(path, 'w')
        json.dump(data, file, indent=3, sort_keys=True)
        file.close()
    except:
        traceback.print_exc()

### Check Ip for playable content
def ipCheck(app, item):
    url = 'http://api.ipinfodb.com/v3/ip-country/?key=053eb7bd26454dfbe57060b35e120193340c688f536899a02047fc787b88b9fa&format=xml'
    data = urlopen(app, url, {'action':'read', 'cache':0})
    try: code = re.compile('<countryCode>(.*?)</countryCode>', re.DOTALL).search(data).group(1)
    except: code = None
    if code != 'item':
        return app.gui.ShowDialogConfirm("Navi-X", app.local['93'], app.local['100'], app.local['101'])
    else: return True

### Function to support python < 2.5
def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True


### converts url string to path string
def slugify(string):
    string = string.strip().lower()
    return re.sub(r'[\s_-]+', '-', string)[:41]


### Try to find the filextension
def getFileExtension(path):
    dict = {'http://www.youtube.com':'avi', 'flyupload.com':'mp4'}

    ext = [dict[source] for source in dict.keys() if source in path]
    if len(ext) > 0:
        ext = ext[0][:3]
    else:
        url_stripped = re.sub('\?.*$', '', path) # strip GET-method args
        re_ext = re.compile('(\.\w+)$') # find extension
        match = re_ext.search(url_stripped)
        if match is None:
            ext_pos = path.rfind('.') #find last '.' in the string
            if ext_pos != -1:
                ext_pos2 = path.rfind('?', ext_pos) #find last '.' in the string
                if ext_pos2 != -1:
                    ext = path[ext_pos+1:ext_pos2][:3]
                else:
                    ext = path[ext_pos+1:][:3]
            else:
                ext = ''
            if ext != '':
                ext = '.' + ext[:3]
            else:
                ext = None
        else:
            ext = match.group(1)
    return ext

### Try to find the mime type
def getMIME(path):
    try:
        ext = getFileExtension(path)
        mime, encoding = mimetypes.guess_type(ext[1][:5])
        return mime
    except: return False

### Converst seconds to timestamp HH:MM
def GetInHMS(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

### Check if on boxee
def IsBoxee():
    if PLATFORM == 'boxee':
        return True
    else:
        return False

### Check if on xbmc
def IsXBMC():
    if PLATFORM == 'xbmc':
        return True
    else:
        return False

### Check if var1 equals var2
def IsEqual(var1, var2):
    if var1 == var2:
        return 'True'
    else:
        return ''
    
### Return folder/drive free space (in bytes)
def get_free_space(app, folder):
    if app.os == 'windows':
        try:
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
            return free_bytes.value
        except:
            return 0
    else:
        try:
            return os.statvfs(folder).f_bfree
        except:
            return 0

def can_create_file(folder_path):
    try:
        f = tempfile.TemporaryFile(dir=folder_path)
        f.close()
        return True
    except OSError:
        return False

def thumb_exists(url):
    try:
      urllib2.urlopen(urllib2.Request(url))
      return True
    except:
      return False

class storage:
    """
    Saves data to disk or persistant storage
    """

    def __init__(self, app, eol = 86400):
        self.app        = app
        self.path       = self.construct()
        self.eol        = eol
        self.clean()

    def construct(self):
        """sets cache dir in temp folder"""
        id     = self.app.appid
        prefix = "cache_"
        tmp    = self.app.tempDir
        path   = os.path.join(tmp, prefix + id)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def clean(self):
        """removes only data that has been expired (EOL)"""
        expire = time.time() - self.eol
        for item in os.listdir(self.path):
            pointer = os.path.join(self.path, item)
            if os.path.isfile(pointer):
                timestamp = os.path.getmtime(pointer)
                if timestamp <= expire:
                    os.chmod(pointer, stat.S_IWUSR)
                    os.remove(pointer)

    def empty(self, **kwargs):
        """
        removes all data from cache
        # persistent - boolean, if true empties all persistent data (optional)
        """
        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files:
                filename = os.path.join(root, name)
                os.chmod(filename, stat.S_IWUSR)
                os.remove(filename)
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        if kwargs.get('persistent', False):
            mc.GetApp().GetLocalConfig().ResetAll()


    def md5(self, string):
        """returns md5 hash of string"""
        return md5(string).hexdigest()

    def get(self, id, **kwargs):
        """
        Gets data from storage
        # id         - string, unique string to identify data
        # age        - int,    if set checks if data is not older then age in seconds (optional)
        # persistent - boolean, if true it saves the data persistent                  (optional)
        """
        if kwargs.get('age'):
            age = kwargs['age']
        else:
            age = 0

        if kwargs.get('persistent', False):
            pointer = self.md5(id)
            expire  = time.time() - age

            try:
                raw       = bz2.decompress(binascii.unhexlify(mc.GetApp().GetLocalConfig().GetValue(pointer)))
                timestamp = float(mc.GetApp().GetLocalConfig().GetValue(pointer+"_timestamp"))
                if timestamp >= expire:
                    return marshal.loads(raw)
            except:
                print traceback.format_exc()
        else:
            pointer = os.path.join( self.path, self.md5(id) )
            expire  = time.time() - age

            if os.path.isfile(pointer):
                timestamp = os.path.getmtime(pointer)
                if timestamp >= expire:
                    try:
                        fp = open( pointer)
                        data = marshal.load(fp)
                        fp.close()
                        return data
                    except:
                        print traceback.format_exc()

        return False

    def set(self, id, data, **kwargs):
        """
        Saves data to storage
        # id   - string,   unique string to identify data
        # data - any type, data to cache (string, int, list, dict)
        # persistent - boolean, if true it saves the data persistent    (optional)
        """

        if kwargs.get('persistent', False):
            pointer = self.md5(id)
            try:
                raw = marshal.dumps(data)
                mc.GetApp().GetLocalConfig().SetValue(pointer, binascii.hexlify(bz2.compress(raw)))
                mc.GetApp().GetLocalConfig().SetValue(pointer+"_timestamp", str(time.time()))
                del raw
                return True
            except:
                print traceback.format_exc()

        else:
            pointer = os.path.join( self.path, self.md5(id) )
            try:
                fp = open( pointer, "wb" )
                marshal.dump(data, fp)
                fp.close()
                return True
            except:
                print traceback.format_exc()

        return False