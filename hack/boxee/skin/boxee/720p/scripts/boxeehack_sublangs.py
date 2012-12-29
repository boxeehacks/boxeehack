import sys
import os
import xbmcgui
import xbmc
import string
import ConfigParser

try: current_dlg_id = xbmcgui.getCurrentWindowDialogId()
except: current_dlg_id = 0
current_win_id = xbmcgui.getCurrentWindowId()

LANGUAGE_LIST = 120

SELECT_ITEM = ( 11, 256, 61453, )
EXIT_SCRIPT = ( 10, 247, 275, 61467, 216, 257, 61448, )
CANCEL_DIALOG = EXIT_SCRIPT + ( 216, 257, 61448, )
SELECT_BUTTON = ( 229, 259, 261, 61453, )
MOVEMENT_UP = ( 166, 270, 61478, )
MOVEMENT_DOWN = ( 167, 271, 61480, )

class GUI( xbmcgui.WindowXMLDialog ):

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

    def __init__( self, *args, **kwargs ):
        pass

    def onInit( self ):
        self.setup()

    def onClick(self, controlID):
        item = self.getControl( LANGUAGE_LIST ).getSelectedItem()
        pos = self.getControl( LANGUAGE_LIST ).getSelectedPosition()
        lang = self.items[pos]
        if(item.getProperty("set") == "true"):
            item.setProperty("set", "false")
            self.removeFromConfig(lang)
        else:
            item.setProperty("set", "true")
            self.addToConfig(lang)

    def addToConfig(self, lang):
        config = ConfigParser.SafeConfigParser({"lang": "All", "plugins" : "BierDopje,OpenSubtitles", "tvplugins" : "BierDopje,OpenSubtitles", "movieplugins" : "OpenSubtitles" })
        if os.path.exists("/data/etc/.subtitles"):
            config.read("/data/etc/.subtitles")
        else:
            self.close();

        langs_config = config.get("DEFAULT", "lang")
        if(langs_config.strip() == "" or langs_config == "All"):
            enabled_langs = []
        else:
            enabled_langs = map(lambda x : x.strip(), langs_config.split(","))

        if(lang not in enabled_langs):
            enabled_langs.append(lang)
        new_value = ",".join(enabled_langs).strip(',')
        if(new_value == ""):
            new_value = "All"
        config.set("DEFAULT", "lang", new_value)
        if os.path.exists("/data/etc/.subtitles"):
            configfile = open("/data/etc/.subtitles", "w")
            config.write(configfile)
            configfile.close()

    def removeFromConfig(self, lang):
        config = ConfigParser.SafeConfigParser({"lang": "All", "plugins" : "BierDopje,OpenSubtitles", "tvplugins" : "BierDopje,OpenSubtitles", "movieplugins" : "OpenSubtitles" })
        if os.path.exists("/data/etc/.subtitles"):
            config.read("/data/etc/.subtitles")
        else:
            self.close();

        langs_config = config.get("DEFAULT", "lang")
        if(langs_config == "".strip() or langs_config == "All"):
            enabled_langs = []
        else:
            enabled_langs = map(lambda x : x.strip(), langs_config.split(","))
        
        if lang in enabled_langs:
            enabled_langs.remove(lang)

        new_value = ",".join(enabled_langs).strip(',')
        if(new_value == ""):
            new_value = "All"
        config.set("DEFAULT", "lang", new_value)

        if os.path.exists("/data/etc/.subtitles"):
            configfile = open("/data/etc/.subtitles", "w")
            config.write(configfile)
            configfile.close()

    def onFocus( self, controlId ):
        self.controlId = controlId
        
    def onAction(self, action):
        if action in CANCEL_DIALOG:
            self.close()

    def setup(self):
        self.controlId = -1
        self.items = []
        config = ConfigParser.SafeConfigParser({"lang": "All", "plugins" : "BierDopje,OpenSubtitles", "tvplugins" : "BierDopje,OpenSubtitles", "movieplugins" : "OpenSubtitles" })

        if os.path.exists("/data/etc/.subtitles"):
            config.read("/data/etc/.subtitles")
        else:
            self.close();
    
        langs_config = config.get("DEFAULT", "lang")
        if(langs_config == "".strip() or langs_config == "All"):
            enabled_langs = []
        else:
            enabled_langs = map(lambda x : x.strip(), langs_config.split(","))
        
        for attr in sorted(self.trans_lang, key=self.trans_lang.get):
            listitem = xbmcgui.ListItem( label=self.trans_lang[attr], label2=attr, iconImage="0.0", thumbnailImage="" )
            if(attr in enabled_langs):
                listitem.setProperty('set', 'true')
            else:
                listitem.setProperty('set', 'false')
            self.items.append(attr)
            self.getControl( LANGUAGE_LIST ).addItem( listitem )
        
        #self.setFocus( self.getControl( LANGUAGE_LIST ) )
        #self.getControl( LANGUAGE_LIST ).setCurrentListPosition(0)

if (__name__ == "__main__"):
    print os.getcwd()
    ui = GUI("boxeehack_sublangs.xml", os.getcwd(), "Boxee")
    ui.doModal()
    del ui
