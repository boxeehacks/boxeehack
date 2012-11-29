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

import zipfile, os, urllib2, urllib, logging, traceback, httplib, re
from BeautifulSoup import BeautifulSoup

import SubtitleDatabase

LANGUAGES = {u"English (US)" : "en",
             u"English (UK)" : "en",
             u"English" : "en",
             u"French" : "fr",
             u"Brazilian" : "pt-br",
             u"Portuguese" : "pt",
             u"Español (Latinoamérica)" : "es",
             u"Español (España)" : "es",
             u"Español" : "es",
             u"Italian" : "it",
             u"Català" : "ca"}

class SubsWiki(SubtitleDatabase.SubtitleDB):
    url = "http://www.subswiki.com"
    site_name = "SubsWiki"

    def __init__(self, config, config_folder_path):
        super(SubsWiki, self).__init__(langs=None,revertlangs=LANGUAGES)
        #http://www.subswiki.com/serie/Dexter/4/1/
        self.host = "http://www.subswiki.com"
        self.release_pattern = re.compile("\nVersion (.+), ([0-9]+).([0-9])+ MBs")
        

    def process(self, filepath, langs):
        ''' main method to call on the plugin, pass the filename and the wished 
        languages and it will query the subtitles source '''
        fname = unicode(self.getFileName(filepath).lower())
        guessedData = self.guessFileData(fname)
        if guessedData['type'] == 'tvshow':
            subs = self.query(guessedData['name'], guessedData['season'], guessedData['episode'], guessedData['teams'], langs)
            return subs
        else:
            return []
    
    def query(self, name, season, episode, teams, langs=None):
        ''' makes a query and returns info (link, lang) about found subtitles'''
        sublinks = []
        name = name.lower().replace(" ", "_")
        searchurl = "%s/serie/%s/%s/%s/" %(self.host, name, season, episode)
        logging.debug("dl'ing %s" %searchurl)
        try:
            page = urllib2.urlopen(searchurl)
            ''' test if no redirect was made '''
            if page.geturl() != searchurl :
                return sublinks
        except urllib2.HTTPError, (inst):
            logging.debug("Error : %s for %s" % (searchurl, inst))
            return sublinks
        
        soup = BeautifulSoup(page)
        for subs in soup("td", {"class":"NewsTitle"}):
            subteams = subs.findNext("b").string.lower()            
            teams = set(teams)
            subteams = self.listTeams([subteams], [".", "_", " ", " y "])
            
            #logging.debug("Team from website: %s" %subteams)
            #logging.debug("Team from file: %s" %teams)
            
            #langs_html = subs.findNext("td", {"class" : "language"})
            #lang = self.getLG(langs_html.string.strip())
            
            nexts = subs.parent.parent.findAll("td", {"class" : "language"})
            for langs_html in nexts:
                lang = self.getLG(langs_html.string.strip())
                #logging.debug("lang: %s" %lang)
                statusTD = langs_html.findNext("td")
                status = statusTD.find("strong").string.strip()
                #logging.debug("status: %s" %status)

                link = statusTD.findNext("td").find("a")["href"]

                if ((status == "Completed" or status == "Completado")) :
                    result = {}
                    result["release"] = "%s.S%.2dE%.2d.%s" %(name.replace("-", ".").title(), int(season), int(episode), '.'.join(subteams))
                    result["lang"] = lang
                    result["link"] = self.host + link
                    result["page"] = searchurl
                    sublinks.append(result)
                
        return sublinks
        
    def listTeams(self, subteams, separators):
        teams = []
        for sep in separators:
            subteams = self.splitTeam(subteams, sep)
        logging.debug(subteams)
        return set(subteams)
    
    def splitTeam(self, subteams, sep):
        teams = []
        for t in subteams:
            teams += t.split(sep)
        return teams

    def createFile(self, subtitle):
        '''pass the URL of the sub and the file it matches, will unzip it
        and return the path to the created file'''
        suburl = subtitle["link"]
        videofilename = subtitle["filename"]
        srtbasefilename = videofilename.rsplit(".", 1)[0]
        srtfilename = srtbasefilename +".srt"
        self.downloadFile(suburl, srtfilename)
        return srtfilename

    def downloadFile(self, url, filename):
        ''' Downloads the given url to the given filename '''
        req = urllib2.Request(url, headers={'Referer' : url, 'User-Agent' : 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3)'})
        
        f = urllib2.urlopen(req)
        dump = open(filename, "wb")
        dump.write(f.read())
        dump.close()
        f.close()
