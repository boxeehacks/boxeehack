from default import *
from gui import *
from tools import *

#Module specific Imports
import socket
import shutil
import unicodedata
import traceback

from subtitles.utilities import *



STATUS_LABEL        = 100
LOADING_IMAGE       = 110
SUBTITLES_LIST      = 120
CANCEL_DIALOG       = ( 9, 10, 216, 247, 257, 275, 61467, 61448, )

SERVICE_DIR         = os.path.join(ROOT, "external", "subtitles")

class Navi_DIALOG_SUBTITLE:
    def __init__( self, app):
        self.app = app
        self.gui = GUI(window=15170)

    def show(self, item):
        self.item = item
        self.gui.ShowDialog('dialog-subtitle')
        self.set_allparam(self.item.name)

    def set_allparam(self, name):
        self.stack          = False
        self.stackSecond    = ""
        self.autoDownload   = False
        self.sub_folder     = self.app.tempDir
        self.list           = []
        self.mediadir       = self.app.mediaDir

        self.year           = ''                                 # Year
        self.season         = ''                                 # Season
        self.episode        = ''                                 # Episode
        self.tvshow         = ''                                 # Show
        self.title          = unicodedata.normalize('NFKD', unicode(unicode(name))).encode('ascii','ignore')# Title

        if self.tvshow == "":
            if str(self.year) == "":
                title, season, episode = regex_tvshow(False, self.title)
                if episode != "":
                    self.season = str(int(season))
                    self.episode = str(int(episode))
                    self.tvshow = title
            else:
                self.title = self.title
        else:
            self.year = ""
            
        self.language_1 = self.app.playback_sub_lang_1       # Full language 1
        self.language_2 = self.app.playback_sub_lang_2       # Full language 2
        self.language_3 = self.app.playback_sub_lang_3       # Full language 3

        self.file_original_path = self.title                  # Movie Path
        self.set_temp     = True
        self.rar          = False                             # rar archive?

        if (len(str(self.year)) < 1 ) :
            self.file_name = self.title.encode('utf-8')
            if (len(self.tvshow) > 0):
                self.file_name = "%s S%.2dE%.2d" % (self.tvshow.encode('utf-8'), int(self.season), int(self.episode) )
        else:
            self.file_name = "%s (%s)" % (self.title.encode('utf-8'), str(self.year),)

        self.tmp_sub_dir = os.path.join( self.sub_folder ,"sub_tmp" )

        if not self.tmp_sub_dir.endswith(':') and not os.path.exists(self.tmp_sub_dir):
            os.makedirs(self.tmp_sub_dir)
        else:
            self.rem_files(self.tmp_sub_dir)

        self.gui.SetVisible( 111, False )                     # check for existing subtitles and set to "True" if found
        self.autoDownload = True




#### ---------------------------- Set Service ----------------------------###

        def_movie_service = 'OpenSubtitles'
        def_tv_service = 'OpenSubtitles'
        service_list = []
        service = ""

        for name in os.listdir(SERVICE_DIR):
            if os.path.isdir(os.path.join(SERVICE_DIR,name)):
                service_list.append( name )
                service = name

        if len(self.tvshow) > 0:
            if service_list.count(def_tv_service) > 0:
                service = def_tv_service
        else:
            if service_list.count(def_movie_service) > 0:
                service = def_movie_service

        if len(service_list) > 0:
            if len(service) < 1:
                self.service = service_list[0]
            else:
                self.service = service

            self.service_list = service_list
            self.next = list(service_list)
            self.controlId = -1
            self.subtitles_list = []

            Log(self.app, "Default Service : [%s]"           % self.service)
            Log(self.app, "Services : [%s]"                  % self.service_list)
            Log(self.app, "Temp?: [%s]"                      % self.set_temp)
            Log(self.app, "Rar?: [%s]"                       % self.rar)
            Log(self.app, "File Path: [%s]"                  % self.file_original_path)
            Log(self.app, "Year: [%s]"                       % str(self.year))
            Log(self.app, "Tv Show Title: [%s]"              % self.tvshow)
            Log(self.app, "Tv Show Season: [%s]"             % self.season)
            Log(self.app, "Tv Show Episode: [%s]"            % self.episode)
            Log(self.app, "Movie/Episode Title: [%s]"        % self.title)
            Log(self.app, "Subtitle Folder: [%s]"            % self.sub_folder)
            Log(self.app, "Languages: [%s] [%s] [%s]"        % (self.language_1, self.language_2, self.language_3,))
            Log(self.app, "Stacked(CD1/CD2)?: [%s]"          % self.stack)

            try:
                self.Search_Subtitles()
            except:
                Log(self.app, traceback.format_exc())
                errno, errstr = sys.exc_info()[:2]
                self.gui.SetLabel( STATUS_LABEL, "Error:" + " " + str(errstr) )
                xbmc.sleep(2000)
                self.hide()
        else:
            self.gui.SetLabel( STATUS_LABEL, self.app.local['95'] )
            xbmc.sleep(2000)
            self.hide()


###-------------------------- Search Subtitles -------------################

    def Search_Subtitles( self ):
        self.subtitles_list = []
        self.gui.ClearLists([SUBTITLES_LIST])
        self.gui.SetTexture( LOADING_IMAGE, os.path.join( SERVICE_DIR, self.service, "logo.png") )

        importstring = 'subtitles.' + self.service + '.service'
        mod = __import__(importstring)
        components = importstring.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        self.Service = mod

        self.gui.SetLabel( STATUS_LABEL, self.app.local['102'] )
        msg = ""
        socket.setdefaulttimeout(float(6))
        try:
            self.subtitles_list, self.session_id, msg = self.Service.search_subtitles( self.file_original_path, self.title, self.tvshow, self.year, self.season, self.episode, self.set_temp, self.rar, self.language_1, self.language_2, self.language_3, self.stack )
        except socket.error:
            errno, errstr = sys.exc_info()[:2]
            if errno == socket.timeout:
                msg = self.app.local['110']
            else:
                msg =    "%s: %s" % ( self.app.local['103'], str(errstr[1]), )
        except:
            errno, errstr = sys.exc_info()[:2]
            msg = "Error: %s" % ( str(errstr), )

        socket.setdefaulttimeout(None)

        self.gui.SetLabel(STATUS_LABEL, '%s %s' % ( self.app.local['111'], "...") )

        if not self.subtitles_list:
            xbmc.sleep(1500)
            self.next = [self.service_list]
            if msg != "":
                self.gui.SetLabel(STATUS_LABEL, msg )
            else:
                self.gui.SetLabel(STATUS_LABEL,  self.app.local['112'] )
                xbmc.sleep(1000)
                self.app.gui.HideDialog('dialog-wait')
		search = self.app.gui.ShowDialogKeyboard('Manual Search - No Results Found', self.title, False)
                self.app.gui.ShowDialog('dialog-wait')
                if search:
                    self.set_allparam(search)
                
            self.gui.SetFocus( SUBTITLES_LIST )
            self.gui.SetFocusedItem( SUBTITLES_LIST, 0 )
        else:
            subscounter = 0
            itemCount = 0
            sub_list = []
            for item in self.subtitles_list:
                item["rating"] = int(item["rating"]) // 2
                listitem = {"label":item["language_name"], "label2":item["filename"], 'icon':item["rating"], 'thumb':item["language_flag"] }
                print listitem
                if item["sync"]:
                    listitem["sync"] = "true"
                else:
                    listitem["sync"] = "false"
                self.list.append(subscounter)
                subscounter = subscounter + 1
                sub_list.append( listitem )
                itemCount += 1

            list = createList(sub_list)
            list.set(GUI(window=15170, listid=SUBTITLES_LIST))

            self.gui.SetLabel( STATUS_LABEL, '%i %s '"' %s '"'' % (len ( self.subtitles_list ), self.app.local['113'], self.file_name,) )
            self.gui.SetFocus( SUBTITLES_LIST )
            self.gui.SetFocusedItem( SUBTITLES_LIST, 0 )

###-------------------------- Download Subtitles    -------------################

    def Download_Subtitles( self, pos, auto = False ):
        self.gui.SetLabel(STATUS_LABEL,  self.app.local['114'] )
        zip_subs = os.path.join( self.tmp_sub_dir, "zipsubs.zip")
        zipped, language, file = self.Service.download_subtitles(self.subtitles_list, pos, zip_subs, self.tmp_sub_dir, self.sub_folder,self.session_id)
        sub_lang = str(toOpenSubtitles_two(language))

        if zipped :
            self.Extract_Subtitles(zip_subs,sub_lang)
        else:
            sub_ext    = os.path.splitext( file )[1]
            sub_name = 'navix'
            file_name = "%s.%s%s" % ( sub_name, sub_lang, sub_ext )
            file_from = file.replace('\\','/')
            file_to = os.path.join(self.sub_folder, file_name).replace('\\','/')
            # Create a files list of from-to tuples so that multiple files may be
            # copied (sub+idx etc')
            files_list = [(file_from,file_to)]
            # If the subtitle's extension sub, check if an idx file exists and if so
            # add it to the list
            if ((sub_ext == ".sub") and (os.path.exists(file[:-3]+"idx"))):
                Log(self.app, "found .sub+.idx pair %s + %s" % (file_from,file_from[:-3]+"idx"))
                files_list.append((file_from[:-3]+"idx",file_to[:-3]+"idx"))
            for cur_file_from, cur_file_to in files_list:
                subtitle_set,file_path    = self.copy_files( cur_file_from, cur_file_to )
            # Choose the last pair in the list, second item (destination file)
            if subtitle_set:
                self.rem_files(self.tmp_sub_dir)
                Log(self.app, files_list[-1][1])
                self.hide(files_list[-1][1])
            else:
                self.SetLabel( STATUS_LABEL,  self.app.local['115'] )
                self.gui.SetFocus( SUBTITLES_LIST )
                self.gui.SetFocusedItem( SUBTITLES_LIST, 0 )

###-------------------------- Extract, Rename & Activate Subtitles    -------------################

    def Extract_Subtitles( self, zip_subs, subtitle_lang ):
        xbmc.executebuiltin('XBMC.Extract("%s","%s")' % (zip_subs,self.tmp_sub_dir,))
        xbmc.sleep(1000)
        files = os.listdir(self.tmp_sub_dir)
        sub_filename = 'navix'
        exts = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass" ]
        if len(files) < 1 :
            self.gui.SetLabel( STATUS_LABEL ).setLabel( self.app.local['115'] )
        else :
            self.gui.SetLabel(STATUS_LABEL, self.app.local['116'])
            subtitle_set = False
            movie_sub = False
            episode = 0
            for zip_entry in files:
                if os.path.splitext( zip_entry )[1] in exts:
                    subtitle_file, file_path = self.create_name(zip_entry,sub_filename,subtitle_lang)
                    if len(self.tvshow) > 0:
                        title, season, episode = regex_tvshow(False, zip_entry)
                        if not episode : episode = -1
                    else:
                        if os.path.splitext( zip_entry )[1] in exts:
                            movie_sub = True
                    if ( movie_sub or len(files) < 2 or int(episode) == int(self.episode) ):
                        if self.stack:
                            try:
                                if (re.split("(?x)(?i)\CD(\d)", zip_entry)[1]) == (re.split("(?x)(?i)\CD(\d)", sub_filename)[1]):
                                    subtitle_file, file_path = self.create_name(zip_entry,sub_filename,subtitle_lang)
                                elif (re.split("(?x)(?i)\CD(\d)", zip_entry)[1]) == (re.split("(?x)(?i)\CD(\d)", self.stackSecond)[1]):
                                    subtitle_file, file_path = self.create_name(zip_entry,self.stackSecond,subtitle_lang)
                                subtitle_set,file_path = self.copy_files( subtitle_file, file_path )
                                if re.split("(?x)(?i)\CD(\d)", zip_entry)[1] == "1":
                                    subToActivate = file_path
                            except:
                                subtitle_set = False
                        else:
                            subtitle_set,subToActivate = self.copy_files( subtitle_file, file_path )

            if not subtitle_set:
                for zip_entry in files:
                    if os.path.splitext( zip_entry )[1] in exts:
                        subtitle_file, file_path = self.create_name(zip_entry,sub_filename,subtitle_lang)
                        subtitle_set,subToActivate    = self.copy_files( subtitle_file, file_path )

        if subtitle_set :
            self.hide(subToActivate)
        else:
            self.SetLabel( STATUS_LABEL,  self.app.local['115'] )
            self.gui.SetFocus( SUBTITLES_LIST )
            self.gui.SetFocusedItem( SUBTITLES_LIST, 0 )

###-------------------------- Create name    -------------################

    def create_name(self,zip_entry,sub_filename,subtitle_lang):
        sub_ext    = os.path.splitext( zip_entry )[1]
        sub_name = os.path.splitext( sub_filename )[0]
        file_name = "%s.%s%s" % ( sub_name, subtitle_lang, sub_ext )
        file_path = os.path.join(self.sub_folder, file_name)
        subtitle_file = os.path.join(self.tmp_sub_dir, zip_entry)
        return subtitle_file, file_path

###-------------------------- Copy files    -------------################

    def copy_files( self, subtitle_file, file_path ):
        subtitle_set = False
        try:
            shutil.copy(subtitle_file, file_path)
            subtitle_set = True
        except :
            import filecmp
            try:
                if filecmp.cmp(subtitle_file, file_path):
                    subtitle_set = True
            except:
                selected = self.gui.ShowDialogConfirm( self.app.local['117'], self.app.local['118'], self.app.local['100'], self.app.local['101'] )
                if selected == 1:
                    file_path = subtitle_file
                    subtitle_set = True

        return subtitle_set, file_path

###-------------------------- Exit script    -------------################


    def hide( self, subtitle=''):
        self.app.dialog_info.item.subtitle = subtitle
        self.app.dialog_info.refresh()
        self.gui.HideDialog('dialog-subtitle')



###-------------------------- Remove temp files    -------------################

    def rem_files( self, directory):
        try:
            for root, dirs, files in os.walk(directory, topdown=False):
                for items in dirs:
                    shutil.rmtree(os.path.join(root, items), ignore_errors=True, onerror=None)
                for name in files:
                    os.remove(os.path.join(root, name))
        except:
            try:
                for root, dirs, files in os.walk(directory, topdown=False):
                    for items in dirs:
                        shutil.rmtree(os.path.join(root, items).decode("utf-8"), ignore_errors=True, onerror=None)
                    for name in files:
                        os.remove(os.path.join(root, name).decode("utf-8"))
            except:
                pass











