import time
import os,sys
import xbmc, xbmcgui, mc
import subprocess
import common
from random import randint


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

def focus_random_movie(listNum):
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
		items = lst.GetItems()
		info_count = len(items) - 1
		focus = randint(1, info_count)
		lst = get_list(listNum, False)
		if lst != "":
			lst.SetFocusedItem(focus)

if (__name__ == "__main__"):
	command = sys.argv[1]
	if command == "movies":
		thumb = int(xbmc.getInfoLabel("Skin.String(show-thumbnails)"))
		win = 53
		if thumb == 0:
			win = 51
		if thumb == 1:
			win = 50
		if thumb == 2:
			win = 52
		if thumb == 3:
			win = 53
		focus_random_movie(win)

	if command == "tvshows": focus_random_movie(52)
