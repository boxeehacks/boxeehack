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

import os, shutil, urllib2, sys, logging, traceback, zipfile
import xbmc
import struct
import socket # For timeout purposes
import re

log = logging.getLogger(__name__)

USER_AGENT = 'BoxeeSubs/1.0'

class SubtitleDB(object):
    ''' Base (kind of abstract) class that represent a SubtitleDB, usually a website. Should be rewritten using abc module in Python 2.6/3K'''
    def __init__(self, langs, revertlangs = None):
        if langs:
            self.langs = langs
            self.revertlangs = dict(map(lambda item: (item[1],item[0]), self.langs.items()))
        if revertlangs:
            self.revertlangs = revertlangs
            self.langs = dict(map(lambda item: (item[1],item[0]), self.revertlangs.items()))
        self.tvshowRegex = re.compile('(?P<show>.*)S(?P<season>[0-9]{2})E(?P<episode>[0-9]{2}).(?P<teams>.*)', re.IGNORECASE)
        self.tvshowRegex2 = re.compile('(?P<show>.*).(?P<season>[0-9]{1,2})x(?P<episode>[0-9]{1,2}).(?P<teams>.*)', re.IGNORECASE)
        self.movieRegex = re.compile('(?P<movie>.*)[\.|\[|\(| ]{1}(?P<year>(?:(?:19|20)[0-9]{2}))(?P<teams>.*)', re.IGNORECASE)

    def searchInThread(self, queue, filename, langs):
        ''' search subtitles with the given filename for the given languages'''
        try:
            subs = self.process(filename, langs)
            map(lambda item: item.setdefault("plugin", self), subs)
            map(lambda item: item.setdefault("filename", filename), subs)
            log.info("%s writing %s items to queue" % (self.__class__.__name__, len(subs)))
        except:
            log.exception("Error occured")
            subs = []
        queue.put(subs, True) # Each plugin must write as the caller periscopy.py waits for an result on the queue
    
    def process(self, filepath, langs):
        ''' main method to call on the plugin, pass the filename and the wished 
        languages and it will query the subtitles source '''
        fname = self.getFileName(filepath)
        try:
            return self.query(fname, langs)
        except Exception, e:
            log.exception("Error occured")
            return []
        
    def createFile(self, subtitle):
        '''pass the URL of the sub and the file it matches, will unzip it
        and return the path to the created file'''
        suburl = subtitle["link"]
        videofilename = subtitle["filename"]
        srtbasefilename = videofilename.rsplit(".", 1)[0]
        zipfilename = srtbasefilename +".zip"
        self.downloadFile(suburl, zipfilename)
        
        if zipfile.is_zipfile(zipfilename):
            log.debug("Unzipping file " + zipfilename)
            zf = zipfile.ZipFile(zipfilename, "r")
            for el in zf.infolist():
                if el.orig_filename.rsplit(".", 1)[1] in ("srt", "sub", "txt"):
                    outfile = open(srtbasefilename + "." + el.orig_filename.rsplit(".", 1)[1], "wb")
                    outfile.write(zf.read(el.orig_filename))
                    outfile.flush()
                    outfile.close()
                else:
                    log.info("File %s does not seem to be valid " %el.orig_filename)
            # Deleting the zip file
            zf.close()
            os.remove(zipfilename)
            return srtbasefilename + ".srt"
        else:
            log.info("Unexpected file type (not zip)")
            os.remove(zipfilename)
            return None

    def downloadContent(self, url, timeout = None):
        ''' Downloads the given url and returns its contents.'''
        try:
            log.debug("Downloading %s" % url)
            req = urllib2.Request(url, headers={'Referer' : url, 'User-Agent' : USER_AGENT})
            if timeout:
                socket.setdefaulttimeout(timeout)
            f = urllib2.urlopen(req)
            content = f.read()
            f.close()
            return content
        except urllib2.HTTPError, e:
            log.warning("HTTP Error: %s - %s" % (e.code, url))
        except urllib2.URLError, e:
            log.warning("URL Error: %s - %s" % (e.reason, url))

    def downloadFile(self, url, filename):
        ''' Downloads the given url to the given filename '''
        content = self.downloadContent(url)
        dump = open(filename, "wb")
        dump.write(content)
        dump.close()
        log.debug("Download finished to file %s. Size : %s"%(filename,os.path.getsize(filename)))
        
    def getLG(self, language):
        ''' Returns the short (two-character) representation of the long language name'''
        try:
            return self.revertlangs[language]
        except KeyError, e:
            log.warn("Ooops, you found a missing language in the config file of %s: %s. Send a bug report to have it added." %(self.__class__.__name__, language))
        
    def getLanguage(self, lg):
        ''' Returns the long naming of the language on a two character code '''
        try:
            return self.langs[lg]
        except KeyError, e:
            log.warn("Ooops, you found a missing language in the config file of %s: %s. Send a bug report to have it added." %(self.__class__.__name__, lg))
    
    def query(self, token):
        raise TypeError("%s has not implemented method '%s'" %(self.__class__.__name__, sys._getframe().f_code.co_name))
        
    def fileExtension(self, filename):
        ''' Returns the file extension (without the dot)'''
        return os.path.splitext(filename)[1][1:].lower()
        
    def getFileName(self, filepath):
        return os.path.basename(filepath)
                
    def guessFileData(self, filename):
        filename = unicode(self.getFileName(filename).lower())
        matches_tvshow = self.tvshowRegex.match(filename)
        if matches_tvshow: # It looks like a tv show
            (tvshow, season, episode, teams) = matches_tvshow.groups()
            tvshow = tvshow.replace(".", " ").strip()
            teams = teams.split('.')
            return {'type' : 'tvshow', 'name' : tvshow.strip(), 'season' : int(season), 'episode' : int(episode), 'teams' : teams}
        else:
            matches_tvshow = self.tvshowRegex2.match(filename)
            if matches_tvshow:
                (tvshow, season, episode, teams) = matches_tvshow.groups()
                tvshow = tvshow.replace(".", " ").strip()
                teams = teams.split('.')
                return {'type' : 'tvshow', 'name' : tvshow.strip(), 'season' : int(season), 'episode' : int(episode), 'teams' : teams}
            else:
                matches_movie = self.movieRegex.match(filename)
                if matches_movie:
                    (movie, year, teams) = matches_movie.groups()
                    teams = teams.split('.')
                    part = None
                    if "cd1" in teams :
                        teams.remove('cd1')
                        part = 1
                    if "cd2" in teams :
                        teams.remove('cd2')
                        part = 2
                    return {'type' : 'movie', 'name' : movie.strip(), 'year' : year, 'teams' : teams, 'part' : part}
                else:
                    return {'type' : 'unknown', 'name' : filename, 'teams' : [] }

    def hashFile(self, name):
	return xbmc.getFileHash(name)	

    def hashFile2(self, name):
        '''
        Calculates the Hash à-la Media Player Classic as it is the hash used by OpenSubtitles.
        By the way, this is not a very robust hash code.
        ''' 
        longlongformat = 'Q'  # unsigned long long little endian
        bytesize = struct.calcsize(longlongformat)
        format= "<%d%s" % (65536//bytesize, longlongformat)
        
        f = open(name, "rb") 
        filesize = os.fstat(f.fileno()).st_size
        hash = filesize 
        
        if filesize < 65536 * 2:
            log.error('File is too small')
            return "SizeError" 
        
        buffer= f.read(65536)
        longlongs= struct.unpack(format, buffer)
        hash+= sum(longlongs)
        
        f.seek(-65536, os.SEEK_END) # size is always > 131072
        buffer= f.read(65536)
        longlongs= struct.unpack(format, buffer)
        hash+= sum(longlongs)
        hash&= 0xFFFFFFFFFFFFFFFF
        
        f.close() 
        returnedhash =  "%016x" % hash
	log.warn(returnedhash)
        return returnedhash


class InvalidFileException(Exception):
    ''' Exception object to be raised when the file is invalid'''
    def __init__(self, filename, reason):
        self.filename = filename
        self.reason = reason
    def __str__(self):
        return (repr(filename), repr(reason))
