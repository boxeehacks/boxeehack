import os
import xbmc, xbmcgui

def vpn_function():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("VPN Connection", "Connect/Disconnect VPN?"):
	os.system("/bin/sh /data/hack/vpn.sh")
    xbmc.executebuiltin("Notification(,Establishing..,3000)")

if (__name__ == "__main__"):
    section = sys.argv[1]

    if section == "vpn":
        vpn_function()

