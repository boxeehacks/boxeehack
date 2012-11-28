
import os,sys
import xbmc, xbmcgui, mc
import subprocess

os.environ["LD_LIBRARY_PATH"]=".:/data/hack/lib:/opt/local/lib:/usr/local/lib:/usr/lib:/lib:/lib/gstreamer-0.10:/opt/local/lib/qt"

def set_watched():
	list = mc.GetWindow(10483).GetList(52)
	item = list.GetItem(1)
	series = mc.GetInfoString("Container(52).ListItem.TVShowTitle")
	db_path = xbmc.translatePath('special://profile/Database/')
	itemList = list.GetItems()
	seasons = []
	for item in itemList:
		season = item.GetSeason()
		if(season != -1):
			seasons.append(season)

	seasons = dict.fromkeys(seasons)
	seasons = seasons.keys()
	
	use_season = -1
	season_string = ""
	if(len(seasons) == 1):
		season_string = " Season %s" % (seasons[0])
		use_season = seasons[0]

	dialog = xbmcgui.Dialog()
    	if dialog.yesno("Watched", "Do you want to mark all episodes of %s%s as watched?" % (series, season_string)):
		for item in itemList:
			episode = item.GetEpisode()
			if(episode != -1):
				os.system('/data/hack/bin/sqlite3 ' + db_path + 'boxee_user_catalog.db \'INSERT INTO watched VALUES(null, "'+item.GetPath()+'", null, 1, 0, -1.0);\'')
		mc.ShowDialogNotification('Marked all episodes for %s%s as watched!' % (series, season_string))

if (__name__ == "__main__"):
	set_watched()
