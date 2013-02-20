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

	mc.LogInfo("focus_last_unwatched() began")
	
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
	
		# If there is an item already selected when the list is loaded then it means
		# that the player has just been dismissed after playing an item. In this case 
		# there is no need to find the last unwatched, just honor the previous selection.
		# This also fixes the issue whereby after finishing playback the top item gets 
		# selected due to Boxee reporting it as watched, regardless of its actual status,
		# until the list items are updated asynchronously (and slowly).
		if lst.GetFocusedItem() != 1:
			return
					
		items = lst.GetItems()
		firstItem = items[1]
		lastItem = items[-1]

		reverse = 0

		if firstItem.GetSeason() < lastItem.GetSeason():
			reverse = 1
		elif firstItem.GetSeason() == lastItem.GetSeason() and firstItem.GetEpisode() < lastItem.GetEpisode():
			reverse = 1
		elif firstItem.GetSeason() == 1 and firstItem.GetEpisode() == 1:
			reverse = 1
		
		if reverse == 0:
			# newest items first
			start = 0
			end = len(items)
			step = 1
		else:
			# oldest items first
			start = len(items) - 1
			end = 0
			step = -1
			
		focus = end
		
		for n in range(start, end, step):				
			item = items[n]
			
			# skip items that are just list separators ('Season' labels)
			if item.GetSeason() == -1 and item.GetEpisode() == -1:			
				continue
					
			# Note: for whatever reason the indexes of 'items' and 'Container(52).ListItem' happen to be off by 1
			# So: items[0] == Container(52).ListItem(-1), items[1] == Container(52).ListItem(0) and so on and so forth					
			watched = mc.GetInfoString("Container(52).ListItem(" + str(n - 1) + ").Property(watched)")						
						
			if watched == "1":
				# no need to look any further
				break
			else:
				focus = n
			
		# make sure the list still exists
		lst = get_list(listNum, False)
		if lst != "":
			mc.LogInfo("focus_last_unwatched() ended selecting list item with index #" + str(focus))
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
