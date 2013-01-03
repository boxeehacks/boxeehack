# -*- coding: utf-8 -*- 

import sys
import os
import xmlrpclib
from subtitles.utilities import *
from xml.dom import minidom
import urllib

BASE_URL_XMLRPC = u"http://api.opensubtitles.org/xml-rpc"
BASE_URL_HASH = u"http://www.opensubtitles.org/en/search/sublanguageid-%s/moviebytesize-%s/moviehash-%s/simplexml"
BASE_URL_NAME = u"http://www.opensubtitles.com/en/search/sublanguageid-%s/moviename-%s/simplexml"

def compare_columns(b,a):
        return cmp( b["language_name"], a["language_name"] )  or cmp( a["sync"], b["sync"] ) 

class OSDBServer:

###-------------------------- Merge Subtitles All -------------################


    def mergesubtitles( self ):
        self.subtitles_list = []
        if( len ( self.subtitles_hash_list ) > 0 ):
            for item in self.subtitles_hash_list:
                if item["format"].find( "srt" ) == 0 or item["format"].find( "sub" ) == 0:
                    self.subtitles_list.append( item )


        if( len ( self.subtitles_list ) > 0 ):
            self.subtitles_list = sorted(self.subtitles_list, compare_columns)

###-------------------------- Sort Subtitles  -------------################

    def sortsubtitles(self, subtitle, hashed, url_base):

        filename = movie = lang_name = subtitle_id = lang_id = link = ""
        flag_image = "-.gif"
        
        if subtitle.getElementsByTagName("releasename")[0].firstChild:
            filename = subtitle.getElementsByTagName("releasename")[0].firstChild.data
        if subtitle.getElementsByTagName("format")[0].firstChild:
            format = subtitle.getElementsByTagName("format")[0].firstChild.data
            filename = "%s.%s" % ( filename,format, )
        if subtitle.getElementsByTagName("movie")[0].firstChild:
            movie = subtitle.getElementsByTagName("movie")[0].firstChild.data
        if subtitle.getElementsByTagName("language")[0].firstChild:
            lang_name = subtitle.getElementsByTagName("language")[0].firstChild.data
        if subtitle.getElementsByTagName("idsubtitle")[0].firstChild:
            subtitle_id = subtitle.getElementsByTagName("idsubtitle")[0].firstChild.data
        if subtitle.getElementsByTagName("iso639")[0].firstChild:
            lang_id = subtitle.getElementsByTagName("iso639")[0].firstChild.data
            flag_image = "flags/%s.gif" % (lang_id,)   
        if subtitle.getElementsByTagName("download")[0].firstChild:
            link = subtitle.getElementsByTagName("download")[0].firstChild.data
            link = url_base + link
        if subtitle.getElementsByTagName("subrating")[0].firstChild:
            rating = subtitle.getElementsByTagName("subrating")[0].firstChild.data
        
        self.subtitles_hash_list.append({'filename':filename,'link':link,'language_name':lang_name,'language_id':lang_id,'language_flag':flag_image,'movie':movie,"ID":subtitle_id,"rating":str( int( rating[0] ) ),"format":format,"sync":hashed})
        
        
    def get_results ( self, search_url ):
        socket = urllib.urlopen( search_url )
        print  "Search url [ %s ]" % (search_url,)
        result = socket.read()
        socket.close()
        return result                

###-------------------------- Opensubtitles Search -------------################
        

    def searchsubtitles( self, srch_string , lang1,lang2,lang3,hash_search, _hash = "000000000", size = "000000000"):
        
        self.subtitles_hash_list = []
        self.subtitles_list =[]
        search_url1 = None
        search_url2 = None
        msg = ""                
        
        language = toOpenSubtitlesId(lang1)
        if lang1 != lang2:
            language += "," + toOpenSubtitlesId(lang2)
            search_url1 = BASE_URL_NAME % (toOpenSubtitlesId(lang2),srch_string,)
        if lang3 != lang1 and lang3 != lang2:
            language += "," + toOpenSubtitlesId(lang3)
            search_url2 = BASE_URL_NAME % (toOpenSubtitlesId(lang3),srch_string,)          
        try:
            if hash_search:
              search_url = BASE_URL_HASH % (language,size, _hash,)
              result = self.get_results( search_url )
              test = True
              if result.find('<?xml version=') < 0:
                msg = _( 755 )
              else:
                xmldoc = minidom.parseString(result)
                subtitles_alt = xmldoc.getElementsByTagName("subtitle")
                if subtitles_alt:
                    url_base = xmldoc.childNodes[0].childNodes[1].firstChild.data
                    for subtitle in subtitles_alt:
                       self.sortsubtitles(subtitle, True, url_base)           

            if (not hash_search) or (not self.subtitles_hash_list):        
              search_url = BASE_URL_NAME % (toOpenSubtitlesId(lang1),srch_string,)
              result = self.get_results( search_url )
              if result.find('<?xml version=') < 0:
                  msg = 'Server is overloaded, please try again later'
              else:
                  xmldoc = minidom.parseString(result)
                  subtitles_alt = xmldoc.getElementsByTagName("subtitle")
                    
                  if search_url1 != None :
                      result = self.get_results( search_url1 )
                      if result.find('<?xml version=') < 0:
                          msg = 'Server is overloaded, please try again later'
                      else:
                          xmldoc = minidom.parseString(result)
                          subtitles_alt += xmldoc.getElementsByTagName("subtitle")
                    
                  if search_url2 != None :
                      result = self.get_results( search_url2 )
                      if result.find('<?xml version=') < 0:
                          msg = 'Server is overloaded, please try again later'
                      else:
                          xmldoc = minidom.parseString(result)
                          subtitles_alt += xmldoc.getElementsByTagName("subtitle")    
                    
            if subtitles_alt:
                url_base = xmldoc.childNodes[0].childNodes[1].firstChild.data
                for subtitle in subtitles_alt:
                   self.sortsubtitles(subtitle, False, url_base)
                        
        except:
            pass
        
        self.mergesubtitles()
        return self.subtitles_list, msg
