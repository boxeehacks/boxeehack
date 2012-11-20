# -*- coding: utf-8 -*-

#   This file is part of periscope.
#   Copyright (c) 2008-2011 Patrick Dessalle <patrick@dessalle.be>
#
#    periscope is free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    periscope is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with periscope; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import zipfile, os, urllib2, urllib, traceback, logging
import xmlrpclib, struct, socket
from hashlib import md5, sha256

import SubtitleDatabase

class Podnapisi(SubtitleDatabase.SubtitleDB):
    url = "http://www.podnapisi.net/"
    site_name = "Podnapisi"

    def __init__(self, config, cache_folder_path):
        super(Podnapisi, self).__init__({"sl" : "1", "en": "2", "no" : "3", "ko" :"4", "de" : "5", "is" : "6", "cs" : "7", "fr" : "8", "it" : "9", "bs" : "10", "ja" : "11", "ar" : "12", "ro" : "13", "es-ar" : "14", "hu" : "15", "el" : "16", "zh" : "17", "lt" : "19", "et" : "20", "lv" : "21", "he" : "22", "nl" : "23", "da" : "24", "se" : "25", "pl" : "26", "ru" : "27", "es" : "28", "sq" : "29", "tr" : "30", "fi" : "31", "pt": "32", "bg" : "33", "mk" : "35", "sk" : "37", "hr" : "38", "zh" : "40", "hi": "42", "th" : "44", "uk": "46", "sr": "47", "pt-br" : "48", "ga": "49", "be": "50", "vi": "51", "fa": "52", "ca": "53", "id": "54"})
        
        #Note: Podnapisi uses two reference for latin serbian and cyrillic serbian (36 and 47). We'll add the 36 manually as cyrillic seems to be more used
        self.revertlangs["36"] = "sr";
        self.server_url = 'http://ssp.podnapisi.net:8000'



    def process(self, filepath, langs):
        ''' main method to call on the plugin, pass the filename and the wished 
        languages and it will query the subtitles source '''
        if os.path.isfile(filepath):
            filehash = self.hashFile(filepath)
            size = os.path.getsize(filepath)
            fname = self.getFileName(filepath)
            return self.query(moviehash=filehash, langs=langs, bytesize=size, filename=fname)
        else:
            fname = self.getFileName(filepath)
            return self.query(langs=langs, filename=fname)
    
    def query(self, filename, imdbID=None, moviehash=None, bytesize=None, langs=None):
        ''' makes a query on podnapisi and returns info (link, lang) about found subtitles'''
        
        #Login
        self.server = xmlrpclib.Server(self.server_url)
        socket.setdefaulttimeout(1)
        try:
            log_result = self.server.initiate("Periscope")
            logging.debug(log_result)
            token = log_result["session"]
            nonce = log_result["nonce"]
        except Exception, e:
            logging.error("Podnapisi could not be contacted")
            socket.setdefaulttimeout(None)
            return []
        logging.debug("got token %s" %token)
        logging.debug("got nonce %s" %nonce)
        logging.debug("hashes are %s" %[moviehash])
        username = 'getmesubs'
        password = '99D31$$'
        hash = md5()
        hash.update(password)
        password = hash.hexdigest()

        hash = sha256()
        hash.update(password)
        hash.update(nonce)
        password = hash.hexdigest()
        print username
        print password
        self.server.authenticate(token, username, password)
        #self.server.authenticate(token, '', '')
        logging.debug("Authenticated. Starting search")
        results = self.server.search(token, [moviehash])
        print "Results are %s" %results
        subs = []
        for sub in results['results']:
            subs.append(sub)
            print sub
            
        print "Try a download"
        d = self.server.download(token, [173793])
        print d
        self.server.terminate(token)
        return subs
        
