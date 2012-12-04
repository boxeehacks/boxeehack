<?php
session_start();

if($_SESSION['username'] == ""){
	die("You are not logged in");
}
echo '<pre>';
 
$last_line = system('if [ ! -d /usr/lib/git-core ]; then sudo apt-get -y install git-core;fi && sudo git clone https://github.com/Bioshox/Raspcontrol.git '.$_SESSION['homepath'].'Update && sudo rm -R -f '.$_SESSION['homepath'].' && sudo mv '.$_SESSION['homepath'].'Update '.$_SESSION['homepath'].'', $retval);
// Printing additional info
echo '
</pre>'; ?>
Raspcontrol updated!<br/>
<a href="<?php echo $_SERVER['HTTP_REFERER']; ?>">Return To Previous Page</a>

