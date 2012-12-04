import os
import xbmc, xbmcgui

def vpn_function():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("VPN Connection", "Connect/Disconnect VPN?"):
    	xbmc.executebuiltin("Notification(,Initiating..,2000)")
	os.system("/data/hack/vpn.sh")

if (__name__ == "__main__"):
    section = sys.argv[1]

if section == "vpn": vpn_function()

