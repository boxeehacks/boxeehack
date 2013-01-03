from default import *

from config import *
from api import *
from library import *
from tools import *
from gui import *
from player import *
from nipl import *
from subtitle import *
from download import *

######
### NAVI-X MAIN APP
######
###
### Short explaination of main processing:
###
###             User clicks on item in list
###                         |
###               get playlist from item
###     (playlist object is depickled from listdata)
###                         |
###                   api processing           -> if playable content is true   ->    NIPL Processing     -> Start playback
###                         |
###           if content/playlist source is true
###                         |
###                    if in cache  ->   no   ->   Download online source
###                         |                      (plx, rss, json etc)
###                        yes                               |
###                         |                    Convert to simple dict data
###                    Load from cache               (cacheble as json)
###                         |                                |
###          Load playlist instance from lib        <-
###                         |
###                  Output to gui (playlist object pickled as listdata)
######

class Navi_APP(Navi_VARS):
    def __init__(self):
        Navi_VARS.__init__(self)
        Log(self, 'NAVI-X: Initialising...')
        
        self.gui     = GUI(window = 15000)
        self.storage = storage(self)

        #Initiate navi modules
        self.playlist = Navi_PLAYLIST
        self.player   = Navi_PLAYER(self)
        self.api      = Navi_API(self)
        self.search   = Navi_SEARCH(self)
        self.settings = Navi_SETTINGS(self)
        self.playlist_info = Navi_PLAYLIST_INFO(self)
        
        self.dialog_info = Navi_DIALOG_INFO(self)
        self.dialog_subtitle = Navi_DIALOG_SUBTITLE(self)

        #Set connected/disconnected text in gui
        if self.api.is_user_logged_in():
            self.gui.SetLabel(20011, self.local['1'])
            self.api.getFavorite()
        else:
            self.gui.SetLabel(20011, self.local['2'])

        #Set top menu to gui
        self.parseData(selected = 0)
        self._list()

        #Set main list to gui
        startpage = self.get(0)
        startpage._list(self)

        Log(self, 'NAVI-X: Initialising... Compleet ')
        self.gui.HideDialog('dialog-wait')

    def parseData(self, selected):
        self.items = [
            self.get_favorite(),
            self.playlist(self, 'navix'),
            self.playlist(self, 'movie'),
            self.playlist(self, 'tv'),
            self.playlist(self, 'audio'),
            self.playlist(self, 'other'),
            self.settings,
            self.search
            ]
            
        self.list = [
            {'label':self.local['3'], 'handle':self, 'active':IsEqual(0, selected), 'action':'topmenu'},
            {'label':self.local['13'],'handle':self, 'active':IsEqual(1, selected), 'action':'topmenu'},
            {'label':self.local['4'], 'handle':self, 'active':IsEqual(2, selected), 'action':'topmenu'},
            {'label':self.local['5'], 'handle':self, 'active':IsEqual(3, selected), 'action':'topmenu'},
            {'label':self.local['6'], 'handle':self, 'active':IsEqual(4, selected), 'action':'topmenu'},
            {'label':self.local['7'], 'handle':self, 'active':IsEqual(5, selected), 'action':'topmenu'},
            {'label':self.local['8'], 'handle':self, 'active':'', 'action':'settings'},
            {'label':self.local['9'], 'handle':self, 'active':IsEqual(6, selected), 'action':'search'}
        ]

    def get(self, n):
	return self.items[n]

    def count(self):
	return len(self.items)

    def _list(self):
        listItems = createList(self.list)
        listItems.set(GUI(window=15000, listid=60))

    def get_favorite(self):
        if self.api.is_user_logged_in():
            item = Navi_ITEM(self, {'name':self.local['3'], 'type':'playlist', 'URL':'http://www.navixtreme.com/playlist/%s/favorite.plx' % self.api.favorite_id})
            data = self.api.loads(item, cache=0)
            return self.playlist(self, data)
        else:
            item = Navi_ITEM(self, {'name':self.local['3'], 'type':'playlist', 'URL':'http://www.navixtreme.com/playlist/week.plx', "thumb":"icons/icon_week.png"})
            data = self.api.loads(item)
            return self.playlist(self, data)
    
    #Process boxee actions from gui (skin files)
    def action(self, **kwargs):
        self.gui.ShowDialog('dialog-wait')
        if kwargs.get('selected',-1) != -1:
            gui       = GUI(window=15000, listid=kwargs['listid'])
            listitems = gui.list.GetItems()
            action    = listitems[kwargs['selected']].GetProperty('action')
            action_id = kwargs['selected']

        if kwargs.get('action', None):
            action = kwargs['action']

        #Actions to go down the list
        if action == 'down':
            focus_id    = gui.list.GetFocusedItem()
            listItems   = gui.list.GetItems()
            playlist_id = listItems[focus_id].GetProperty('playlist.id')
            handle      = self.parking[playlist_id]
            obj = handle.get(action_id)
            obj._list(self)

        #Actions related to the top menu
        elif action == 'topmenu':
            gui.ClearStateStack(False)
            self.gui.SetVisible(2004, False)
            self.gui.SetLabel(20043, self.local['10'])
            
            self.parseData(action_id)
            self._list()
            gui.list.SetFocusedItem(action_id)
            gui.ClearLists(self.options['navi_main_lists'].itervalues())

            obj = self.get(action_id)
            obj._list(self)

        #Actions related to the search gui functions
        elif action == 'search':
            gui = GUI(window=15000, listid=kwargs['listid'])
            gui.ClearStateStack(False)
            
            #Execute Search
            if kwargs.get('query',False):
                obj = self.get(7)
                obj.start(kwargs['query'])

            #Save Search option configuration
            elif kwargs.get('search_save',False):
                obj = self.get(7)
                obj.dialog.save()

                gui.ShowDialogNotification(self.local['11'])
                gui.SetFocus(20041)

            #Show search in gui
            else:
                self.parseData(action_id)
                self._list()

                gui.SetVisible(2004, True)
                gui.SetLabel(20043, self.local['10'])
                gui.list.SetFocusedItem(action_id)
                gui.ClearLists(self.options['navi_main_lists'].itervalues())
                gui.SetFocus(2004)
                
        elif action == 'settings':
            self.parseData(action_id)
            self._list()
            self.settings.show()

        elif action == 'options':
            selected = kwargs.get('focus',0)
            gui = GUI(window=self.gui.windows['dialog-options'], listid=kwargs['listid'])
            listitems = gui.list.GetItems()
            obj = listitems[selected].GetProperty('obj')
            refresh = listitems[selected].GetProperty('refresh')
            vars(self)[obj].save(selected)
            if refresh:
                self.settings.refresh()

        self.gui.HideDialog('dialog-wait')
