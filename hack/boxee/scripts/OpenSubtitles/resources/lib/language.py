"""
Language module

Nuka1195
"""

import os
import xbmc
import xml.dom.minidom


class Language:
    """ Language Class: creates a dictionary of localized strings { int: string } """
    def __init__( self ):
        """ initializer """
        # language folder
        base_path = os.path.join( os.getcwd().replace( ";", "" ), "resources", "language" )
        # get the current language
        language = self._get_language( base_path )
        # create strings dictionary
        self._create_localized_dict( base_path, language )
        
    def _get_language( self, base_path ):
        """ returns the current language if a strings.xml file exists else returns english """
        # get the current users language setting
        language = xbmc.getLanguage().lower()
        # if no strings.xml file exists, default to english
        if ( not os.path.isfile( os.path.join( base_path, language, "strings.xml" ) ) ):
            language = "english"
        return language

    def _create_localized_dict( self, base_path, language ):
        """ initializes self.strings and calls _parse_strings_file """
        # localized strings dictionary
        self.strings = {}
        # add localized strings
        self._parse_strings_file( os.path.join( base_path, language, "strings.xml" ) )
        # fill-in missing strings with english strings
        if ( language != "english" ):
            self._parse_strings_file( os.path.join( base_path, "english", "strings.xml" ) )
        
    def _parse_strings_file( self, language_path ):
        """ adds localized strings to self.strings dictionary """
        try:
            # load and parse strings.xml file
            doc = xml.dom.minidom.parse( language_path )
            # make sure this is a valid <strings> xml file
            root = doc.documentElement
            if ( not root or root.tagName != "strings" ): raise
            # parse and resolve each <string id="#"> tag
            strings = root.getElementsByTagName( "string" )
            for string in strings:
                # convert id attribute to an integer
                string_id = int( string.getAttribute( "id" ) )
                # if a valid id add it to self.strings dictionary
                if ( string_id not in self.strings and string.hasChildNodes() ):
                    self.strings[ string_id ] = string.firstChild.nodeValue
        except:
            # print the error message to the log and debug window
            xbmc.output( "ERROR: Language file %s can't be parsed!" % ( language_path, ) )
        # clean-up document object
        try: doc.unlink()
        except: pass

    def localized( self, code ):
        """ returns the localized string if it exists """
        return self.strings.get( code, "Invailid Id %d" % ( code, ) )
