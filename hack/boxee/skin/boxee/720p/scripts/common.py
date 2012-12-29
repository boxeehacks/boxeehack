import os,sys,mc,xbmcgui

sys.path.append(os.path.abspath("./external"))

if 'linux' in sys.platform:
    sys.path.append(os.path.abspath("./external/Linux"))
elif 'win32' in sys.platform:
    sys.path.append(os.path.abspath("./external/win32"))
elif 'darwin' in sys.platform:
    sys.path.append(os.path.abspath("./external/OSX"))

def get_window_id(special):
    if special == True:
        return xbmcgui.getCurrentWindowDialogId()
    else:
        return xbmcgui.getCurrentWindowId()

def get_control(controlNum, special):
    try:
        control = mc.GetWindow(get_window_id(special)).GetControl(controlNum)
    except:
        control = ""
    return control

def get_list(listNum, special):
    try:
        lst = mc.GetWindow(get_window_id(special)).GetList(listNum)
    except:
        lst = ""
    return lst
    
# Read file contents into a string
def file_get_contents(filename):
    if os.path.exists(filename):
        fp = open(filename, "r")
        content = fp.read()
        fp.close()
        return content
    return ""

# Write string back to a file
def file_put_contents(filename, content):
    fp = open(filename, "w")
    fp.write(content.encode('ascii', 'ignore'))
    fp.close()