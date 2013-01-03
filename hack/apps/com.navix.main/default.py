import os
import sys

# SET APP WIDE GLOBAL VARS
CWD             = os.getcwd().replace(";","")
ROOT            = CWD
PLATFORM        = "boxee"
VERSION         = '4.07'
SOURCES         = 'http://navi-x.googlecode.com/svn/trunk/Navi-X%20BOXEE/source/data/settings/sources.json'
WINDOWS_ID      = {
                        'main':15000, 'dialog-wait':15100, 'dialog-splash':15110, 'dialog-info':15120, 'dialog-search-history':15140,
                        'dialog-search-options':15150, 'dialog-text':15160, 'dialog-subtitle':15170, 'dialog-settings':15190, 'dialog-options':15200, 'dialog-image':15210,
                }
WINDOWS_STACK   =   []

sys.path.append(os.path.join(ROOT, 'libs'))
sys.path.append(os.path.join(ROOT, 'external'))

import mc
import xbmc
import re

# Init App
if ( __name__ == "__main__" ):
    mc.ActivateWindow(15000)
    mc.ActivateWindow(15110)
    mc.ActivateWindow(15100)

    import navi

    if len(mc.GetWindow(15000).GetList(60).GetItems()) < 1:
        app = navi.Navi_APP()
    else:
        app.api.download.active = False
        app.gui.HideDialog('dialog-wait')
    app.gui.HideDialog('dialog-splash')

