
import os,sys
import xbmc, xbmcgui, mc
import subprocess

os.environ["LD_LIBRARY_PATH"]=".:/data/hack/lib:/opt/local/lib:/usr/local/lib:/usr/lib:/lib:/lib/gstreamer-0.10:/opt/local/lib/qt"

def set_watched(command):
	list = mc.GetWindow(10483).GetList(52)
	item = list.GetItem(1)
	series = mc.GetInfoString("Container(52).ListItem.TVShowTitle")
	db_path = xbmc.translatePath('special://profile/Database/')
	itemList = list.GetItems()
	seasons = []
	episodes_count = 0
	for item in itemList:
		season = item.GetSeason()
		if(season != -1):
			seasons.append(season)
			episodes_count = episodes_count + 1

	seasons = dict.fromkeys(seasons)
	seasons = seasons.keys()

	use_season = -1
	season_string = ""
	if(len(seasons) == 1):
		season_string = " Season %s" % (seasons[0])
		use_season = seasons[0]

	dialog = xbmcgui.Dialog()
    	if dialog.yesno("Watched", "Do you want to mark all episodes of %s%s as %s?" % (series, season_string, command)):
        	progress = xbmcgui.DialogProgress()
        	progress.create('Updating episodes', 'Setting %s%s as %s' % (series, season_string, command))

		current_count = 0
		info_count = 0
		for item in itemList:
			episode = item.GetEpisode()
			boxeeid = mc.GetInfoString("Container(52).ListItem("+str(info_count)+").Property(boxeeid)")
			info_count = info_count + 1
			if(episode != -1):
				current_count = current_count+1
				percent = int( ( episodes_count / current_count ) * 100)
				message = "Episode " + str(current_count) + " out of " + str(episodes_count)
				progress.update( percent, "", message, "" )
				if command == "watched":
				    	os.system('echo -e \'.timeout 10000;\\nINSERT INTO watched VALUES(null, "'+item.GetPath()+'", null, 1, 0, -1.0);\' | /data/hack/bin/sqlite3 ' + db_path + 'boxee_user_catalog.db')
		        	elif command == "unwatched":
		            		os.system('echo -e \'.timeout 10000;\\nDELETE FROM watched WHERE strPath = "'+item.GetPath()+'" OR strBoxeeId = "'+boxeeid+'";\' | /data/hack/bin/sqlite3 ' + db_path + 'boxee_user_catalog.db')
				else:
                    			print "Unknown command"
		progress.close()
		mc.ShowDialogNotification('Marked all episodes for %s%s as %s!' % (series, season_string, command))
		xbmc.executebuiltin("XBMC.ReplaceWindow(10483)")

if (__name__ == "__main__"):
    	command = sys.argv[1]
	set_watched(command)
