from default import *
from tools import *

######
### GUI
######
### All Gui functions are called in this section, this makes porting the app more easy
######

### Main gui functions
class GUI:
    def __init__(self, **kwarg):
        self.windows = WINDOWS_ID
        self.id = kwarg.get('window',False)
        
        if kwarg.get('window',False):   self.window = mc.GetWindow(kwarg['window'])
        if kwarg.get('listid',False):   self.list = self.window.GetList(kwarg['listid'])
        if kwarg.get('window',False):   self.focus = self.FocusMain
        
    def SetVisible(self, id, bool):
        control = self.window.GetControl(id)
        control.SetVisible(bool)

    def ClearLists(self, lists):
        for id in lists:
            list = self.window.GetList(id)
            list.SetItems(mc.ListItems())

    def SetTexture(self, id, texture):
        self.window.GetImage(id).SetTexture(str(texture))

    def SetLabel(self, id, label):
        self.window.GetLabel(id).SetLabel(str(label))

    def SetButton(self, id, label):
        self.window.GetButton(id).SetLabel(str(label))

    def SetFocus(self, id):
        self.window.GetControl(id).SetFocus()

    def SetEnabled(self, id, bool):
        self.window.GetControl(id).SetEnabled(bool)

    def SetFocusedItem(self, list, id):
        _list = self.window.GetList(list)
        _list.SetFocusedItem(id)

    def PushState(self):
        self.window.PushState()
    
    def ClearStateStack(self, bool):
        self.window.ClearStateStack(bool)

    def GetInfoString(self, string):
        return mc.GetInfoString(string)
        
    def ShowDialog(self, id):
        mc.ActivateWindow(self.windows[id])

    def HideDialog(self, id):
        xbmc.executebuiltin("Dialog.Close(" + str(self.windows[id]) + ")")

    def ShowDialogConfirm(self, *args):
        return mc.ShowDialogConfirm(*args)

    def ShowDialogNotification(self, msg):
        mc.ShowDialogNotification(msg)

    def ShowDialogKeyboard(self, *args):
        return mc.ShowDialogKeyboard(*args)

    def ShowDialogNumeric(self, *args):
        import xbmcgui
        dialog = xbmcgui.Dialog()
        return dialog.numeric(*args)

    def ShowDialogBrowse(self, *args):
        import xbmcgui
        dialog = xbmcgui.Dialog()
        return dialog.browse(*args)

    def ShowDialogOk(self, *args):
        args = (str(r) for r in args)
        return mc.ShowDialogOk(*args)

    def FocusMain(self):
        if self.window.GetControl(2001).IsVisible(): self.window.GetControl(2001).SetFocus()
        if self.window.GetControl(2002).IsVisible(): self.window.GetControl(2002).SetFocus()
        if self.window.GetControl(2003).IsVisible(): self.window.GetControl(2003).SetFocus()
        if self.window.GetControl(2004).IsVisible(): self.window.GetControl(2004).SetFocus()

### Create list from object and sets to gui
class createList:
    def __init__(self, items):
        self.listItems = mc.ListItems()

        if getattr(items, '__iter__', False):
            for item in items:
                self.listItems.append(self.create(item))

    def create(self, item, type = mc.ListItem.MEDIA_UNKNOWN):
        listitem = mc.ListItem(type)
        action   = {
            'label'       :   listitem.SetLabel,
            'path'        :   listitem.SetPath,
            'thumb'       :   listitem.SetThumbnail,
            'SetContentType': listitem.SetContentType,
        }

        for key, value in item.items():
            try:    action[key](checkUTF8(value))
            except:
                try:    listitem.SetProperty(str(key), checkUTF8(value))
                except: pass
        return listitem

    def set(self, gui):
        gui.list.SetItems(self.listItems)
        if gui.id == gui.windows['main']: gui.focus()
