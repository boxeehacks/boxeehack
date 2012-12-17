import xbmc, xbmcgui
import time
import common

fanart = {}
def get_fanart_list():
    global fanart
    showlist = common.file_get_contents("/data/etc/.fanart")
    if showlist == "":
        return
        
    showlist = showlist.split("\n")
    fanart = {}
    for line in showlist:
        if "=" in line:
            line = line.split("=")
            show = line[0]
            art = line[1]
            fanart[show] = art

def store_fanart_list():
    global shows
    
    file = ""
    for show in fanart:
        file = file + show + "=" + fanart[show] + "\n"
    
    common.file_put_contents("/data/etc/.fanart", file)

first = 1
def grab_fanart_for_item(item):
    global fanart, first
    
    db_path = xbmc.translatePath('special://profile/Database/')
    
    label = item.GetLabel()
    path = item.GetPath()
    thumbnail = item.GetThumbnail()
    art = ""

    if label in fanart:
        art = fanart[item.GetLabel()]
    elif path != "" and path.find("boxeedb://") == -1:
        art = path[0:path.rfind("/")+1] + "fanart.jpg"
    elif thumbnail.find("special://") == -1:
        art = thumbnail[0:thumbnail.rfind("/")+1] + "fanart.jpg"
    else:
        command = "echo \"SELECT strCover FROM series WHERE strTitle=\'" + label + "\';\" | sqlite3 \"" + db_path + "../../../Database/boxee_catalog.db\""
        thumbnail = os.popen(command).read()
        art = thumbnail[0:thumbnail.rfind("/")+1] + "fanart.jpg"

    if art != "":
        fanart[label] = art
        item.SetProperty("fanart", art)

#    item.SetThumbnail(thumbnail)
    
def grab_fanart():
    get_fanart_list()
    
    items = mc.GetActiveWindow().GetList(53).GetItems()
    if len(items) == 0:
        time.sleep(0.5)
        items = mc.GetActiveWindow().GetList(53).GetItems()
        
    for item in items:
        grab_fanart_for_item(item)

#    mc.GetActiveWindow().GetList(53).SetItems(items)
#    mc.GetActiveWindow().GetList(53).Refresh()
#    xbmc.executebuiltin("Notification(,flap%s,2000)" % items[0].GetThumbnail())
    
    store_fanart_list()
        
        
#    grabloop = int(mc.GetInfoString("Skin.String(grab-fanart-loop)"))
#    if grabloop == 1:
#        return
#        
#    grabloop = 1
#    lasttitle = ""
#    xbmc.executebuiltin("Skin.SetString(grab-fanart-loop,%s)" % grabloop )
#    while grabloop == 1:
#        grabloop = int(mc.GetInfoString("Skin.String(grab-fanart-loop)"))
#        time.sleep(0.1)
#        if grabloop == 1:
#            item = mc.GetActiveWindow().GetList(53).GetFocusedItem()
#            
#            title = mc.GetInfoString("Container(53).ListItem.Label")
#            if lasttitle != title:
#                lasttitle = title
#                items = mc.GetActiveWindow().GetList(53)
#            
#                xbmc.executebuiltin("Notification(,%s,2000)" % title)

#def stop_grab_fanart():
#    xbmc.executebuiltin("Skin.SetString(grab-fanart-loop,0)")

if (__name__ == "__main__"):
    command = sys.argv[1]

    if command == "grab_fanart": grab_fanart()
#    if command == "stop_grab_fanart": stop_grab_fanart()
#    if command == "reset": stop_grab_fanart()
