
# -*- coding: UTF-8 -*-

import os, sys, re, xbmc, xbmcgui, string, time, urllib, urllib2, logging, time, shutil
from BeautifulSoup import BeautifulSoup


import ConfigParser

import SubtitleDatabase
import version

log = logging.getLogger(__name__)

def rematch(pattern, inp):
    matcher = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    matches = matcher.match(inp)
    if matches:
        yield matches


class Undertexter(SubtitleDatabase.SubtitleDB):
    main_url = "http://www.undertexter.se/"
    eng_download_url = "http://eng.undertexter.se/"
    debug_pretext = ""

    #====================================================================================================================
    # Functions
    #====================================================================================================================

    def __init__(self, config, cache_folder_path):
        super(Undertexter, self).__init__(None)
        self.headers = {'User-Agent' : 'BoxeeSubs/1.0'}


    def process(self, filepath, langs):
            ''' main method to call on the plugin, pass the filename and the wished
            languages and it will query the subtitles source '''
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
                log.exception("Error raised by plugin")
                return []


    def query(self, token, langs=None):
        ''' makes a query and returns info (link, lang) about found subtitles'''

        guessedData = self.guessFileData(token)
        if langs and not set(langs).intersection((['en', 'sv'])): # lang is given but does not include nl or en
            return []

        if not langs :
            availableLangs = ['sv', 'en']
        else :
            availableLangs = list(set(langs).intersection((['en', 'sv'])))
        log.debug("possible langs : %s " % availableLangs)
        sublinks = []

        if guessedData['type'] == 'tvshow':
	    if(int(guessedData['season']) < 10):
		guessedData['season'] = "0"+str(guessedData['season'])
	    if(int(guessedData['episode']) < 10):
                guessedData['episode'] = "0"+str(guessedData['episode'])
            searchstring = "%s S%sE%s" % (guessedData['name'], guessedData['season'], guessedData['episode'])
	else:
	    searchstring = guessedData['name']
        for lang in availableLangs :
            if(lang == "sv"):
                url = self.main_url + "?p=soek&add=arkiv&submit=S%F6k&select2=&select3=&select=&str=" + urllib.quote_plus(searchstring)
            else:
                url = self.main_url + "?group1=on&p=eng_search&add=arkiv&submit=S%F6k&select2=&select3=&select=&str=" + urllib.quote_plus(searchstring)
            req = urllib2.Request(url, headers = self.headers )
            page = urllib2.urlopen(req)
            content = page.read()
            page.close()

	    soup = BeautifulSoup(content)
	    for subs in soup("table", {"width" : "460", "cellpadding" : "0", "cellspacing" : "0"}):
		for tr in subs("tr"):
			links = tr.findAll("a")
			result = {}
			id = 0
			if(len(links) > 0):
				for m in rematch("http://www.undertexter.se/laddatext.php\?id=(.*)", links[0]['href']):
					id = m.group(1)
				for m in rematch("http://eng.undertexter.se/subtitle.php\?id=(.*)", links[0]['href']):
                        		id = m.group(1)
				if(int(id) > 0):
					if(lang == "sv"):
						link = "http://www.undertexter.se/laddatext.php?id=" + id
					else:
						link = "http://eng.undertexter.se/subtitle.php?id=" + id
					
					release = ""
					for a in tr.findAll('td')[0].childGenerator(): 
						release = str(a).strip()
					
					if(release != ""):
						result["link"] = link
						result["page"] = link			
						result["lang"] = lang
						result["release"] = release
						sublinks.append(result)

        return sublinks

    def downloadFile(self, url, filename):
	req = urllib2.Request(url, headers = self.headers)
        f = urllib2.urlopen(req)
        content = f.read()
        f.close()
	orig_sub_dir = os.path.dirname(os.path.abspath(filename))
	tmp_sub_dir = os.path.dirname(os.path.abspath(filename))
	tmp_sub_dir = tmp_sub_dir+"/dl"
	if os.path.exists(tmp_sub_dir):
		files = os.listdir(tmp_sub_dir)
                for file in files:
			os.remove(os.path.join(tmp_sub_dir, file))		
	else:
		os.mkdir(tmp_sub_dir)
	pass
	if content is not None:
            header = content[:4]
	    print header
            if header == 'Rar!':
                local_tmp_file = filename + ".rar"
                packed = True
            elif header == 'PK':
                local_tmp_file = filename + ".zip"
                packed = True
            else: # never found/downloaded an unpacked subtitles file, but just to be sure ...
                local_tmp_file = filename
                subs_file = local_tmp_file
                packed = False
        try:
	    if os.path.exists(local_tmp_file):
		os.remove(local_tmp_file)
            local_file_handle = open(local_tmp_file, "wb")
            local_file_handle.write(content)
            local_file_handle.close()
        except:
            log( __name__ ,"%s Failed to save subtitles to '%s'" % (self.debug_pretext, local_tmp_file))

	print packed
	print local_tmp_file
        if packed:
        	print tmp_sub_dir
		files = os.listdir(tmp_sub_dir)
		init_filecount = len(files)
		max_mtime = 0
		filecount = init_filecount
		print filecount
		for file in files:
                	if (string.split(file,'.')[-1] in ['srt','sub','txt']):
                		mtime = os.stat(os.path.join(tmp_sub_dir, file)).st_mtime
                		if mtime > max_mtime:
                			max_mtime =  mtime
            	init_max_mtime = max_mtime
		time.sleep(2)
            	xbmc.executebuiltin("XBMC.Extract(" + local_tmp_file + "," + tmp_sub_dir +")")
		time.sleep(1)
            	waittime  = 0
            	while (filecount == init_filecount) and (waittime < 20) and (init_max_mtime == max_mtime): # nothing yet extracted
                	time.sleep(1)  # wait 1 second to let the builtin function 'XBMC.extract' unpack
                	files = os.listdir(tmp_sub_dir)
                	filecount = len(files)
			print filecount
                	# determine if there is a newer file created in tmp_sub_dir (marks that the extraction had completed)
                	for file in files:
                    		if (string.split(file,'.')[-1] in ['srt','sub','txt']):
                        		mtime = os.stat(os.path.join(tmp_sub_dir, file)).st_mtime
                        		if (mtime > max_mtime):
                            			max_mtime =  mtime
                	waittime  = waittime + 1
		print 'out of loopie yayyy'
            	if waittime == 20:
                	print "%s Failed to unpack subtitles in '%s'" % ("", tmp_sub_dir)
           	else:
                	print "%s Unpacked files in '%s'" % ("", tmp_sub_dir)
                	for file in files:
                    		# there could be more subtitle files in tmp_sub_dir, so make sure we get the newly created subtitle file
                    		if (string.split(file, '.')[-1] in ['srt', 'sub', 'txt']) and (os.stat(os.path.join(tmp_sub_dir, file)).st_mtime > init_max_mtime): # unpacked file is a newly created subtitle file
                        		print "%s Unpacked subtitles file '%s'" % ("", file)
                        		subs_file = os.path.join(tmp_sub_dir, file)
			shutil.move(subs_file, filename)
			subs_file = filename
			print subs_file
            	os.remove(local_tmp_file)

        return subs_file
