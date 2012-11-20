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

import os, urllib2, urllib, xml.dom.minidom, logging, traceback
import ConfigParser

try:
    import xdg.BaseDirectory as bd
    is_local = True
except ImportError:
    is_local = False
    
import SubtitleDatabase

SS_LANGUAGES = {"en": "English",
                "sv": "Swedish",
                "da": "Danish",
                "fi":"Finnish",
                "no": "Norwegian",
                "fr" : "French",
                "es" : "Spanish",
                "is" : "Icelandic"}

class SubtitleSource(SubtitleDatabase.SubtitleDB):
    url = "http://www.subtitlesource.org/"
    site_name = "SubtitleSource"

    def __init__(self, config, cache_folder_path):
        super(SubtitleSource, self).__init__(SS_LANGUAGES)
        key = config.get("SubtitleSource", "key") # You need to ask for it
        if not key:
            log.error("No key in the config file for SubtitleSource")
            return
        #http://www.subtitlesource.org/api/KEY/3.0/xmlsearch/Heroes.S03E09.HDTV.XviD-LOL/all/0
        #http://www.subtitlesource.org/api/KEY/3.0/xmlsearch/heroes/swedish/0

        self.host = "http://www.subtitlesource.org/api/%s/3.0/xmlsearch" %key
            
    def process(self, filepath, langs):
        ''' main method to call on the plugin, pass the filename and the wished 
        languages and it will query the subtitles source '''
        if not key:
            log.info("No key in the config file for SubtitleSource : skip")
            return []
        fname = self.getFileName(filepath)
        try:
            subs = self.query(fname, langs)
            if not subs and fname.rfind(".[") > 0:
                # Try to remove the [VTV] or [EZTV] at the end of the file
                teamless_filename = fname[0 : fname.rfind(".[")]
                subs = self.query(teamless_filename, langs)
                return subs
            else:
                return subs
        except Exception, e:
            logging.error("Error raised by plugin %s: %s" %(self.__class__.__name__, e))
            traceback.print_exc()
            return []
    
    def query(self, token, langs=None):
        ''' makes a query on subtitlessource and returns info (link, lang) about found subtitles'''
        logging.debug("local file is  : %s " % token)
        sublinks = []
        
        if not langs: # langs is empty of None
            languages = ["all"]
        else: # parse each lang to generate the equivalent lang
            languages = [SS_LANGUAGES[l] for l in langs if l in SS_LANGUAGES.keys()]
            
        # Get the CD part of this
        metaData = self.guessFileData(token)
        multipart = metaData.get('part', None)
        part = metaData.get('part')
        if not part : # part will return None if not found using the regex
            part = 1
                            
        for lang in languages:
            searchurl = "%s/%s/%s/0" %(self.host, urllib.quote(token), lang)
            logging.debug("dl'ing %s" %searchurl)
            page = urllib2.urlopen(searchurl, timeout=5)
            xmltree = xml.dom.minidom.parse(page)
            subs = xmltree.getElementsByTagName("sub")

            for sub in subs:
                sublang = self.getLG(self.getValue(sub, "language"))
                if langs and not sublang in langs:
                    continue # The language of this sub is not wanted => Skip
                if multipart and not int(self.getValue(sub, 'cd')) > 1:
                    continue # The subtitle is not a multipart
                dllink = "http://www.subtitlesource.org/download/text/%s/%s" %(self.getValue(sub, "id"), part)
                logging.debug("Link added: %s (%s)" %(dllink,sublang))
                result = {}
                result["release"] = self.getValue(sub, "releasename")
                result["link"] = dllink
                result["page"] = dllink
                result["lang"] = sublang
                releaseMetaData = self.guessFileData(result['release'])
                teams = set(metaData['teams'])
                srtTeams = set(releaseMetaData['teams'])
                logging.debug("Analyzing : %s " % result['release'])
                logging.debug("local file has : %s " % metaData['teams'])
                logging.debug("remote sub has  : %s " % releaseMetaData['teams'])
                #logging.debug("%s in %s ? %s - %s" %(releaseMetaData['teams'], metaData['teams'], teams.issubset(srtTeams), srtTeams.issubset(teams)))
                if result['release'].startswith(token) or (releaseMetaData['name'] == metaData['name'] and releaseMetaData['type'] == metaData['type'] and (teams.issubset(srtTeams) or srtTeams.issubset(teams))):
                    sublinks.append(result)
        return sublinks

            
    def createFile(self, subtitle):
        '''pass the URL of the sub and the file it matches, will unzip it
        and return the path to the created file'''
        suburl = subtitle["link"]
        videofilename = subtitle["filename"]
        srtfilename = videofilename.rsplit(".", 1)[0] + '.srt'
        self.downloadFile(suburl, srtfilename)
        return srtfilename

    def getValue(self, sub, tagName):
        for node in sub.childNodes:
            if node.nodeType == node.ELEMENT_NODE and node.tagName == tagName:
                return node.childNodes[0].nodeValue
