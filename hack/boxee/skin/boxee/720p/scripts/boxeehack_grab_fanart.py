import xbmc, xbmcgui
import time
import subprocess
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
    path = "%s" % item.GetPath()
    if "stack:" in path:
        path = path.split(" , ")
        path = path[len(path)-1]
        
    thumbnail = item.GetThumbnail()
    art = ""

    if label in fanart:
        art = fanart[item.GetLabel()]
    elif path != "" and path.find("boxeedb://") == -1:
        art = path[0:path.rfind("/")+1] + "fanart.jpg"
    elif thumbnail.find("special://") == -1:
        art = thumbnail[0:thumbnail.rfind("/")+1] + "fanart.jpg"
#    else:
#        sql = ".timeout 1000000\n"
#        if path.find("boxeedb://") == -1:
#            # it must be a movie
#            sql = sql + "SELECT strCover FROM video_files WHERE strTitle=\"" + label + "\";\n"
#        else:
#            # it must be a tv show
#            sql = sql + "SELECT strCover FROM series WHERE strTitle=\"" + label + "\";\n"
#
#        common.file_put_contents("/tmp/sqlinject", sql)
#        os.system('/bin/sh \'cat /tmp/sqlinject | /data/hack/bin/sqlite3 "' + db_path + '../../../Database/boxee_catalog.db" > /tmp/readsql\'')
#        thumbnail = common.file_get_contents("/tmp/readsql")
#        if first == 1:
#            first = 0
#            xbmc.executebuiltin("Notification(,'%s',)" % thumbnail)
#        if "/" in thumbnail:
#            art = thumbnail[0:thumbnail.rfind("/")+1] + "fanart.jpg"

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

    store_fanart_list()

if (__name__ == "__main__"):
    command = sys.argv[1]

    if command == "grab_fanart": grab_fanart()