import os
import xbmc, xbmcgui

def vpn_function():
	os.system("sh /data/hack/vpn/vpn_chk.sh")
	xbmc.sleep(100)
if os.path.exists("/data/hack/vpn/vpn.enabled"):
	dialog = xbmcgui.Dialog()
	if dialog.yesno("VPN Connection", "Connect/Disconnect VPN?"):
		xbmc.executebuiltin("Notification(,Initiating...,2000)")
		os.system("sh /data/hack/vpn/vpn_con.sh")
	
else:
	dialog = xbmcgui.Dialog()
        ok = dialog.ok('VPN Connection', 'VPN has not been configured.')

if (__name__ == "__main__"):
    section = sys.argv[1]

if section == "vpn": vpn_function()

