<?php
session_start();

if($_SESSION['username'] == ""){
	die("You are not logged in");
}

echo '<pre>';

$last_line = system('sudo wget http://goo.gl/1BOfJ -O /usr/bin/rpi-update && sudo chmod +x /usr/bin/rpi-update && sudo apt-get -y install git-core && sudo apt-get -y install ca-certificates', $retval);

// Printing additional info
echo '
</pre>'; ?>
Firmware Updater Installed!<br/>
<a href="<?php echo $_SERVER['HTTP_REFERER']; ?>">Return To Previous Page</a>
