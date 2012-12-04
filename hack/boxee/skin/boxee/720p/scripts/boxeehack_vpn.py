import os
import xbmc, xbmcgui

def vpn_function():
	os.system("/data/hack/vpn/vpn_check.sh")
	xbmc.sleep(400)
if os.path.exists("/tmp/vpn.enabled"):
	dialog = xbmcgui.Dialog()
	if dialog.yesno("VPN Connection", "Connect/Disconnect VPN?"):
		xbmc.executebuiltin("Notification(,Initiating...,2000)")
		os.system("/data/hack/vpn/vpn_connect.sh")
	
else:
	dialog = xbmcgui.Dialog()
        ok = dialog.ok('VPN Connection', 'VPN has not been configured.')

if (__name__ == "__main__"):
    section = sys.argv[1]

if section == "vpn": vpn_function()

