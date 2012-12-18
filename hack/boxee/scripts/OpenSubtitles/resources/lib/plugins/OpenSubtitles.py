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

import os, struct, xmlrpclib, commands, gzip, traceback, logging
import xbmc
import socket # For timeout purposes

import SubtitleDatabase

log = logging.getLogger(__name__)

OS_LANGS ={ "en": "eng", 
            "fr" : "fre", 
            "hu": "hun", 
            "cs": "cze", 
            "pl" : "pol", 
            "sk" : "slo", 
            "pt" : "por", 
            "pt-br" : "pob", 
            "es" : "spa", 
            "el" : "ell", 
            "ar":"ara",
            'sq':'alb',
            "hy":"arm",
            "ay":"ass",
            "bs":"bos",
            "bg":"bul",
            "ca":"cat",
            "zh":"chi",
            "hr":"hrv",
            "da":"dan",
            "nl":"dut",
            "eo":"epo",
            "et":"est",
            "fi":"fin",
            "gl":"glg",
            "ka":"geo",
            "de":"ger",
            "he":"heb",
            "hi":"hin",
            "is":"ice",
            "id":"ind",
            "it":"ita",
            "ja":"jpn",
            "kk":"kaz",
            "ko":"kor",
            "lv":"lav",
            "lt":"lit",
            "lb":"ltz",
            "mk":"mac",
            "ms":"may",
            "no":"nor",
            "oc":"oci",
            "fa":"per",
            "ro":"rum",
            "ru":"rus",
            "sr":"scc",
            "sl":"slv",
            "sv":"swe",
            "th":"tha",
            "tr":"tur",
            "uk":"ukr",
            "vi":"vie"}

class OpenSubtitles(SubtitleDatabase.SubtitleDB):
    url = "http://www.opensubtitles.org/"
    site_name = "OpenSubtitles"
    
    def __init__(self, config, cache_folder_path):
        super(OpenSubtitles, self).__init__(OS_LANGS)
        self.server_url = 'http://api.opensubtitles.org/xml-rpc'
        self.revertlangs = dict(map(lambda item: (item[1],item[0]), self.langs.items()))

    def process(self, filepath, langs):
        ''' main method to call on the plugin, pass the filename and the wished 
        languages and it will query OpenSubtitles.org '''

	subs = []
        filehash = self.hashFile(filepath)
        # disabled this part because getFileSize gives negative values for large files
        # on BoxeeBox, which makes this useless for larger movies
	fname = self.getFileName(filepath)
        if xbmc.getFileSize(filepath):
            log.debug(filehash)
            size = long(xbmc.getFileSize(filepath))
            fname = self.getFileName(filepath)
            subs += self.query(moviehash=filehash, langs=langs, bytesize=size, filename=fname)
  
        subs += self.query(langs=langs, filename=fname)
	return subs
        
    def createFile(self, subtitle):
        '''pass the URL of the sub and the file it matches, will unzip it
        and return the path to the created file'''
        suburl = subtitle["link"]
        videofilename = subtitle["filename"]
        srtbasefilename = videofilename.rsplit(".", 1)[0]
        
	content = self.downloadContent(suburl)
        f = gzip.open(srtbasefilename+".srt.gz")
        dump = open(srtbasefilename+".srt", "wb")
        dump.write(f.read())
        dump.close()
        f.close()
        os.remove(srtbasefilename+".srt.gz")
        return srtbasefilename+".srt"

    def downloadFile(self, link, path):
	content = self.downloadContent(link)
	dump = open(path+".gz", "wb")
        dump.write(content)
        dump.close()
        f = gzip.open(path+".gz")
        dump = open(path, "wb")
        dump.write(f.read())
        dump.close()
        f.close()
        os.remove(path+".gz")
        return path	

    def query(self, filename, imdbID=None, moviehash=None, bytesize=None, langs=None):
        ''' Makes a query on opensubtitles and returns info about found subtitles.
            Note: if using moviehash, bytesize is required.    '''
        log.debug('query')
        #Prepare the search
        search = {}
        sublinks = []
	gotHash = False
	fileHash = ''
	if(moviehash):
		gotHash = True
		fileHash = moviehash
		
        if moviehash: 
            search['moviehash'] = moviehash
            gotHash = True
        if imdbID: search['imdbid'] = imdbID
        if bytesize: search['moviebytesize'] = str(bytesize)
        if len(search) == 0:
            log.debug("No search term, we'll use the filename")
            # Let's try to guess what to search:
            guessed_data = self.guessFileData(filename)
	    searchstring = guessed_data['name']
	    if guessed_data['type'] == 'tvshow':
	    	if(int(guessed_data['season']) < 10):
                	guessed_data['season'] = "0"+str(guessed_data['season'])
            	if(int(guessed_data['episode']) < 10):
                	guessed_data['episode'] = "0"+str(guessed_data['episode'])
            
		searchstring = "%s S%sE%s" % (guessed_data['name'], guessed_data['season'], guessed_data['episode'])

            search['query'] = searchstring
            log.debug(search['query'])
            
        #Login
        self.server = xmlrpclib.Server(self.server_url)
        socket.setdefaulttimeout(10)
        try:
            log_result = self.server.LogIn("","","eng","periscope")
            log.debug(log_result)
            token = log_result["token"]
        except Exception:
            log.error("Open subtitles could not be contacted for login")
            token = None
            socket.setdefaulttimeout(None)
            return []
        if not token:
            log.error("Open subtitles did not return a token after logging in.")
            return []            
            
        # Search
        self.filename = filename #Used to order the results
        sublinks += self.get_results(token, search, gotHash, fileHash)

        # Logout
        try:
            self.server.LogOut(token)
        except:
            log.error("Open subtitles could not be contacted for logout")
        socket.setdefaulttimeout(None)
        return sublinks
        
    def get_results(self, token, search, gotHash, fileHash):
        log.debug("query: token='%s', search='%s'" % (token, search))
        try:
            if search:
                results = self.server.SearchSubtitles(token, [search])
        except Exception, e:
            log.error("Could not query the server OpenSubtitles")
            log.debug(e)
            return []
        log.debug("Result: %s" %str(results))

        sublinks = []
        if results['data']:
            log.debug(results['data'])
            # OpenSubtitles hash function is not robust ... We'll use the MovieReleaseName to help us select the best candidate
            for r in sorted(results['data'], self.sort_by_moviereleasename):
                # Only added if the MovieReleaseName matches the file
                result = {}
                result["release"] = r['SubFileName']
                result["link"] = r['SubDownloadLink']
                result["page"] = r['SubDownloadLink']
		if(gotHash == True and r['MovieHash'] == fileHash):
			result["hash"] = True
                result["lang"] = self.getLG(r['SubLanguageID'])
                if search.has_key("query") : #We are using the guessed file name, let's remove some results

                    # We're not actually removing, since due to some BoxeeBox issues we're
                    # always searching by filename. And if a user renames their files (which)
                    # works better with Boxee, then these names will probably never match
                    # so we only prioritize the matches, but keep everything else in there as
                    # well...
                    if r["MovieReleaseName"].startswith(self.filename):
                        sublinks.insert(0,result)
                    else:
                        sublinks.append(result)
                        log.debug("Removing %s because release '%s' has not right start %s" %(result["release"], r["MovieReleaseName"], self.filename))
                else :
                    sublinks.append(result)
        return sublinks

    def sort_by_moviereleasename(self, x, y):
        ''' sorts based on the movierelease name tag. More matching, returns 1'''
        #TODO add also support for subtitles release
        xmatch = x['MovieReleaseName'] and (x['MovieReleaseName'].find(self.filename)>-1 or self.filename.find(x['MovieReleaseName'])>-1)
        ymatch = y['MovieReleaseName'] and (y['MovieReleaseName'].find(self.filename)>-1 or self.filename.find(y['MovieReleaseName'])>-1)
        #print "analyzing %s and %s = %s and %s" %(x['MovieReleaseName'], y['MovieReleaseName'], xmatch, ymatch)
        if xmatch and ymatch:
            if x['MovieReleaseName'] == self.filename or x['MovieReleaseName'].startswith(self.filename) :
                return -1
            return 0
        if not xmatch and not ymatch:
            return 0
        if xmatch and not ymatch:
            return -1
        if not xmatch and ymatch:
            return 1
        return 0

