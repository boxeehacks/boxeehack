import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import threading
import socket
import urllib
from Queue import Queue
import plugins
import ConfigParser
import logging
import difflib

try: current_dlg_id = xbmcgui.getCurrentWindowDialogId()
except: current_dlg_id = 0
current_win_id = xbmcgui.getCurrentWindowId()

_ = sys.modules[ "__main__" ].__language__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__version__ = sys.modules[ "__main__" ].__version__

STATUS_LABEL = 100
LOADING_IMAGE = 110
SUBTITLES_LIST = 120

trans_lang = {'aa' : 'Afar',
'ab' : 'Abkhaz',
'ae' : 'Avestan',
'af' : 'Afrikaans',
'ak' : 'Akan',
'am' : 'Amharic',
'an' : 'Aragonese',
'ar' : 'Arabic',
'as' : 'Assamese',
'av' : 'Avaric',
'ay' : 'Aymara',
'az' : 'Azerbaijani',
'ba' : 'Bashkir',
'be' : 'Belarusian',
'bg' : 'Bulgarian',
'bh' : 'Bihari',
'bi' : 'Bislama',
'bm' : 'Bambara',
'bn' : 'Bengali',
'bo' : 'Tibetan',
'br' : 'Breton',
'bs' : 'Bosnian',
'ca' : 'Catalan',
'ce' : 'Chechen',
'ch' : 'Chamorro',
'co' : 'Corsican',
'cr' : 'Cree',
'cs' : 'Czech',
'cu' : 'Old Church Slavonic',
'cv' : 'Chuvash',
'cy' : 'Welsh',
'da' : 'Danish',
'de' : 'German',
'dv' : 'Divehi',
'dz' : 'Dzongkha',
'ee' : 'Ewe',
'el' : 'Greek',
'en' : 'English',
'eo' : 'Esperanto',
'es' : 'Spanish',
'et' : 'Estonian',
'eu' : 'Basque',
'fa' : 'Persian',
'ff' : 'Fula',
'fi' : 'Finnish',
'fj' : 'Fijian',
'fo' : 'Faroese',
'fr' : 'French',
'fy' : 'Western Frisian',
'ga' : 'Irish',
'gd' : 'Scottish Gaelic',
'gl' : 'Galician',
'gn' : 'Guaraní',
'gu' : 'Gujarati',
'gv' : 'Manx',
'ha' : 'Hausa',
'he' : 'Hebrew',
'hi' : 'Hindi',
'ho' : 'Hiri Motu',
'hr' : 'Croatian',
'ht' : 'Haitian',
'hu' : 'Hungarian',
'hy' : 'Armenian',
'hz' : 'Herero',
'ia' : 'Interlingua',
'id' : 'Indonesian',
'ie' : 'Interlingue',
'ig' : 'Igbo',
'ii' : 'Nuosu',
'ik' : 'Inupiaq',
'io' : 'Ido',
'is' : 'Icelandic',
'it' : 'Italian',
'iu' : 'Inuktitut',
'ja' : 'Japanese (ja)',
'jv' : 'Javanese (jv)',
'ka' : 'Georgian',
'kg' : 'Kongo',
'ki' : 'Kikuyu',
'kj' : 'Kwanyama',
'kk' : 'Kazakh',
'kl' : 'Kalaallisut',
'km' : 'Khmer',
'kn' : 'Kannada',
'ko' : 'Korean',
'kr' : 'Kanuri',
'ks' : 'Kashmiri',
'ku' : 'Kurdish',
'kv' : 'Komi',
'kw' : 'Cornish',
'ky' : 'Kirghiz, Kyrgyz',
'la' : 'Latin',
'lb' : 'Luxembourgish',
'lg' : 'Luganda',
'li' : 'Limburgish',
'ln' : 'Lingala',
'lo' : 'Lao',
'lt' : 'Lithuanian',
'lu' : 'Luba-Katanga',
'lv' : 'Latvian',
'mg' : 'Malagasy',
'mh' : 'Marshallese',
'mi' : 'Maori',
'mk' : 'Macedonian',
'ml' : 'Malayalam',
'mn' : 'Mongolian',
'mr' : 'Marathi',
'ms' : 'Malay',
'mt' : 'Maltese',
'my' : 'Burmese',
'na' : 'Nauru',
'nb' : 'Norwegian',
'nd' : 'North Ndebele',
'ne' : 'Nepali',
'ng' : 'Ndonga',
'nl' : 'Dutch',
'nn' : 'Norwegian Nynorsk',
'no' : 'Norwegian',
'nr' : 'South Ndebele',
'nv' : 'Navajo, Navaho',
'ny' : 'Chichewa; Chewa; Nyanja',
'oc' : 'Occitan',
'oj' : 'Ojibwe, Ojibwa',
'om' : 'Oromo',
'or' : 'Oriya',
'os' : 'Ossetian, Ossetic',
'pa' : 'Panjabi, Punjabi',
'pi' : 'Pali',
'pl' : 'Polish',
'ps' : 'Pashto, Pushto',
'pt' : 'Portuguese',
'pb' : 'Brazilian',
'qu' : 'Quechua',
'rm' : 'Romansh',
'rn' : 'Kirundi',
'ro' : 'Romanian',
'ru' : 'Russian',
'rw' : 'Kinyarwanda',
'sa' : 'Sanskrit',
'sc' : 'Sardinian',
'sd' : 'Sindhi',
'se' : 'Northern Sami',
'sg' : 'Sango',
'si' : 'Sinhala, Sinhalese',
'sk' : 'Slovak',
'sl' : 'Slovene',
'sm' : 'Samoan',
'sn' : 'Shona',
'so' : 'Somali',
'sq' : 'Albanian',
'sr' : 'Serbian',
'ss' : 'Swati',
'st' : 'Southern Sotho',
'su' : 'Sundanese',
'sv' : 'Swedish',
'sw' : 'Swahili',
'ta' : 'Tamil',
'te' : 'Telugu',
'tg' : 'Tajik',
'th' : 'Thai',
'ti' : 'Tigrinya',
'tk' : 'Turkmen',
'tl' : 'Tagalog',
'tn' : 'Tswana',
'to' : 'Tonga',
'tr' : 'Turkish',
'ts' : 'Tsonga',
'tt' : 'Tatar',
'tw' : 'Twi',
'ty' : 'Tahitian',
'ug' : 'Uighur',
'uk' : 'Ukrainian',
'ur' : 'Urdu',
'uz' : 'Uzbek',
've' : 'Venda',
'vi' : 'Vietnamese',
'vo' : 'Volapük',
'wa' : 'Walloon',
'wo' : 'Wolof',
'xh' : 'Xhosa',
'yi' : 'Yiddish',
'yo' : 'Yoruba',
'za' : 'Zhuang, Chuang',
'zh' : 'Chinese',
'zu' : 'Zulu' }


SELECT_ITEM = ( 11, 256, 61453, )

EXIT_SCRIPT = ( 10, 247, 275, 61467, 216, 257, 61448, )

CANCEL_DIALOG = EXIT_SCRIPT + ( 216, 257, 61448, )

GET_EXCEPTION = ( 216, 260, 61448, )

SELECT_BUTTON = ( 229, 259, 261, 61453, )

MOVEMENT_UP = ( 166, 270, 61478, )

MOVEMENT_DOWN = ( 167, 271, 61480, )

DEBUG_MODE = 5

# Log status codes
LOG_INFO, LOG_ERROR, LOG_NOTICE, LOG_DEBUG = range( 1, 5 )

def LOG( status, format, *args ):
    if ( DEBUG_MODE >= status ):
        xbmc.output( "%s: %s\n" % ( ( "INFO", "ERROR", "NOTICE", "DEBUG", )[ status - 1 ], format % args, ) )

def sort_inner(inner):
	if("hash" in inner and inner["hash"] == True):
		return 100
	return inner["percent"]

class GUI( xbmcgui.WindowXMLDialog ):
    socket.setdefaulttimeout(10.0) #seconds
	
    def __init__( self, *args, **kwargs ):
        pass

    def set_filepath( self, path ):
        LOG( LOG_INFO, "set_filepath [%s]" , ( path ) )
        self.file_original_path = path
        self.file_path = path[path.find(os.sep):len(path)]

    def set_filehash( self, hash ):
        LOG( LOG_INFO, "set_filehash [%s]" , ( hash ) )
        self.file_hash = hash

    def set_filesize( self, size ):
        LOG( LOG_INFO, "set_filesize [%s]" , ( size ) )
        self.file_size = size

    def set_searchstring( self, search ):
        LOG( LOG_INFO, "set_searchstring [%s]" , ( search ) )
        self.search_string = search
    
    def set_type( self, type ):
	self.file_type = type

    def onInit( self ):
        LOG( LOG_INFO, "onInit" )
        self.setup_all()
        if self.file_path:
            self.connThread = threading.Thread( target=self.connect, args=() )
            self.connThread.start()
        
    def setup_all( self ):
        self.setup_variables()
        
    def setup_variables( self ):
        self.controlId = -1
        self.allow_exception = False
        if xbmc.Player().isPlayingVideo():
            self.set_filepath( xbmc.Player().getPlayingFile() )

    def connect( self ):
	self.setup_all()
        logging.basicConfig()
	self.getControl( LOADING_IMAGE ).setVisible( True )
        self.getControl( STATUS_LABEL ).setLabel( "Searching" )
	sub_filename = os.path.basename(self.file_original_path)
	title = sub_filename[0:sub_filename.rfind(".")]
	self.getControl( 180 ).setLabel("[B][UPPERCASE]$LOCALIZE[293]:[/B] " + title + "[/UPPERCASE]");
	langs = None
	subtitles = []
	q = Queue()
	self.config = ConfigParser.SafeConfigParser({"lang": "All", "plugins" : "BierDopje,OpenSubtitles", "tvplugins" : "BierDopje,OpenSubtitles", "movieplugins" : "OpenSubtitles" })
	basepath = os.path.dirname(__file__)
	self.config.read(basepath + "/config.ini")
		
	config_plugins = self.config.get("DEFAULT", "plugins")
	if(self.file_type == "tv"):
		config_plugins = self.config.get("DEFAULT", "tvplugins")
	elif(self.file_type == "movie"):
		config_plugins = self.config.get("DEFAULT", "movieplugins")

	use_plugins = map(lambda x : x.strip(), config_plugins.split(","))

	config_langs = self.config.get("DEFAULT", "lang") 
	if(config_langs != "All" and config_langs != ""):
		use_langs = map(lambda x : x.strip(), config_langs.split(","))
	else:
		use_langs = None

	for name in use_plugins:
	    filep = self.file_original_path
            try :
                plugin = getattr(plugins, name)(self.config, '/data/hack/cache')
                LOG( LOG_INFO, "Searching on %s ", (name) )
                thread = threading.Thread(target=plugin.searchInThread, args=(q, str(filep), use_langs))
                thread.start()
            except ImportError, (e) :
		LOG( LOG_INFO, "Plugin %s is not a valid plugin name. Skipping it.", ( e) )		

        # Get data from the queue and wait till we have a result
        count = 0
        for name in use_plugins:
            subs = q.get(True)
	    count = count + 1
	    self.getControl( STATUS_LABEL ).setLabel( "Searching " + str(count) + "/" + str(len(use_plugins)) )
            if subs and len(subs) > 0:
                if not use_langs:
                    subtitles += subs
                else:
                    for sub in subs:
			lang_code = sub["lang"]
			if(lang_code == "pt-br"):
                                lang_code = "pb"
                        if lang_code in use_langs:
                            subtitles += [sub]
	
	if(len(subtitles) > 0):
		self.sublist = subtitles
		for item in subtitles:
			sub_filename = os.path.basename( self.file_original_path )
                	sub_filename = sub_filename[0:sub_filename.rfind(".")]
			percent = (round(difflib.SequenceMatcher(None, sub_filename, item["release"]).ratio(), 2) * 100)
			item["percent"] = percent
		subtitles.sort(key=sort_inner,reverse=True)	
		for item in subtitles:
			if(item["lang"] and item["release"]):
				if(item["lang"] == "pt-br"):
					item["lang"] = "pb"
				if(item["lang"] in trans_lang):
					language = trans_lang[item["lang"]]
				else:
					language = item["lang"]
                    		listitem = xbmcgui.ListItem( label=language, label2=item["release"], iconImage="0.0", thumbnailImage="flags/" + item["lang"] + ".png" )
                    		listitem.setProperty( "source", str(item["plugin"].__class__.__name__))
				listitem.setProperty( "release", item["release"])
		        	listitem.setProperty( "equals", str(item["percent"]) + "%")
				if("hash" in item and item["hash"] == True):
        	                	listitem.setProperty( "sync", "true" )
	                	else:
            	        		listitem.setProperty( "sync", "false" )
	
				self.getControl( SUBTITLES_LIST ).addItem( listitem )
							
        self.setFocus( self.getControl( SUBTITLES_LIST ) )
	self.getControl( SUBTITLES_LIST ).selectItem( 0 )
	self.getControl( LOADING_IMAGE ).setVisible( False )
        self.getControl( STATUS_LABEL ).setVisible( False )
        
    def download_subtitles(self, pos):
	if self.sublist:
	    item = self.sublist[pos]
	    ok = xbmcgui.Dialog().yesno( "BoxeeSubs", _( 242 ), ( _( 243 ) % ( item["release"], ) ), "", _( 260 ), _( 259 ) )
            if not ok:
                self.getControl( STATUS_LABEL ).setLabel( _( 645 ) )
                return
            else:
		local_path = xbmc.translatePath("special://home/subtitles")
		dp = xbmcgui.DialogProgress()
		dp.create( __scriptname__, _( 633 ), os.path.basename( self.file_path ) )
		sub_filename = os.path.basename( self.file_path )
		sub_filename = sub_filename[0:sub_filename.rfind(".")] + "." + item["lang"] + ".srt"
		item["plugin"].downloadFile(item["link"], os.path.join( local_path, sub_filename ))
		dp.close()
		xbmc.Player().setSubtitles( os.path.join( local_path, sub_filename ) )
		xbmc.showNotification( 652, '', '' )
		self.getControl( STATUS_LABEL ).setLabel( _( 652 ) )
		
            self.getControl( STATUS_LABEL ).setLabel( _( 649 ) )
            self.exit_script()

    def exit_script( self, restart=False ):
        self.connThread.join()
        self.close()

    def onClick( self, controlId ):
        if ( self.controlId == SUBTITLES_LIST ):
            self.download_subtitles( self.getControl( SUBTITLES_LIST ).getSelectedPosition() )

    def onFocus( self, controlId ):
        self.controlId = controlId

    def onAction( self, action ):
        try:
                if ( action.getButtonCode() in CANCEL_DIALOG ):
                    self.exit_script()
        except:
                self.exit_script()

