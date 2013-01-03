from default import *
from tools import *

import gui

######
### PLAYER
######
### All the playback related processeing
######

class Navi_PLAYER(mc.Player):
    def  __init__(self, app):
        #Init vars
        mc.Player.__init__(self, True)
        self.call = {
            self.EVENT_STOPPED      :   self.onPlayBackStopped,
            self.EVENT_ENDED        :   self.onPlayBackEnded,
            self.EVENT_STARTED      :   self.onPlayBackStarted
            }

        self.app = app
        
        self.plsVideo = mc.PlayList(mc.PlayList.PLAYLIST_MUSIC)
        self.plsAudio = mc.PlayList(mc.PlayList.PLAYLIST_VIDEO)

    #main function to call for playback processing
    def playContent(self, item):
        if item.path == '':         return
        if item.processor != '':
            item = self.app.api._PROCESSOR(item)
        else:
            item.playurl = item.path

        Log(self.app, 'NAVI-X: Playing item \'%s\' - type \'%s\'' % ( item.playurl, item.type ) )

        if item.type == 'html':     self.playHTML(item)
        elif item.type == 'audio':  self._play(item, mc.ListItem.MEDIA_AUDIO_MUSIC)
        else:                       self._play(item, mc.ListItem.MEDIA_VIDEO_CLIP)

    #Handle playback type=html
    def playHTML(self, item):
        badUrl = False
        if not 'flash://' in item.playurl:
            http = mc.Http()
            if not http.Get(item.playurl):
                badUrl = True
                self.app.gui.ShowDialogNotification(app.local['50'])
            if not badUrl:
                self._play(item, mc.ListItem.MEDIA_UNKNOWN, mime="text/html")
        else:
            self._play(item, mc.ListItem.MEDIA_UNKNOWN, mime="text/html")

    #Start plyayback of item
    def _play(self, item, listtype, mime=None):
        if item.playurl == '':
            if getattr(item, 'error', False):
                self.app.gui.ShowDialogOk('Playback Error', str(item.error))
            return

        self.item = item
        data = item.parseList()
        data['path'] = item.playurl

        if item.playpath != '':
            data['SWFPlayer'] = item.swfplayer
            data['PlayPath'] = item.playpath
            data['PageURL'] = item.pageurl
            mime = "video/x-flv"

        if not mime: mime = getMIME(item.playurl)
        if mime: data['SetContentType'] = mime

        listItem = gui.createList([])
        listItem = listItem.create(data, listtype)

        self.app.gui.HideDialog('dialog-info')
        self.Play(listItem)

        if int(item.seek) != 0:
            #while (self.GetLastPlayerEvent() != self.EVENT_STARTED):
            #    xbmc.sleep(1000)
            xbmc.sleep(4000)
            self.SeekTime(item.seek)

        if item.subtitle != '':
            while (self.GetLastPlayerEvent() != self.EVENT_STARTED):
                xbmc.sleep(1000)
            xbmc.Player().setSubtitles(str(item.subtitle))

        if item.type in ['video'] and self.app.bookmark:
            self.eventStart()

    #Event monitor
    def eventStart(self):
        self.last = self.GetLastPlayerEvent()
        self.time = 0.000
        while True:
            event = self.GetLastPlayerEvent()
            if event != self.last:
                if event in self.call.keys():
                    self.last = event
                    self.call[event]()
                    if event in [self.EVENT_ENDED, self.EVENT_STOPPED]:
                        break
            elif event == self.EVENT_STARTED:
                try:	self.time = self.GetTime()
                except:	print 'NAVI-X: Player not ready'
            xbmc.sleep(1000)

    #Event functions to call
    def onPlayBackStopped(self):
        if len(self.app.playback_history) > 10: self.app.playback_history.remove.pop(0)
        [self.app.playback_history.remove(dict_history) for dict_history in self.app.playback_history if dict_history.keys()[0] == self.item.name]
        self.app.playback_history.append( { self.item.name  :  self.time } )
        self.app.save()
        Log(self.app, 'NAVI-X: Saved resume time for:%s' % self.item.name)

    def onPlayBackEnded(self):
        pass

    def onPlayBackStarted(self, **kwargs):
        pass
