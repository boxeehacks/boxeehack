from default import *
from tools import *
from gui import *

#Module specific Imports
from urllib import quote_plus
from urlparse import urlparse
import random
import base64

######
### LIBRARY
######
### Contains all playlist standard objects and dialog/window actions
######

### Main Navi-X Playlist object
class Navi_PLAYLIST:
    def __init__(self, app, data):
        self.items = []
        self.__view__ = app.options['navi_main_lists']
        #
        self.version = '0'
        self.background = str(app.plx_default_background)
        self.logo = '%s/icons/playlist.png' % app.mediaDir
        self.icon = '%s/icons/playlist.png' % app.mediaDir
        #
        self.name = ''
        self.type = 'plx'
        self.description = ''
        self.path = ''
        self.player = str(app.plx_default_player)
        self.playmode = str(app.plx_default_playmode)
        self.view = str(app.plx_default_view)
        self.sort = 'Default'
        self.id   = str(random.randint(0, 100))
        #
        if isinstance(data, str):
            self.parseSource(app, data)
        else:
            self.parseData(app, data)

    def parseSource(self, app, id):
        self.name = id + ' menu'
        self.view = 'thumbnails'
        self.type = 'sources'
        self.path = id
        sublist = select_sublist(app.sources['scrapers'], tag=id)
        self.items = [self.itemContainer(app, raw_item) for raw_item in sublist]

 
    def parseData(self, app, data):
        raw_items =  False
        if 'items' in data:
            raw_items = data['items']
            del data['items']         
        if 'URL' in data:
            self.path = data['URL']
            del data['URL']
        if 'title' in data:
            self.name = app.regex['item_name'].sub('', data['title'])
            del data['title']
        if 'description' in data:
            self.description = app.regex['item_name'].sub('', data['description']).replace('/description', '')
            del data['description']
        for key in data.keys():
            vars(self)[key] = data[key]

        if raw_items:
            for raw_item in raw_items:
                try: 
                    item = self.itemContainer(app, raw_item)
                    if (item.platform == '' or item.platform == app.platform) and item.type:
                        self.items.append(item)
                except: pass

    def itemContainer(self, app, data):
        return Navi_ITEM(app, data)

    def addItem(self, item):
	self.items.append(item)

    def get(self, n):
	return self.items[n]

    def count(self):
	return len(self.items)

    #Output playlist to gui
    def _list(self, app):
        list   = []
        total  = self.count()
        for i in xrange(total):
            item     = self.get(i)
            totalstr = "".join(['ITEM: ', str(i+1), '-', str(total)])
            data     = item.parseList(playlist=self, total=totalstr, background=self.background, view=self.view)
            list.append(data)
        app.parking[self.id] = self

        listItems = createList(list)
        for id in unique(self.__view__.itervalues()):
            listItems.set(GUI(window=15000, listid=id))
            
        app.playlist_info.set(self, GUI(window=15000, listid=self.__view__[self.view.lower()]))
        app.gui.SetFocus(self.__view__[self.view])


    #Sort playlist, key = name|date
    def _sort(self, app, key, reverse):
        navi_server = False
        if app.url_navi_server in self.path:
            if len(self.path.split('/')) > 5: navi_server = True
        if navi_server and self.count() > 15 and not key == 'rating' or key == 'default':
            args = {'name':'srt=alpha', 'date':'srt=dd'}
            arg = ''
            try:
                arg = '?' + args[key]
                if reverse: arg + 'd'
                data = { 'name':self.name, 'URL': self.path.split('?')[0] + arg, 'type':self.type }
            except:
                if self.type == 'sources': data = self.path
                else:   data = { 'name':self.name, 'URL': self.path, 'type':self.type }
            item = self.itemContainer(app, data)
            data = app.api.loads(item)
            playlist = app.playlist(app, data)
            if len(data) > 0:
                playlist._list(app)
            else:
                app.gui.ShowDialogNotification(app.local['50'])
        else:
            self.items = sort_instance(self.items, key, reverse)
            self._list(app)

        app.playlist_info.set(self, GUI(window=15000, listid=self.__view__[self.view.lower()]))
        Log(app, 'NAVI-X: Sorted playlist - ' + self.path +' - For key - '+key + ' Reverse - ' + str(reverse))

 
### Main Navi-X Item object
class Navi_ITEM:
    def __init__(self, app, data):
        self.type = ''
        self.name = ''
        self.thumb = 'icons/nothumb.png'
        self.icon = ''
        self.rating = ''
        self.description = ''
        self.date = ''

        self.tag = ''
        self.platform = ''
        self.restricted = False
        self.language = []

        self.player  = 'default'
        self.processor = ''
        self.version = ''
        self.path = ''
        self.download = ''
        self.background = ''
        self.playpath = ''
        self.swfplayer = ''
        self.pageurl = ''
        self.subtitle = ''
        self.seek = 0

        self.parseData(app, data)

    def parseData(self, app, data):
        if 'name' in data:
            if 'Sorted ' in data['name']: return False
            self.name = app.regex['item_name'].sub('', data['name'])
            #### New Tagging system disabled for now
            #.replace('$N', '')
            #try:
            #    tags = re.compile('$N\[(.*?)\]').search(data['name']).group(1)
            #    tags = tags.split('|')
            #    for tag in tags:
            #        if tag == 'boxee': self.platform = 'boxee'
            #         elif tag == 'xbmc': self.platform = 'xbmc'
            #        elif tag == 'restricted': self.restricted = True
            #        elif len(tag) == 2: self.language.append(tag.upper())
            #except: pass
            del data['name']
        if 'URL' in data:
            self.path = data['URL']
            del data['URL']
        if 'url' in data:
            self.path = data['url']
            del data['url']
        if 'DLloc' in data:
            self.download = data['DLloc']
            del data['DLloc']
        if 'description' in data:
            self.description = re.sub("(\[.*?\])", '', data['description']).replace('/description', '')
            del data['description']
        if 'rating' in data:
            if data['rating'][:2] != '-1': self.rating = 'rating/rating' + data['rating'][:1] + '.png'
            del data['rating']
        if not 'icon' in data:
            if ':' in data['type']:
                icon, type = data['type'].split(':')
            else:
                icon = data['type']
            self.icon = '%sicons/%s.png' % (app.mediaDir, str(icon))

        for key in data.keys():
            vars(self)[key] = data[key]
        
        if not 'http' in self.thumb[:5]:
            self.thumb = "".join([app.mediaDir, self.thumb])

    def parseList(self, **kwargs):
        list = {
                'label':self.name,
                'label2':self.type,
                'thumb':self.thumb,
                'icon':self.icon,
                'rating':self.rating,
                'date':process_date(self.date),
                'background':kwargs.get('background', ''),
                'description':self.description,
                'view':kwargs.get('view', 'default'),
                'action':kwargs.get('action', 'down'),
                'total':kwargs.get('total', 0),
                'path':kwargs.get('path', self.path),
            }
        if kwargs.get('playlist', False):
            list['playlist.id']    = kwargs['playlist'].id
            list['playlist.thumb'] = kwargs['playlist'].logo
            list['playlist.label'] = kwargs['playlist'].name
            list['playlist.description'] = kwargs['playlist'].description
        return list

    def parseRAW(self):
        return {
                'name':self.name,
                'type':self.type,
                'thumb':self.thumb,
                'date':self.date,
                'description':self.description,
            }
            
    def setVar(self, var, value):
        vars(self)[var] = value

    def _list(self, app):
        content = ['html_youtube', 'html', 'video', 'audio', 'image', 'text', 'list_note']
        if self.type not in content:
            if forceHEX(self.name) in app.playback_blocklist:
                app.gui.HideDialog('dialog-wait')
                response = app.gui.ShowDialogConfirm("Navi-X", app.local['94'], app.local['100'], app.local['101'])
                if response and app.navi_pincode != '':
                    code = app.gui.ShowDialogNumeric(0, app.local['20'], '')
                    if int(code) != app.navi_pincode:
                        app.gui.ShowDialogNotification(app.local['52'])
                        return
                    else:
                        app.playback_blocklist.remove( forceHEX(self.name) )
                        app.save()
                else:
                    return
                app.gui.ShowDialog('dialog-wait')

            if self.type in ['sources', 'downloads', 'search']:
                data = app.api.loads(self, cache=0)
            else:
                data = app.api.loads(self)
            if len(data) < 1:
                app.gui.ShowDialogNotification(app.local['50'])
                return

            playlist = app.playlist(app, data)

            app.gui.PushState()
            if self.type not in ['Video', 'Audio', 'Image', 'search']:
                app.gui.SetVisible(2004, False)
            elif self.type == 'search':
                app.gui.SetVisible(2004, True)
                app.gui.SetLabel(20043, app.local['10'])

            app.gui.ClearLists(unique(app.options['navi_main_lists'].itervalues()))
            playlist._list(app)
            
        elif self.type == 'text' or self.type == 'image':
            app.api.loads(self, cache=0)

        elif self.type == 'list_note':
            pass
        else:
            app.dialog_info.show(self)



#######################################################################################



### Navi search main
class Navi_SEARCH:
    def __init__(self, app):
        self.app = app
        self.gui = GUI

        self.sources = app.sources['search']
        self.dialog_options = SEARCH_DIALOG_OPTIONS(app, self)
        self.dialog_history = SEARCH_DIALOG_HISTORY(self)  

    def start(self, query, url=False):
        self.dialog_history.add(query)
        self.save()
        
        if url:
            data = [{'type':'playlist', 'url':url+quote_plus(query)}]
        else:
            data = self.getSources(query)
        if data:
            results = self.app.api.SEARCH(data)
            if len(results) > 0:
                playlistdata = {}
                playlistdata['name'] = 'Search results'
                playlistdata['view'] = 'search'
                playlistdata['items'] = results
                if url: return playlistdata

                playlist = self.app.playlist(self.app, playlistdata)
                Log(self.app, 'NAVI-X: Search executed with query - ' + query)
                playlist._list(self.app)
            else:
                self.app.gui.ShowDialogNotification(self.app.local['12'])
                self.app.gui.ClearLists([75])

    def getSources(self, query):
        source = self.dialog_options.options['source'][self.dialog_options.focus['source']]

        if source == 'All':
            sources = self.sources
        else:
            sources = select_sublist(self.sources, name=source)

        data = False
        if len(sources) > 0:
            data = [{'type':source['type'], 'url':self.getUrl(source, query)} for source in sources]
        return data

    def getUrl(self, source, query):
        url = source['URL'] + quote_plus(query)
        if source.has_key('extended'):
            if source['extended']:
                options = []
                append = options.append
                phrase = self.dialog_options.options['phrase'][self.dialog_options.focus['phrase']]
                type = self.dialog_options.options['type'][self.dialog_options.focus['type']]
                mode = self.dialog_options.options['mode'][self.dialog_options.focus['mode']]
                adult = self.dialog_options.options['adult'][self.dialog_options.focus['adult']]
                if phrase: append('&phrase=1')
                if type != 'All': append('&type=%s' % type.lower())
                if mode != 'All': append('&mode=%s' % mode.lower())
                if adult: append('&adult=1')
                url = "".join([url, "".join([option for option in options]) ])
        return url

    def save(self):
        self.dialog_options.save()
        self.dialog_history.save()
        self.app.save()

### Control for Navi Search settings dialog
class SEARCH_DIALOG_OPTIONS:
    def __init__(self, app, search):
        self.search = search
        self.app = app
        
        self.options = self.app.options['search']

        try:    self.defaults = {'genre':self.search.app.search_setting_genre, 'source':self.search.app.search_setting_source, 'phrase':self.search.app.search_setting_phrase, 'type':self.search.app.search_setting_type, 'mode':self.search.app.search_setting_mode, 'adult':self.search.app.search_setting_adult}
        except: self.defaults = {'genre':'All', 'source':'All', 'phrase':True, 'type':'All', 'mode':'All', 'adult':False}

        self.focus = {}
        self.id = {"genre":90, "source":91, "phrase":92, "type":93, "mode":94, "adult":95}

        #self.options['genre'] = [genre.lower() for genre in self.options['genre']]
        self.sources = self.search.sources
        for source in  self.sources:
            self.options['source'].append(source['name'])
            self.options['genre'].append( "".join([source['genre'][:1].capitalize(), source['genre'][1:]]) )
        self.options['genre'] = unique(self.options['genre'])

        for option in self.options:
            try:    focus = self.options[option].index(self.defaults[option])
            except: focus = 0
            self.focus[option] = focus

    def next(self, stringid):
        size = len(self.options[stringid]) - 1
        focus = self.focus[stringid]
        if focus < size:
            index = focus + 1
        else: index = 0
        self.options[stringid][index]
        self.focus[stringid] = index
        self.update(stringid)

    def previous(self, stringid):
        size = len(self.options[stringid]) - 1
        focus = self.focus[stringid]
        if 0 < focus <= size:
            index = focus - 1
        else: index = size
        self.options[stringid][index]
        self.focus[stringid] = index
        self.update(stringid)

    def set(self, stringid, index):
        id = self.id[stringid]
        if index == -1: string = ''
        else: string = self.options[stringid][index]
        self.gui.SetButton(id, string)

    def show(self):
        self.search.app.gui.ShowDialog('dialog-search-options')
        self.gui = GUI(window=15150)
        self.update()

    def hide(self):
        self.search.app.gui.HideDialog('dialog-search-options')

    def update(self, stringid=None):
        if stringid == 'genre':
            for option in self.options:
                if option != 'genre':
                    self.focus[option] = 0

            genre = self.options['genre'][self.focus['genre']]
            if genre == 'All':
                self.sources = self.search.sources
            else:
                self.sources = select_sublist(self.search.sources, genre=genre.lower())

            self.options['source'] = ['All']
            for source in self.sources:
                self.options['source'].append(source['name'])

        extended = [source.get('extended', 0) for source in self.sources]
        if not True in extended:
            extended = False

        optiondict = ['phrase','type','mode','adult']
        for option in self.options:
            if option in optiondict and not extended:
                self.set(option, -1)
            else:
                self.set(option, self.focus[option])
        self.save()

    def save(self):
        self.search.app.search_setting_source = self.options['source'][self.focus['source']]
        self.search.app.search_setting_phrase = self.options['phrase'][self.focus['phrase']]
        self.search.app.search_setting_mode = self.options['mode'][self.focus['mode']]
        self.search.app.search_setting_adult = self.options['adult'][self.focus['adult']]
        self.search.app.search_setting_genre = self.options['genre'][self.focus['genre']]


### Control for Navi Search history dialog
class SEARCH_DIALOG_HISTORY:
    def __init__(self, search):
        self.search = search

        try: self.history = self.search.app.search_history
        except: self.history = []

    def add(self, query):
        if len(self.history) > 10: self.history.pop()
        if query in self.history:
            self.history.remove(query)
        self.history.insert(0, query)
        self.save()

    def save(self):
        self.search.app.search_history = self.history

    def show(self):
        self.search.app.gui.ShowDialog('dialog-search-history')
        historylist = [{'label':item} for item in self.history]
        listItems = createList(historylist)
        listItems.set( GUI(window=15140, listid=90) )

    def get(self, n):
	return self.history[n]

    def start(self, focus):
        self.search.start(self.get(focus))

    def hide(self):
        self.search.app.gui.HideDialog('dialog-search-history')



#######################################################################################
#######################################################################################
#######################################################################################


### Control for Navi ITEM information dialog
class Navi_DIALOG_INFO:
    def __init__(self, app):
        self.app = app
        self.action = {
            'play'  : self.play,
            'subtitle'  : self.subtitle,
            'add_favorite':self.add_favorite,
            'del_favorite':self.del_favorite,
            'block':self.block,
            'unblock':self.unblock,
            'download':self.download,
            'none':self.none,
            'rate':self.rate
            }
            
    def none(self):
        self.app.gui.ShowDialogNotification(self.app.local['53'])

    def show(self, item):
        self.item = item
        self.app.gui.ShowDialog('dialog-info')
        self.refresh()

    def refresh(self):
        name = checkUTF8(self.item.name)
        thumb = checkUTF8(self.item.thumb)
        description = 'Source: [I]%s[/I] \n' %  urlparse(self.item.path)[1]
        description += checkUTF8(self.item.description)
        tags = checkStreamTags(self.app, self.item)
        self.list = []

        #Set view / play
        if self.item.type in ['html', 'image']:
            self.list.append( {'label':self.app.local['40'], 'action':'play', 'item.name':name, 'item.thumb':thumb, 'item.description':description} )
        else:
            self.list.append( {'label':self.app.local['30'], 'action':'play', 'item.name':name, 'item.thumb':thumb, 'item.description':description} )

        #Check if login and
        if self.app.api.is_user_logged_in():

            #Check if item is in favorite list
            if self.item.name in self.app.api.favorite_list:
                self.list.append( {'label':self.app.local['31'], 'action':'del_favorite', 'item.name':name, 'item.thumb':thumb, 'item.description':description})
            else:
                self.list.append( {'label':self.app.local['32'], 'action':'add_favorite', 'item.name':name, 'item.thumb':thumb, 'item.description':description})

            #Add rate option
            self.list.append( {'label':self.app.local['33'], 'action':'rate', 'item.name':name, 'item.thumb':thumb, 'item.description':description})

        history = [dict_history.keys()[0] for dict_history in self.app.playback_history]

        #Check if item is in blocklist
        if forceHEX(self.item.name) in self.app.playback_blocklist:
            self.list.pop(0)
            self.list.insert(0 , {'label':self.app.local['34'], 'action':'none', 'item.name':name, 'item.thumb':thumb, 'item.description':description} )
            self.list.insert(3 , {'label':self.app.local['35'], 'action':'unblock', 'item.name':name, 'item.thumb':thumb, 'item.description':description} )
        else:
            if self.item.type in ['video']:
                self.list.append( {'label':self.app.local['36'], 'action':'subtitle', 'item.name':name, 'item.thumb':thumb, 'item.description':description} )
            self.list.append( {'label':self.app.local['37'], 'action':'block', 'item.name':name, 'item.thumb':thumb, 'item.description':description} )

            #Check if item has been played before
            if self.item.name in history and self.app.bookmark:
                index = history.index(self.item.name)
                resume = self.app.playback_history[index].values()[0]
                self.list.insert(1 , {'label':'%s %s' % (self.app.local['38'], GetInHMS(resume)) , 'action':'play', 'item.name':name, 'item.thumb':thumb, 'item.description':description} )
                self.item.seek = resume

            #Add download option
            if self.item.type in ['video'] and self.app.url_download_location != 'not set':
                self.list.append( {'label':self.app.local['39'], 'action':'download', 'item.name':name, 'item.thumb':thumb, 'item.description':description} )

        for i in self.list:
            for t in tags:
                i[t] = 'True'
        listItems = createList(self.list)
        listItems.set(GUI(window=15120, listid=90))

    def hide(self):
        self.app.gui.HideDialog('dialog-info')

    def _exec(self, selected):
        self.app.gui.ShowDialog('dialog-wait')
        id = self.list[selected]['action']
        self.action[id]()
        self.app.gui.HideDialog('dialog-wait')

    def play(self):
        self.app.api.loads(self.item)

    def rate(self):
        self.id = 'rate'
        list = [{'thumb': 'rating/rating%s.png' % item, 'id':self.id, 'obj':'dialog_info'} for item in xrange(6) ]

        self.app.gui.ShowDialog('dialog-options')
        listItems = createList(list)
        listItems.set(GUI(window=self.app.gui.windows['dialog-options'], listid=90))

    def save(self, selected):
        self.app.gui.HideDialog('dialog-options')
        if self.id == 'rate':
            self.app.api.rate_item(self.item, selected)

    def subtitle(self):
        self.app.dialog_subtitle.show(self.item)

    def add_favorite(self):
        self.app.gui.HideDialog('dialog-wait')
        self.app.api.saveFavorite(self.item)
        self.app.gui.ShowDialog('dialog-wait')
        self.refresh()

    def del_favorite(self):
        self.app.gui.HideDialog('dialog-wait')
        self.app.api.delFavorite(self.item)
        self.app.gui.ShowDialog('dialog-wait')
        self.refresh()

    def block(self):
        name = forceHEX(self.item.name)
        if not name in self.app.playback_blocklist:
            self.app.playback_blocklist.append( name)
            self.app.save()
        self.refresh()

    def unblock(self):
        if not self.app.navi_pincode == 0:
            self.app.gui.HideDialog('dialog-wait')
            code = self.app.gui.ShowDialogNumeric(0, self.app.local['20'], '')
            self.app.gui.ShowDialog('dialog-wait')
            if int(code) == self.app.navi_pincode:
                self._unblock()
            else:
                self.app.gui.ShowDialogNotification(self.app.local['52'])
        else:
            self._unblock()

    def _unblock(self):
        name = forceHEX(self.item.name)
        if name in self.app.playback_blocklist:
            self.app.playback_blocklist.remove( name )
            self.app.save()
        self.refresh()

    def download(self):
        self.app.gui.HideDialog('dialog-info')
        self.app.api._DOWNLOAD(self.item, self.app.url_download_location)
        self.app.gui.HideDialog('dialog-wait')


#######################################################################################
#######################################################################################
#######################################################################################


### Control for Navi PLAYLIST information - right menu
class Navi_PLAYLIST_INFO:
    def __init__(self, app):
        self.app = app
        self.selected = 0
        self.menu = GUI(window=self.app.gui.windows['main'], listid=30003)
        self.options = self.app.options['playlist']
        
        self.action = {'add_favorite':self.add_favorite, 'del_favorite':self.del_favorite, 'rate':self.rate, 'block':self.block}

    def set(self, playlist, gui):
        self.gui = gui
        self.playlist = playlist
        self.refresh()

    def refresh(self):
        self.list = [
            {'label':'[B]%s:[/B] %s' % (self.app.local['40'], self.playlist.view), 'action':'view'},
            {'label':'[B]%s:[/B]  %s' % (self.app.local['41'], self.playlist.sort), 'action':'sort'},
        ]

        #Add options if user is logged in
        if self.app.api.is_user_logged_in():
            if self.playlist.name not in  ['Favorite ', 'Search results', 'Downloads', ''] and not ' menu' in self.playlist.name:
                if self.playlist.name in self.app.api.favorite_list:
                    self.list.append( {'label':'[B]%s[/B] ' % self.app.local['42'], 'action':'del_favorite'} )
                else:
                    self.list.append( {'label':'[B]%s[/B] ' % self.app.local['43'], 'action':'add_favorite'} )

                self.list.append( {'label':'[B]%s[/B] ' % self.app.local['44'], 'action':'rate'} )

        if self.playlist.name not in  ['Favorite ', 'Search results'] and not ' menu' in self.playlist.name:
            self.list.append( {'label':'[B]%s[/B] ' % self.app.local['45'], 'action':'block'} )

        listItems = createList(self.list)
        listItems.set(self.menu)

    def show(self, focus):
        self.focus = focus
        self.app.gui.SetFocus(3000)
        self.menu.list.SetFocusedItem(self.selected)

    def hide(self):
        self.app.gui.FocusMain()
        self.gui.list.SetFocusedItem(self.focus)

    def _exec(self, selected):
        self.id = self.list[selected]['action']
        if self.id in ['view', 'sort']:
            data = self.options[self.id]
            list = [{'label': item, 'id':self.id, 'obj':'playlist_info'} for item in data ]

            self.app.gui.ShowDialog('dialog-options')
            listItems = createList(list)
            listItems.set(GUI(window=self.app.gui.windows['dialog-options'], listid=100))
        else:
            self.action[self.id]()
            self.menu.list.SetFocusedItem(selected)

    def save(self, selected):
        self.app.gui.HideDialog('dialog-options')
        try: options = str(self.options[self.id][selected])
        except: pass
        if self.id == 'sort':
            if options == 'default':
                key = 'default'
                reverse = False
            elif options == 'newest':
                key = 'date'
                reverse = True
            elif options == 'oldest':
                key = 'date'
                reverse = False
            elif options == 'asc.':
                key = 'name'
                reverse = False
            elif options == 'desc.':
                key = 'name'
                reverse = True
            elif options == 'rating':
                key = 'rating'
                reverse = True
            self.playlist.sort = options
            self.playlist._sort(self.app, key, reverse)
        elif self.id == 'view':
            self.playlist.view = options
            self.playlist._list(self.app)
        elif self.id == 'rate':
            self.app.api.rate_item(self.playlist, selected)
            
    def rate(self):
        self.id = 'rate'
        list = [{'thumb': 'rating/rating%s.png' % item, 'id':self.id, 'obj':'playlist_info'} for item in xrange(6) ]

        self.app.gui.ShowDialog('dialog-options')
        listItems = createList(list)
        listItems.set(GUI(window=self.app.gui.windows['dialog-options'], listid=100))

    def add_favorite(self):
        self.app.api.saveFavorite(self.playlist)
        self.refresh()

    def del_favorite(self):
        self.app.api.delFavorite(self.playlist)
        self.refresh()

    def block(self):
        name = forceHEX(self.playlist.name)
        if not name in self.app.playback_blocklist:
            self.app.playback_blocklist.append( name )
            self.app.save()
        self.refresh()


#######################################################################################
#######################################################################################
#######################################################################################

### Control for Navi Settings dialog
class Navi_SETTINGS:
    def __init__(self, app):
        self.app = app
        self.gui = GUI(window=self.app.gui.windows['dialog-settings'])
        self.focus = 0
        self.id = ''

    def show(self):
        self.app.gui.ShowDialog('dialog-settings')
        try:
            self.refresh()
        except:
            self.app.loadDefaults()
            self.refresh()

    def refresh(self):
        gui = GUI(window=self.app.gui.windows['dialog-settings'], listid=90)
        gui.SetLabel(80, 'Version: %s' % VERSION)
        list = [
                {'label':'[B]%s:[/B]' % self.app.local['60'], 'action':'main', 'active':IsEqual(0, self.focus)},
                {'label':'[B]%s:[/B]' % self.app.local['61'], 'action':'playback', 'active':IsEqual(1, self.focus)},
                {'label':'[B]%s:[/B]' % self.app.local['62'], 'action':'playlist', 'active':IsEqual(2, self.focus)},
                {'label':'[B]%s:[/B]' % self.app.local['63'], 'action':'advanced', 'active':IsEqual(3, self.focus)}
        ]
        listItems = createList(list)
        listItems.set(gui)
        self.sub()


    def sub(self):
        if self.app.api.is_user_logged_in():
            login = self.app.local['1']
        else:
            login = self.app.local['2']

        self.sublist = [
            #main
            [
                {'label':'%s: %s' % (self.app.local['70'], login), 'action':'login'},
                {'label':'%s: %s' % (self.app.local['71'], self.app.language), 'action':'language'},
                {'label':self.app.local['72'] , 'action':'navi_pincode'},
                {'label':self.app.local['73'], 'action':'reset_cache'},
                {'label':self.app.local['74'], 'action':'defaults'}
            ],
            #playback
            [
                {'label':'%s: %s' % (self.app.local['87'], self.app.bookmark), 'action':'bookmark'},
                {'label':'[COLOR FF222222][I]%s[/I][/COLOR]' % self.app.local['75'], 'action':'none'},
                {'label':'%s 1: %s' % (self.app.local['71'], self.app.playback_sub_lang_1), 'action':'playback_sub_lang_1'},
                {'label':'%s 2: %s' % (self.app.local['71'], self.app.playback_sub_lang_2), 'action':'playback_sub_lang_2'},
                {'label':'%s 2: %s' % (self.app.local['71'], self.app.playback_sub_lang_3), 'action':'playback_sub_lang_3'},

            ],
            #playlist
            [
                {'label':'%s: %s' % (self.app.local['77'], self.app.plx_default_background), 'action':'plx_default_background'},
                {'label':'%s: %s' % (self.app.local['78'], self.app.plx_default_view), 'action':'plx_default_view'},
            ],
            #advanced
            [
                {'label':'%s: %s' % (self.app.local['79'], str(self.app.debug)), 'action':'debug'},
                {'label':'%s: %s s' % (self.app.local['80'], self.app.cache_url_time), 'action':'cache_url_time'},
                {'label':'%s: %s lines' % (self.app.local['81'], str(self.app.plx_lines_max)), 'action':'plx_lines_max'},
                {'label':'%s: %s' % (self.app.local['82'], self.app.url_useragent), 'action':'url_useragent'},
                {'label':'%s: %s kbps' % (self.app.local['83'], str(self.app.url_max_bandwidth)), 'action':'url_max_bandwidth'},
                {'label':'%s: %s s' % (self.app.local['84'], self.app.url_open_timeout), 'action':'url_open_timeout'},
            ]
        ]
        #Add download option
        self.sublist[0].insert(2, {'label':'%s: %s' % (self.app.local['85'], self.app.url_download_location), 'action':'url_download_location'})

        #Add player option for xbmc
        if IsXBMC():
            self.sublist[2].append({'label':'%s: %s' % (self.app.local['86'], self.app.plx_default_player), 'action':'plx_default_player'})

        listItems = createList(self.sublist[self.focus])
        listItems.set(GUI(window=self.app.gui.windows['dialog-settings'], listid=91))

    def _exec(self, selected):
        self.focus = selected
        self.refresh()
        self.gui.SetFocus(91)

    def _execsub(self, selected):
        self.id = selected
        id = self.sublist[self.focus][selected]['action']
        if id in ['language','debug','playback_sub_lang_1','playback_sub_lang_2','playback_sub_lang_3','player', 'plx_default_view', 'plx_default_player', 'bookmark']:
            if 'playback_sub_lang' in id:
                id = 'playback_sub_lang'

            data = self.app.options[id]
            list = ({'label': item, 'id':id, 'obj':'settings', 'refresh':True} for item in data )
            
            self.app.gui.ShowDialog('dialog-options')
            listItems = createList(list)
            listItems.set(GUI(window=self.app.gui.windows['dialog-options'], listid=100))
            
        elif id in ['url_useragent']:
            var = self.app.gui.ShowDialogKeyboard('Settings - %s' % id, str(vars(self.app)[id]), False)
            if var != '':
                vars(self.app)[id] = var
                self.app.save()
                Log(self.app, 'NAVI-X: Changed value \'%s\' to \'%s\'' % ( id, str(vars(self.app)[id] ) ) )
                self.refresh()

        elif id in ['cache_url_time', 'plx_lines_max', 'url_max_bandwidth', 'url_open_timeout', 'navi_pincode']:
            var = self.app.gui.ShowDialogNumeric(0, 'Settings - %s' % id, str(vars(self.app)[id]))
            if var != '':
                vars(self.app)[id] = int(var)
                self.app.save()
                Log(self.app, 'NAVI-X: Changed value \'%s\' to \'%s\'' % ( id, str(vars(self.app)[id] ) ) )
                self.refresh()

        elif id in ['plx_default_background', 'url_download_location']:
            if id in ['plx_default_background']:
                var = self.app.gui.ShowDialogBrowse(1, 'Settings - %s' % id, 'pictures', '.jpg|.png', True)

            elif id in ['url_download_location']:
                var = self.app.gui.ShowDialogBrowse(0, 'Settings - %s' % id, 'myprograms')

            if var != '':
                vars(self.app)[id] = var
                self.app.save()
                Log(self.app, 'NAVI-X: Changed value \'%s\' to \'%s\'' % ( id, str(vars(self.app)[id] ) ) )
                self.refresh()
        
        else:
            getattr(self, id)()
            self.refresh()

    def login(self):
        if self.app.api.is_user_logged_in():
            self.app.api.logout()
        else:
            self.app.api.login()

    def defaults(self):
        self.app.loadDefaults()
        self.gui.ShowDialogNotification(self.app.local['54'])
        Log(self.app, 'NAVI-X: Loaded defaults')

    def save(self, selected):
        self.app.gui.HideDialog('dialog-options')
        id = self.sublist[self.focus][self.id]['action']
        if 'playback_sub_lang' in id:
            vars(self.app)[id] = self.app.options['playback_sub_lang'][selected]
        else:
            vars(self.app)[id] = self.app.options[id][selected]

        if id == 'language':
            languages = json_loads(path=os.path.join(self.app.dataDir, 'languages', str(self.app.language)))
            for id, value in languages.items():
                self.app.local[id] = value.encode('utf-8')
            self.app.parseData(8)
            self.app._list()

        self.app.save()
        self.refresh()

    def none(self):
        pass

    def reset_cache(self):
        self.app.storage.empty(persistent = True)
        self.app.storage.empty()
        self.gui.ShowDialogNotification(self.app.local['55'])
        Log(self.app, 'NAVI-X: Cache is reset')
