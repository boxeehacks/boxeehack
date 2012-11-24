import sys
import os
import xbmcgui
import xbmc
import string

__scriptname__ = "OpenSubtitles"
__author__ = "Leo"
__url__ = ""
__svn_url__ = ""
__credits__ = "Leo"
__version__ = "1.0"

BASE_RESOURCE_PATH = os.path.join( os.getcwd().replace( ";", "" ), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
import language
__language__ = language.Language().localized

if ( __name__ == "__main__" ):

	import gui
	window = "main"

	search_string = ""
	path_string = ""
	type = "file"
	if len( sys.argv ) > 1:
		tmp_string = sys.argv[1]
		tmp_string.strip()
		path_string = tmp_string[tmp_string.find( "[PATH]" ) + len( "[PATH]" ):tmp_string.find( "[/PATH]" )]
		if ( tmp_string.find( "[MOVIE]" ) > -1 ):
			search_string = tmp_string[tmp_string.find( "[MOVIE]" ) + len( "[MOVIE]" ):tmp_string.find( "[/MOVIE]" )]
			tmp_list = search_string.split()
			search_string = string.join( tmp_list, '+' )
			type = "movie"
		elif ( tmp_string.find( "[TV]" ) > -1 ):
			search_string = tmp_string[tmp_string.find( "[TV]" ) + len( "[TV]" ):tmp_string.find( "[/TV]" )]			
			tmp_list = search_string.split()
			tmp_string = tmp_list.pop( 0 )
			if ( int( tmp_string ) < 10 ):
				search_string = "S0" + tmp_string
			else:
				search_string = "S" + tmp_string
			tmp_string = tmp_list.pop( 0 )
			if ( int( tmp_string ) < 10 ):
				search_string = search_string + "E0" + tmp_string
			else:
				search_string = search_string + "E" + tmp_string
			search_string = search_string + "+" + string.join( tmp_list, '+' )
			type = "tv"

	ui = gui.GUI( "script-%s-%s.xml" % ( __scriptname__.replace( " ", "_" ), window, ), os.getcwd(), "Boxee")
	ui.set_filepath( path_string )
	ui.set_searchstring( search_string )
	ui.set_type( type )
	ui.doModal()
	del ui
