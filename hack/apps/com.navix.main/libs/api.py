#App Imports
from default import *
from library import *
from tools import *
from gui import *
from nipl import *
from download import *

#Module specific Imports
import csv
import urllib
import time

from itertools import izip
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup

import threading
from Queue import Queue
import traceback

######
### API
######
### Main playlist and server processing
######

class Navi_API:
    def __init__(self, app):
        #Init Api
        self.app = app
        self.download = Navi_DOWNLOAD(app)

        self.user_id = self.app.navi_id
        self.cookie = self.app.navi_cookie

        self.favorite_id = self.app.navi_favorite
        self.favorite_list = {}
        
        #Action dict key->function
        self.action = {
            'playlist':self._PLAYLIST, 
            'json':self._JSON,
            'rss':self._RSS,
            'atom':self._ATOM,
            'html_youtube':self._YOUTUBE,
            'xml_shoutcast':self._SHOUTCAST,
            'xml_applemovie':self._APPLE,
            'rss_flickr_daily':self._FLICKR,  
            'html':self.app.player.playContent,
            'video':self.app.player.playContent,
            'audio':self.app.player.playContent,
            'image':self._IMAGE,
            'script':'',
            'text':self._TXT,
            'download':self._DOWNLOAD,
            'plugin':'',
            'search':self._SEARCH,
            'search_youtube':'',
            'search_shoutcast':'',
            'sources':self._SOURCES,
            'downloads':self._DOWNLOADDIR
            }

    ######
    ### Navi api main processing function, processes the calls and performs the right function based on input
    ######

    ### process api load request
    def loads(self, item, **kwargs):
        cache = kwargs.get('cache', self.app.cache_url_time)

        #check if item exist in cache
        data = self.app.storage.get(item.path, age = cache)
        if data:
            Log(self.app, 'NAVI-X: Loaded playlist from cache - %s' % item.path)
            return data

        #Load Item
        data = {}
        try:
            if ':' in item.type:
                item.type, type = item.type.split(':')
                data = self.action[item.type.lower()](item, type)
            else:
                data = self.action[item.type.lower()](item)
        except:
            Log(self.app, traceback.format_exc() )

        if data:
            data['URL']  = getattr(item, 'path', '')
            data['type'] = getattr(item, 'type', '')

        #Save to cache
        if cache > 0:
            self.app.storage.set(item.path, data)

        Log(self.app, 'NAVI-X: Loaded playlist - %s' % item.path)
        return data

    ######
    ### Navi Server communication functions
    ######
    
    ### login user
    def login(self):
        username = self.app.gui.ShowDialogKeyboard(self.app.local['21'], "", False)
        if len(username) == 0: return -2

        password = self.app.gui.ShowDialogKeyboard(self.app.local['22'], "", True)
        if len(password) == 0: return -2

        #login to the Navi-X server
        cookies = urlopen(self.app, 'http://www.navixtreme.com/members/',{
                    'method':'post',
                    'action':'read',
                    'postdata':urllib.urlencode({'action':'takelogin', 'ajax':1, 'username':username,'password':password, 'rndval':int(time.time()) })
                })['cookies']
        try:
            self.user_id = cookies.pop('nxid')
            self.cookie = "; ".join([ "=".join([cookie, cookies[cookie]]) for cookie in cookies.keys() ])
        except:
            self.user_id = ''
            self.cookie = ''
        

        if self.user_id == '':
            self.app.gui.ShowDialogNotification(self.app.local['56'])
            self.app.gui.SetLabel(20011, self.app.local['2'])
            Log(self.app, 'NAVI-X: Login to the NXServer failed')
        else:
            self.app.gui.ShowDialogNotification(self.app.local['57'])

            Log(self.app, 'NAVI-X: Login to the NXServer was successful')
            self.app.gui.SetLabel(20011, self.app.local['1'])

            #Sync ip with device
            urlopen(self.app, 'http://www.navixtreme.com/members/',{
                    'method':'post',
                    'action':'read',
                    'postdata':urllib.urlencode({
                        'action':'ipsync',
                        'rndval':int(time.time())
                    }),
                    'cookie':self.cookie
                })['content']
            Log(self.app, 'NAVI-X: IP Synced')

            self.getFavorite()

        self.save()

    ### log out user
    def logout(self):
        self.user_id = ''
        self.save()

    ### check if logged in
    def is_user_logged_in(self):
        if self.user_id != '':
            return True
        return False

    ### save user id
    def save(self):
        self.app.navi_id = self.user_id
        self.app.navi_cookie = self.cookie
        self.app.navi_favorite = self.favorite_id
        self.app.save()

    ### rate an item
    def rate_item(self, item, rating):
        if self.is_user_logged_in() == False:
            self.app.gui.ShowDialogNotification(self.app.local['58'])
        else:
            result=urlopen(self.app, 'http://www.navixtreme.com/rate/',{
                'method':'post',
                'action':'read',
                'postdata':urllib.urlencode({'url':item.path,'rating':rating}),
            })['content']

            p = re.compile('^\d$')
            match = p.search(result)
            if match:
                self.app.gui.ShowDialogOk(self.app.local['46'], self.app.local['59'])
            else:
                self.app.gui.ShowDialogOk(self.app.local['46'], 'Error: %s' % result)

    ### get favorites
    def getFavorite(self):
        if self.favorite_id == '':
            data = urlopen(self.app, 'http://www.navixtreme.com/playlist/mine.plx',{
                    'action':'read',
                })['content']
            try:
                #get favorite plx
                self.favorite_id = re.compile('playlist/(.*?)/favorite.plx').search(data).group(1)
                Log(self.app, 'NAVI-X: Favorite plx id: %s' % self.favorite_id)
            except:
                #create favorite plx
                favorite_id = urlopen(self.app, 'http://www.navixtreme.com/mylists/',{
                        'method':'post',
                        'action':'read',
                        'postdata':urllib.urlencode({
                            'action':'list_save','background':'','description':'','icon_playlist':'','id':'','is_adult':0,'is_home':1,
                            'is_private':1,'logo':'','player':'','title':'Favorite','rndval':int(time.time())
                        }),
                        'cookie':self.cookie
                    })['content']

                if len(favorite_id) > 100:
                    self.login()
                    self.getFavorite()
                    return
                else:
                    self.favorite_id = favorite_id

                urlopen(self.app, 'http://www.navixtreme.com/mylists/',{
                    'method':'post',
                    'action':'read',
                    'postdata':urllib.urlencode({
                        'URL':'','action':'item_save','background': '','description': '','list_id':self.favorite_id,'list_pos':'top',
                        'name':'Navi-X Favorite Readme','player':'','playpath':'','plugin_type':'music','processor':'','text_local':1,
                        'this_list_id':'','thumb':'',
                        'txt':  'Thank you for using Navi-X.\n\n'+ \
                                'The favorite section has been adapted since the previous Navi-X version. All your favorites are now stored online at http://www.navixtreme.com.  As long as you are logged in you can add items to your favorites from the menu.\n\n' + \
                                'When you are logged out you see the top 24h of all users instead of your personal favorites.\n'+ \
                                'Any items added will be by default stored as private and will not be visible by other users!\n\n'+ \
                                'You can also import and manage your favorites online using the playlist editor. See also http://www.navixtreme.com. \n\n'+ \
                                'Have fun using Navi-X!',
                        'type':'text','rndval':int(time.time())
                    }),
                    'cookie':self.cookie
                })['content']

                Log(self.app, 'NAVI-X: Favorite plx id: %s' % self.favorite_id)
            self.save()

        data = urlopen(self.app, 'http://www.navixtreme.com/mylists/?action=edit&id=%s' % self.favorite_id,{
                'action':'read',
                'cookie':self.cookie
            })['content']

        data = '{%s}' % re.compile('var item_data=\{(.*?)\}\;', re.DOTALL).search(data).group(1)

        names = self.app.regex['js_name'].findall(data)
        id = self.app.regex['js_id'].findall(data)

        self.favorite_list = {}
        for name_i, id_i in izip(names,id):
            self.favorite_list[name_i] = id_i

    ### save favorites
    def saveFavorite(self, item):
        #save item
        if item.type == 'playlist':
            item.type = 'plx'
            
        thumb =  getattr(item, 'thumb', '')
        if thumb and not thumb_exists(thumb):
            thumb = ''

        result = urlopen(self.app, 'http://www.navixtreme.com/mylists/',{
                'method':'post',
                'action':'read',
                'postdata':urllib.urlencode({
                    'URL':getattr(item, 'path', ''),
                    'action':'item_save',
                    'background': getattr(item, 'background', ''),
                    'description': getattr(item, 'description', ''),
                    'list_id':self.favorite_id,
                    'list_pos':'top',
                    'name':getattr(item, 'name', ''),
                    'player':getattr(item, 'player', ''),
                    'playpath':getattr(item, 'playpath', ''),
                    'plugin_type':'music',
                    'processor':getattr(item, 'processor', ''),
                    'text_local':0,
                    'this_list_id':'',
                    'thumb':thumb,
                    'txt':'',
                    'type':getattr(item, 'type', ''),
                    'rndval':int(time.time())
                }),
                'cookie':self.cookie
            })['content']
        if 'ok' in result:
            self.favorite_list[item.name] = re.sub("\D", "", result)
            self.app.gui.ShowDialogOk(self.app.local['3'], self.app.local['90'])
        else:
            self.app.gui.ShowDialogOk(self.app.local['3'], 'Error: %s' % result)

    ### delete favorite
    def delFavorite(self, item):
        result = urlopen(self.app, 'http://www.navixtreme.com/mylists/',{
                'method':'post',
                'action':'read',
                'postdata':urllib.urlencode({
                    'action':'item_delete',
                    'id':self.favorite_list[item.name],
                    'rndval':int(time.time())
                }),
                'cookie':self.cookie
            })['content']

        if 'ok' in result:
            self.favorite_list.pop(item.name)
            self.app.gui.ShowDialogOk(self.app.local['3'], self.app.local['91'])
        else:
            self.app.gui.ShowDialogOk(self.app.local['3'], 'Error: %s' % result)


    ######
    ### Navi internal processing
    ######

    def _PROCESSOR(self, item):
        url = "".join([item.processor, '?url=', urllib.quote_plus(item.path), '&phase=0'])
        Log(self.app, 'NAVI-X: Get Processor - ' + url)
        data = self.app.storage.get(url)
        if data:
            datalist = data
        else:
            #phase 1 retreive processor data
            rawdata = urlopen(self.app, str(url), {'cookie':'version='+VERSION+'.'+str(self.app.navi_sub_version)+'; platform='+self.app.options['navi_platform'], 'action':'read'})
            htmRaw = rawdata['content']
            htmRaw = re.sub('(?m)\r[#].+|\n[#].+|^\s+|\s+$', '\r\n', htmRaw)    #remove comments and tabs
            htmRaw = re.sub('[\r\n]+', '\n', htmRaw)                            #remove empty lines
            datalist = htmRaw.replace('\t','').split('\n')

        if datalist[0] == 'v2':
            nipl = NIPL(self.app, item, 0, datalist)
            return nipl.process()
        elif 'http' in datalist[0]:
            return self.PROCESS(item, datalist)

    ### Processor for fetching the real item path
    def PROCESS(self, item, datalist):
        url = datalist[0]
        regex = datalist[1]

        rawpage = urlopen(self.app, url, {'action':'read'})
        try: results = re.compile(regex).findall(rawpage['content'])
        except:
            Log(self.app, traceback.format_exc() )
            results = []

        if len(results) > 0:
            vars = ["".join(['v', str(i+1),'=', urllib.quote_plus(value), '&']) for i, value in enumerate(results)]
            url = "".join([item.processor, '?', "&".join(vars) ])
            rawdata = urlopen(self.app, str(url), {'cookie':'version='+VERSION+'.'+str(self.app.navi_sub_version)+'; platform='+self.app.os})
            try: path = rawdata['content'].readline()
            except: path = ''
            rawdata['content'].close()

            Log(self.app, 'NAVI-X PROCESS: Path - ' + path)

            item.setVar('path', path)
            return item
        else: return item
        


    ######
    ### Navi playlist functions
    ######

    ### Fetch playlist from navi sources.json  - type=sources
    def _SOURCES(self, item):
        id = item.path
        data = {}
        data['name'] = id + ' menu'
        data['view'] = 'thumbnails'
        data['type'] = 'sources'
        data['URL'] = id
        data['items'] = select_sublist(self.app.sources['scrapers'], tag=id)
        return data

    ### Fetch navi native 'plx' playlist type - type=playlist
    def _PLAYLIST(self, item):
        rawdata = urlopen(self.app, item.path)
        data = csv.reader(rawdata['content'], delimiter="=", quoting=csv.QUOTE_NONE, quotechar='|')

        if hasattr(item, 'maxline'): number = item.maxline
        else: number = self.app.plx_lines_max

        datalist = []
        item = {}
        description = False
        for i, line in enumerate(data):
            if i < number:
                total = len(line)
                if total > 1 and line[0][:1] != '#':
                    if line[0] == 'type':
                        if item: datalist.append(item)
                        description = False
                        item = {}

                if description:
                    if line == [] or line == ['#']:
                        item['description'] = "".join([item['description'],' \n '])
                    else:
                        item['description'] = "".join([item['description'],  "=".join(x for x in line)  ])

                elif total > 1 and line[0][:1] != '#':
                    key = line.pop(0)
                    item[key] = "=".join(x for x in line)
                    if key == 'description': description = True
            else:
                break
        if 'URL' in item.keys(): datalist.append(item)
        if len(datalist) == 0:
            return {}

        playlistdata = datalist.pop(0)
        playlistdata['items'] = datalist

        if not playlistdata['items']:
            return {}

        rawdata['content'].close()
        return playlistdata

    ### Fetch json playlist type [both yahoo pipes and navi-x search json output excepted]   - type=json
    def _JSON(self, item):
        rawdata  = urlopen(self.app, item.path, {'action':'read'})
        jsondata  = rawdata['content'].replace('null', '""')
        datalist = json_loads(string=jsondata)

        try: datalist = datalist['value']['items']
        except: pass
        
        playlistdata = {}
        if len(datalist) > 0:
            try:
                datalist[0]['type']
                playlistdata['items'] = datalist
            except:
                playlistdata = datalist.pop(0)
                playlistdata['items'] = datalist
        return playlistdata

    ### Fetch rss playlist type   - type=rss
    def _RSS(self, item, dtype=''):
        if 'rss://' in item.path:
            item.path = item.path.replace('rss:', 'http:')
        rawdata = urlopen(self.app, item.path)
        try: rss = BeautifulStoneSoup(rawdata['content'], convertEntities=BeautifulStoneSoup.XHTML_ENTITIES, smartQuotesTo="xml")
        except:
            Log(self.app, traceback.format_exc() )
            return {}

        #Playlist data
        playlistdata = {}
        try:    playlistdata['title'] = rss.channel.title.string
        except: pass
        try:    daplaylistdatata['description'] = rss.channel.description.string
        except: pass
        try:    playlistdata['logo'] = rss.channel.image.string
        except: pass

        #Items data
        data_items = []
        rss_items = rss.findAll("item")
        
        for rss_item in rss_items:
            data_item = {}
            type = ''
            try:    data_item['name'] = rss_item.find('title').string
            except: pass
            try:    data_item['name'] = rss_item.find('media:title').string
            except: pass
            try:    data_item['thumb'] = rss_item.find('thumbnail')['url']
            except: pass
            try:    data_item['thumb'] = rss_item.find('media:thumbnail')['url']
            except: pass
            try:    data_item['description'] = self.app.regex['del_html_tags'].sub('', rss_item.find('description').string).replace('&#39;','\'')
            except: pass
            try:    data_item['description'] = self.app.regex['del_html_tags'].sub('', rss_item.find('media:description').string).replace('&#39;','\'')
            except: pass
            try:    data_item['URL'] = rss_item.find('link').string
            except: pass
            try:    data_item['URL'] = rss_item.find('media:content')['url']
            except: pass
            try:    data_item['URL'] = rss_item.find('enclosure')['url']
            except: pass
            try:    type = rss_item.find('media:content')['type']
            except: pass
            try:    type = rss_item.find('enclosure')['type']
            except: pass
            
            if not dtype:
                data_item['type'] = False
                if 'audio' in type:         data_item['type'] = 'audio'
                elif 'video' in type:       data_item['type'] = 'video'
                elif 'image' in type:       data_item['type'] = 'image'
                elif 'application' in type: data_item['type'] = 'download'
                else:                       data_item['type'] = 'html'
            else:
                data_item['type'] = dtype
                #playlistdata['view'] =  'detail'
            if data_item.has_key('URL'):
                data_items.append(data_item)

        playlistdata['items'] = data_items
        return playlistdata

    ### Fetch txt info type  - type=txt
    def _TXT(self, item):
        self.app.gui.ShowDialog('dialog-text')
        rawdata = urlopen(self.app, item.path, {'action':'read'})['content']
        listItems = createList([{'label':item.name, 'description': rawdata}])
        listItems.set(GUI(window=15160, listid=90))
        return {}

    ### Fetch imaget type  - type=txt
    def _IMAGE(self, item):
        self.app.gui.ShowDialog('dialog-image')
        listItems = createList([{'label':item.name, 'thumb':item.path}])
        listItems.set(GUI(window=15210, listid=90))
        self.app.gui.ShowDialogNotification('Image: %s' % checkUTF8(item.name))
        return {}

    ### Fetch atom playlist type  - type=atom
    def _ATOM(self, item):
        if 'rss://' in item.path:
            item.path = item.path.replace('rss:', 'http:')
        rawdata = urlopen(self.app, item.path)
        try: rss = BeautifulStoneSoup(rawdata['content'], convertEntities="xml", smartQuotesTo="xml")
        except:
            Log(self.app, traceback.format_exc() )
            return {}

        #Playlist data
        playlistdata = {}
        try:    playlistdata['title'] = rss.title.string
        except: pass
        try:    daplaylistdatata['description'] = rss.subtitle.string
        except: pass
        try:    playlistdata['logo'] = rss.image.string
        except: pass
        try:    playlistdata['logo'] = rss.logo.string
        except: pass

        #Items data
        data_items = []
        rss_items = rss.findAll("entry")

        for rss_item in rss_items:
            data_item = {}
            try:    data_item['title'] = rss_item.title.string
            except: pass
            try:    data_item['description'] = rss_item.find('summary').string
            except: pass
            try:    data_item['thumb'] = rss_item.find('link', {'type':'image'})['href']
            except: pass
            try:    data_item['URL'] = rss_item.find('link', {'rel':'enclosure'})['href']
            except: pass
            try:    type = rss_item.find('link', {'rel':'enclosure'})['type']
            except: type = False

            if type:
                data_item['type'] = False
                if 'audio' in type: data_item['type'] = 'audio'
                elif 'video' in type: data_item['type'] = 'video'
                elif 'image' in type: data_item['type'] = 'image'
                elif 'application' in type: data_item['type'] = 'download'
            else:
                data_item['type'] = 'html'
                #playlistdata['view'] =  'detail'
            if data_item['URL']:
                data_items.append(data_item)

        playlistdata['items'] = data_items
        return playlistdata

    ### Fetch flickr playlist type  - type=flickr
    def _FLICKR(self, item):
        if 'rss://' in item.path:
            item.path = item.path.replace('rss:', 'http:')
        rawdata = urlopen(self.app, item.path)
        try: rss = BeautifulStoneSoup(rawdata['content'], convertEntities="xml", smartQuotesTo="xml")
        except:
            Log(self.app, traceback.format_exc() )
            return {}

        #Playlist data
        playlistdata = {}
        try:    playlistdata['title'] = rss.channel.title.string
        except: pass
        try:    daplaylistdatata['description'] = rss.channel.description.string
        except: pass
        try:    playlistdata['logo'] = rss.channel.image.string
        except: pass

        #Items data
        data_items = []
        rss_items = rss.findAll("item")

        for rss_item in rss_items:
            data_item = {}
            try:    data_item['name'] = rss_item.find('title').string
            except: pass
            try:    info = rss_item.find('description').string
            except: pass
            try:
                info_item = BeautifulSoup(info, convertEntities="html", smartQuotesTo="xml")
                data_item['URL'] = info_item.a.img['src']
                data_item['description'] =  info_item.a.img['title']
            except: data_item['URL'] = False
            data_item['type'] = 'image'
            if data_item['URL']:
                data_items.append(data_item)

        playlistdata['items'] = data_items
        return playlistdata

    ### Fetch youtube playlist type  - type=youtube
    def _YOUTUBE(self, item):
        if not "http://gdata.youtube.com" in item.path: return {}

        rawdata = urlopen(self.app, item.path)
        try: rss = BeautifulStoneSoup(rawdata['content'], convertEntities="xml", smartQuotesTo="xml")
        except:
            Log(self.app, traceback.format_exc() )
            return {}

        #Playlist data
        playlistdata = {}
        try:    playlistdata['title'] = rss.title.string
        except: pass
        try:    daplaylistdatata['description'] = rss.subtitle.string
        except: pass
        try:    playlistdata['logo'] = rss.image.string
        except: pass
        try:    playlistdata['logo'] = rss.logo.string
        except: pass

        #Items data
        data_items = []
        rss_items = rss.findAll("entry")

        for rss_item in rss_items:
            data_item = {}
            try:    data_item['title'] = rss_item.find('title').string
            except: pass
            try:    data_item['description'] = rss_item.find('content').string
            except: pass
            try:    data_item['thumb'] = rss_item.find('media:thumbnail', {'height' : '240'})['url']
            except: pass
            try:    data_item['URL'] = rss_item.find('media:content', {'isdefault' : 'true'})['url']  + '&fmt=22'
            except: data_item['URL'] = False

            if data_item['URL']:
                data_item['type'] = 'video'
                data_items.append(data_item)

        playlistdata['items'] = data_items
        return playlistdata

    ### Fetch shoutcast playlist type  - type=shoutcast
    def _SHOUTCAST(self, item):
        rawdata = urlopen(self.app, item.path)
        try: xml = BeautifulStoneSoup(rawdata['content'], convertEntities="xml", smartQuotesTo="xml")
        except:
            Log(self.app, traceback.format_exc() )
            return {}

        #Playlist data
        playlistdata = {
            'title' : 'Shoutcast - '+ item.name,
            'logo' : '%s/icons/shoutcast.png'  % self.app.mediaDir
            }

        #Items data
        data_items = []
        xml_items = xml.findAll('station')

        for xml_item in xml_items:
            data_item = {}
            try:    data_item['name'] = xml_item['name']
            except: pass
            try:    data_item['name'] = "".join([data_item['name'], ' (', xml_item['br'], 'kbps) '])
            except: pass
            try:    ddata_item['name'] = "".join([data_item['name'], '- Now Playing: ', xml_item['ct']])
            except: pass
            try:
                id = xml_item['id']
                data_item['URL'] = "".join(["http://yp.shoutcast.com/sbin/tunein-station.pls?id=", id, "&file=filename.pls"])
            except: data_item['URL'] = False

            if data_item['URL']:
                data_item['type'] = 'audio'
                data_items.append(data_item)

        playlistdata['items'] = data_items
        return playlistdata

    ### Fetch apple playlist type  - type=apple
    def _APPLE(self, item):
        rawdata = urlopen(self.app, item.path)
        try: xml = BeautifulStoneSoup(rawdata['content'], convertEntities="xml", smartQuotesTo="xml")
        except:
            Log(self.app, traceback.format_exc() )
            return {}

        #Playlist data
        playlistdata = {
            'title' : 'Apple Movie Trailers '
            }
        try: playlistdata['title'] = playlistdata['title'] + xml['date']
        except: pass

        #Items data
        data_items = []
        xml_items = xml.findAll('movieinfo')


        for xml_item in xml_items:
            data_item = {'date2':'', 'description':'', 'name':''}
            try:    
                date = xml_item.info.releasedate.string.split('-')
                data_item['description'] = "".join([date[2], '.', date[1], '.', date[0], ' - '])
                data_item['date2'] = date
            except: pass
            try:    data_item['name'] = xml_item.info.title.string
            except: pass
            try:    data_item['thumb'] = xml_item.poster.location.string
            except: pass
            try:    data_item['URL'] = xml_item.preview.large.string
            except: pass
            try:    data_item['date'] = xml_item.info.postdate.string
            except: pass
            try:    data_item['description'] = "".join([data_item['description'], xml_item.info.description.string])
            except: pass

            if data_item['URL']:
                data_item['type'] = 'video'
                data_items.append(data_item)

        data_items = sort_dict(data_items, 'date2', True)
        
        playlistdata['items'] = data_items
        return playlistdata

    ######
    ### Navi download functions
    ######

    ### Get all items in download dir and parse info
    def _DOWNLOADDIR(self, item):
        path = self.app.url_download_location

        if self.app.embedded:
            tmp_path = os.path.join(self.app.tempDir, 'download')
            if os.path.islink(tmp_path):
                os.chmod(tmp_path, stat.S_IWUSR)
                os.remove(tmp_path)
            os.symlink(path, os.path.join(self.app.tempDir, 'download') )
            path = tmp_path

        files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and os.path.splitext(file)[1] == '.plx']
        data = {}
        data['name'] = 'Downloads'
        data['view'] = 'default'
        data['items'] = []

        for file in files:
            data['items'].append( json_loads(path=os.path.join(path, file)) )

        if len(data['items']) < 1:
            data = {}
        return data

    ### Download an item
    def _DOWNLOAD(self, item, path):
        if self.download.active:
            self.app.gui.ShowDialogNotification(self.app.local['97'])
            return

        if self.app.embedded:
            tmp_path = os.path.join(self.app.tempDir, 'download')
            if os.path.islink(tmp_path):
                os.chmod(tmp_path, stat.S_IWUSR)
                os.remove(tmp_path)
            os.symlink(path, os.path.join(self.app.tempDir, 'download') )
            path = tmp_path

        
        if not os.access(path, os.W_OK):
            self.app.gui.ShowDialogNotification(self.app.local['96'])
            return

        filename = slugify(item.name)

        if item.download != '':
            item.playurl = item.download
        elif item.processor != '':
            item = self.app.api._PROCESSOR(item)

        url = item.playurl
        ext = getFileExtension(url)
    
        filepath = os.path.join(path, "".join([filename, ext]))

        #write info
        infodata = item.parseRAW()
        infodata['URL'] = filepath
        infodata['processor'] = ''
        infopath = os.path.join(path, '%s.plx' % filename)

        Log(self.app, "NAVI-X: Init Download thread...")
        Log(self.app, "NAVI-X: Download info - %s, %s" % (filepath, url))
        try:
            self.download.start(url, filepath, infodata, infopath, item.name)
        except:
            Log(self.app, traceback.format_exc() )
        Log(self.app, "NAVI-X: Download Thread started")

    ######
    ### Navi search functions
    ######

    ### Call search dialog (from playlist type 'search')
    def _SEARCH(self, item):
        self.app.gui.HideDialog('dialog-wait')
        query = self.app.gui.ShowDialogKeyboard(item.name, '', False)
        self.app.gui.ShowDialog('dialog-wait')
        if query != '':
            return self.app.search.start(query, url=item.path)
        else:
            return {}
    
    ### Perform multithread search - consumer
    def SEARCH(self, data):
        def producer(q, data):
            for item in data:
                thread = dataGetter(self.app, item)
                thread.start()
                q.put(thread, True)
        
        finished = []
        results = []
        def consumer(q, total_data):
            while len(finished) < total_data:
                thread = q.get(True)
                thread.join()
                try: results.extend(thread.get_result()['items'])
                except: Log(self.app, traceback.format_exc() )
                finished.append('end')
                    
        q = Queue(3)
        prod_thread = threading.Thread(target=producer, args=(q, data))
        cons_thread = threading.Thread(target=consumer, args=(q, len(data)))
        prod_thread.start()
        cons_thread.start()
        prod_thread.join()
        cons_thread.join()
        
        return results

### Thread class to retreive search data - worker
class dataGetter(threading.Thread):
    def __init__(self, app, item):
        self.app = app
        self.url = item['url']
        self.type = item['type']
        self.result = None
        threading.Thread.__init__(self)

    def get_result(self):
        return self.result

    def run(self):
        try:
            item = Navi_ITEM(self.app, {'type':self.type, 'path':self.url, 'maxline':100})
            self.result = self.app.api.loads(item, cache=0)
        except:
            Log(self.app, traceback.format_exc() )

