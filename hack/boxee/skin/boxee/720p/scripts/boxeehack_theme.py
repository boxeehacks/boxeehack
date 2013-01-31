import os
import xbmc, xbmcgui, mc
import ConfigParser
import common
themes =[]
theme_count = 0
theme_shown = 0

def theme_next():
	get_themes() #Load varaiables with theme names based on the directory structure
	theme_selected_tracker = get_theme_selected_from_file() #Get the numerical value of the theme currently showing on the boxee+ settings page
	num = int(theme_selected_tracker) + 1 #convert string read from file to int so a comparison can be completed and add 1
	if num >= theme_count: num = 0 # if the number is the last of the themes in the array then reset back to 0.

	theme_selected_tracker = "%s" % num # convert it back to string to be written to the tracker file.

	common.file_put_contents("/data/etc/.replace_theme_enabled", theme_selected_tracker) #write the currently shown theme number back to file
	xbmc.executebuiltin("Skin.SetString(theme-name,%s)" % get_theme_name() ) #change the text shown on the setting screen.

def theme_previous():
	get_themes() #Load varaiables with theme names based on the directory structure
	theme_selected_tracker = get_theme_selected_from_file() #Get the numerical value of the theme currently showing on the boxee+ settings page
	num = int(theme_selected_tracker) - 1 #convert string read from file to int so a comparison can be completed and add 1
	if num < 0: num = theme_count -1 # if the number has been set back to 0 then go back to the top.

	theme_selected_tracker = "%s" % num# convert it back to string to be written to the tracker file.
	common.file_put_contents("/data/etc/.replace_theme_enabled", theme_selected_tracker) #write the currently shown theme number back to file
	xbmc.executebuiltin("Skin.SetString(theme-name,%s)" % get_theme_name() ) #change the text shown on the setting screen.

def get_theme_path():
	theme_selected_tracker = get_theme_selected_from_file()  #Get the numerical value of the theme currently showing on the boxee+ settings page
	num = int(theme_selected_tracker) # convert from string to int
	location = "/data/hack/boxee/skin/" + themes[num] #build the path based on the theme name/dir name


	return location

def get_theme_name():
	theme_selected_tracker = get_theme_selected_from_file()  #Get the numerical value of the theme currently showing on the boxee+ settings page
	num = int(theme_selected_tracker) #convert string to int.
	name = themes[num] #set the variable name to be what the name stored in the array/list at point shown on screen.


	return name

def get_themes():
	folder = r'/data/hack/boxee/skin' #location to look for themes
	global themes #make the variables global to avoid rerunning the script
	global theme_count
	themes = [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))] #fill list/array with directories, to look for folders only.
	theme_count = len(themes)


def apply_theme():
	get_themes() #Load varaiables with theme names based on the directory structure
	theme_location = get_theme_path() #Load variable theme_location with the theme path
	theme_name = get_theme_name() #Load variable theme_name with the theme name
	should_restart = 'false' #Created variable to monitor if the selected theme needs a full restart
	
	if theme_name == 'boxee': # Ask for confirmation of a full restart if the selected theme is boxee
		if mc.ShowDialogConfirm("Restart Required", "To apply the original boxee theme a full restart is required", "Cancel", "Restart"):
			should_restart = 'true'
		else:
			return
	if os.path.isfile(theme_location + '/skin.sh'):#checks the presence of skin.sh before applying the theme
		if os.path.isfile(theme_location + '/media/Textures.xbt'):#checks the presence of Textures.xbt before applything theme.
			commandStr = "cp -f " + theme_location + "/*.sh /data/hack/"#build the copy comand to copy skin.sh and or splash.sh to the hack directory
			commandStr = "%s" % commandStr#converts to a string
			os.system(commandStr)#exectures the copy command
			os.system("dos2unix /data/hack/*.sh")#if the .sh file has been edited in windows then its not possible to execute it. this converts the files to unixx files
			os.system("chmod 777 /data/hack/*.sh")#ensures all *.sh files are executable
			os.system("sh /data/hack/skin.sh")#runs skin.sh to map the texture folder to the curenntly chosen theme
			common.file_put_contents("/data/etc/.currently_enabled_theme", theme_name)#write the currently enabled theme to text file
		elif theme_name == 'boxee':#boxee is the only theme that doesnt require a Textures.xby so make an exception if its not present
			commandStr = "cp -f " + theme_location + "/*.sh /data/hack/"
			commandStr = "%s" % commandStr
			os.system(commandStr)
			os.system("dos2unix /data/hack/*.sh")
			os.system("chmod 777 /data/hack/*.sh")
			os.system("sh /data/hack/skin.sh")
			common.file_put_contents("/data/etc/.currently_enabled_theme", theme_name)#write the currently enabled theme to text file
		else:
			mc.ShowDialogOk("Error", "It appears that this theme has not been contructed correctly.\n\n Please contact the author of the theme for further assistance")#error message for missing Textures.xbt
			return
	else:
		mc.ShowDialogOk("Error", "It appears that this theme has not been contructed correctly.\n\n Please contact the author of the theme for further assistance")#error message for missing skin.sh
		return
	if should_restart == 'true':#if the restart variable was set to true restart
		os.system("reboot")
	else:
		os.system("sh /data/hack/reset.sh")	#if the variable was set to false do a soft reset
	
def get_theme_selected_from_file():
	theme_selected_tracker = common.file_get_contents("/data/etc/.replace_theme_enabled")
	if theme_selected_tracker == "":
		theme_selected_tracker = "0"
	return theme_selected_tracker

def delete_theme():
	get_themes() #Load varaiables with theme names based on the directory structure
	theme_location = get_theme_path() #Load variable theme_location with the theme path
	theme_name = get_theme_name()
	currently_enabled = common.file_get_contents("/data/etc/.currently_enabled_theme")#read the currently enabled theme.
	if theme_name == 'boxee':
		mc.ShowDialogOk('Error','You cannot remove the boxee theme')
		return
	if theme_name == currently_enabled:
		mc.ShowDialogOk('Error','This is the currently enabled theme. \n if you wish to remove this theme please apply another theme before deleting this theme.')
		return
	if mc.ShowDialogConfirm("Confirmation", "Are you sure you wish to delete this theme", "Cancel", "Delete"):
		commandStr = "rm -rf " + theme_location + "/"#build the delete string
		commandStr = "%s" % commandStr#converts to a string
		os.system(commandStr)#action the delete
		mc.ShowDialogNotification("Theme Deleted")
	else:
		return
	
	

def theme_get():#method for downloading theme
	URL = mc.ShowDialogKeyboard("Enter Theme URL:", "", False) #show dialog boxee asking for URL
	if URL != "":#check if there is content entered
		if URL.lower().find('.zip') != -1:#convert the entered string to lowercase and see if it contains '.zip'
			mc.ShowDialogWait()#show spinning circle
			mc.ShowDialogNotification("Downloading Theme")#inform the user what is happening
			os.system("wget "+ URL + " -P /data/hack/boxee/skin/")#launch wget to download the file.
			mc.HideDialogWait()#remove the spinning circle
			mc.ShowDialogNotification("Download Complete")#keep the user updated.
			mc.ShowDialogNotification("Unpacking Theme.")
			mc.ShowDialogWait()
			os.system("unzip /data/hack/boxee/skin/*.zip -d /data/hack/boxee/skin/")#unzip the downloaded file to the skin dir
			os.system("rm /data/hack/boxee/skin/*.zip")#remove the zip file
			mc.HideDialogWait()
			mc.ShowDialogNotification("Theme Unpacked")
		else:
			mc.ShowDialogOk("Error", "The URL you have entered is either incorrct or the theme is not in a zip file.")#if the url does not contain .zip

if (__name__ == "__main__"):
	command = sys.argv[1]

	if command == "theme_next": theme_next()
	if command == "theme_previous": theme_previous()
	if command == "theme_apply": apply_theme()
	if command == "theme_get": theme_get()
	if command == "theme_delete": delete_theme()