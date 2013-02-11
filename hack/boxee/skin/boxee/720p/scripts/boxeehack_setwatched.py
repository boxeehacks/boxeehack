import time
import os,sys
import xbmc, xbmcgui, mc
import subprocess
import common
import time

from pysqlite2 import dbapi2 as sqlite

def get_window_id(special):
	if special == True:
		return xbmcgui.getCurrentWindowDialogId()
	else:
		return xbmcgui.getCurrentWindowId()

def get_list(listNum, special):
	try:
		lst = mc.GetWindow(get_window_id(special)).GetList(listNum)
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
	prevLen = 0
	count = 10
	while count > 0:
		time.sleep(0.1)
		lst = get_list(listNum, False)
		count = count - 1
		
		if lst != "":
			newLen = len(lst.GetItems())
			if newLen != prevLen:
				count = 5
			prevLen = newLen
	
	if lst == "" or len(lst.GetItems()) <= 2:
		pass
	else:
		item = lst.GetItem(1)
		items = lst.GetItems()
		lastItem = items[-1]

		more = 1
		reverse = 0

		if item.GetSeason() < lastItem.GetSeason():
			reverse = 1
		if item.GetSeason() == lastItem.GetSeason() and item.GetEpisode() < lastItem.GetEpisode():
			reverse = 1
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
					focus = info_count + 1
				info_count = info_count - 1
				
				if watched == "1":
					more = 0

		# make sure the list still exists
		lst = get_list(listNum, False)
		if lst != "":
			lst.SetFocusedItem(focus)

def set_watched(command):
	lst = get_list(52, False)
	count = 10
	while lst == "" and count > 0:
		time.sleep(0.1)
		lst = get_list(52, False)
		count = count - 1
		
	if lst == "":
		pass
	else:
		item = lst.GetItem(1)

		series = mc.GetInfoString("Container(52).ListItem.TVShowTitle")
		itemList = lst.GetItems()
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
			season_string = " Season %s" % (seasons[0])
			use_season = seasons[0]

		dialog = xbmcgui.Dialog()
		if dialog.yesno("Watched", "Do you want to mark all episodes of %s%s as %s?" % (series, season_string, command)):
			progress = xbmcgui.DialogProgress()
			progress.create('Updating episodes', 'Setting %s%s as %s' % (series, season_string, command))

			current_count = 0
			info_count = 0

			db_path = xbmc.translatePath('special://profile/Database/') + "./boxee_user_catalog.db"
			conn = sqlite.connect(db_path, 100000)
			c = conn.cursor()
			
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
					sql = "DELETE FROM watched WHERE strPath = \""+str(path).strip()+"\" or (strBoxeeId != \"\" AND strBoxeeId = \""+str(boxeeid).strip()+"\");"
					c.execute(sql)

					if command == "watched":
						sql = "INSERT INTO watched VALUES(null, \""+path+"\", \""+boxeeid+"\", 1, 0, -1.0);"
						c.execute(sql)

			c.execute("REINDEX;")

			conn.commit()
			c.close()
			conn.close()
			
			lst = get_list(52, False)
			if lst != "":
				lst.Refresh()
			xbmc.executebuiltin("XBMC.ReplaceWindow(10483)")

			progress.close()

			mc.ShowDialogNotification("%s marked as %s..." % (display_name, command))

if (__name__ == "__main__"):
	command = sys.argv[1]
	if command == "watched": set_watched("watched")
	if command == "unwatched": set_watched("unwatched")
	if command == "focus_last_unwatched": focus_last_unwatched(int(sys.argv[2]))
