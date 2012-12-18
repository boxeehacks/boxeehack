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

    # to make sure we don't generate fanart entries for things like vimeo
    if path.find("http://") != -1:
        return

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
#        item.SetThumbnail(art)

def get_list(listNum):
    try:
        lst = mc.GetActiveWindow().GetList(listNum)
    except:
        lst = ""
    return lst

def grab_fanart_list(listNum):

    get_fanart_list()
    
    # sometimes the list control isn't available yet onload
    # so add some checking to make sure
    lst = get_list(listNum)
    count = 3
    while lst == "" and count > 0:
        time.sleep(0.25)
        lst = get_list(listNum)
        count = count - 1

    if lst == "":
        pass
    else:
        items = lst.GetItems()
        done = 1
        num = len(items)
        count = 5
        
        # some delays to wait until the list is complete
        # Boxee does a bit of lazy initialisation which
        # sometimes causes only half the list to be updated
        # otherwise
        while done != 0:
            time.sleep(0.25)
            items = lst.GetItems()
            if num == len(items) and num != 0:
                # do a few attempts to find more before giving up
                # because sometimes the Boxee Box is really slow
                count = count - 1
                if count == 0:
                    done = 0
            else:
                num = len(items)
        
                # try and apply the stuff we already know about
                for item in items:
                    grab_fanart_for_item(item)
        
        # store the fanart list for next time
        store_fanart_list()

if (__name__ == "__main__"):
    command = sys.argv[1]

    if command == "grab_fanart_list": grab_fanart_list(int(sys.argv[2]))