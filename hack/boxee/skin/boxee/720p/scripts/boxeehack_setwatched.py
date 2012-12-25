import time
import os,sys
import xbmc, xbmcgui, mc
import subprocess
import common

os.environ["LD_LIBRARY_PATH"]=".:/data/hack/lib:/opt/local/lib:/usr/local/lib:/usr/lib:/lib:/lib/gstreamer-0.10:/opt/local/lib/qt"

def get_list(listNum, special):
    try:
        if special == True:
            lst = mc.GetWindow(xbmcgui.getCurrentWindowDialogId()).GetList(listNum)
        else:
            lst = mc.GetActiveWindow().GetList(listNum)
    except:
        lst = ""
    return lst
    
def get_jump_to_last_unwatched_value():
    jumpenabled = common.file_get_contents("/data/etc/.jump_to_unwatched_enabled")
    if jumpenabled == "":
        jumpenabled = "0"
    return jumpenabled

def focus_last_unwatched(listNum):
    global fanart_changed
    
    jumpenabled = get_jump_to_last_unwatched_value()
    if jumpenabled == "0":
        return
    
    # sometimes the list control isn't available yet onload
    # so add some checking to make sure
    lst = get_list(listNum, False)
    count = 10
    while lst == "" and count > 0:
        time.sleep(0.1)
        lst = get_list(listNum, False)
        count = count - 1
        
    if lst == "":
        pass
    else:
        time.sleep(0.1)
        items = lst.GetItems()
        
        more = 1
        reverse = 0

        item = items[1]
        if item.GetSeason() == 1 and item.GetEpisode() == 1:
            reverse = 1

        if reverse == 0:
            info_count = 0
            focus = info_count
            for item in items:
                watched = "%s" % mc.GetInfoString("Container(52).ListItem("+str(info_count)+").Property(watched)")
                
                info_count = info_count + 1
                if watched == "0" and info_count > focus and more == 1:
                    focus = info_count
                
                if watched == "1":
                    more = 0
        else:
            info_count = len(items) - 1
            focus = info_count
            for item in items:
                watched = "%s" % mc.GetInfoString("Container(52).ListItem("+str(info_count)+").Property(watched)")
                
                if watched == "0" and info_count < focus and more == 1:
                    focus = info_count
                info_count = info_count - 1
                
                if watched == "1":
                    more = 0
            
        lst.SetFocusedItem(focus)

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
	display_name = series
	season_string = ""
	if(len(seasons) == 1):
		display_name = "Season %s" % (seasons[0])
		season_string = " %s" % display_name
		use_season = seasons[0]

	dialog = xbmcgui.Dialog()
    	if dialog.yesno("Watched", "Do you want to mark all episodes of %s%s as %s?" % (series, season_string, command)):
        	progress = xbmcgui.DialogProgress()
        	progress.create('Updating episodes', 'Setting %s%s as %s' % (series, season_string, command))

		current_count = 0
		info_count = 0

		sql = ".timeout 100000;\n"
				
		for item in itemList:
			episode = item.GetEpisode()
			boxeeid = mc.GetInfoString("Container(52).ListItem("+str(info_count)+").Property(boxeeid)")
			info_count = info_count + 1
			print boxeeid
			if(episode != -1):
				current_count = current_count+1
				percent = int( ( episodes_count / current_count ) * 100)
				message = "Episode " + str(current_count) + " out of " + str(episodes_count)
				progress.update( percent, "", message, "" )
				path = item.GetPath()

				# First make sure we don't get double values in the DB, so remove any old ones				
				sql = sql + "DELETE FROM watched WHERE strPath = \""+path+"\" or (strBoxeeId != \"\" AND strBoxeeId = \""+boxeeid+"\");\n"
				if command == "watched":
					sql = sql + "INSERT INTO watched VALUES(null, \""+path+"\", \""+boxeeid+"\", 1, 0, -1.0);\n"

		common.file_put_contents("/tmp/sqlinject", sql)
		os.system('cat /tmp/sqlinject | /data/hack/bin/sqlite3 ' + db_path + 'boxee_user_catalog.db')

		xbmc.executebuiltin("Container.Update")
		xbmc.executebuiltin("Container.Refresh")
		xbmc.executebuiltin("Window.Refresh")
		progress.close()

		xbmc.executebuiltin("XBMC.ReplaceWindow(10483)")

#        	progress = xbmcgui.DialogProgress()
#        	progress.create('Updating episodes', 'Setting %s%s as %s' % (series, season_string, command))
#
#		for x in range(0, 10):
#			time.sleep(1);
#			xbmc.executebuiltin("Container.Update")
#			xbmc.executebuiltin("Container.Refresh")
#			xbmc.executebuiltin("Window.Refresh")
#
#		progress.close()
#
#		xbmc.executebuiltin("XBMC.ReplaceWindow(10483)")

		xbmc.executebuiltin("Notification(,%s marked as %s...,2000)" % (display_name, command))

if (__name__ == "__main__"):
    command = sys.argv[1]
    if command == "watched": set_watched("watched")
    if command == "unwatched": set_watched("unwatched")
    if command == "focus_last_unwatched": focus_last_unwatched(int(sys.argv[2]))
