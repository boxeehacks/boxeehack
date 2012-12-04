<?php
session_start();

if($_SESSION['username'] == ""){
	die("You are not logged in");
}

if(isset($_GET['cmd'])){

	echo '<pre>';

	$json = file_get_contents(dirname(__FILE__)."/services.json");
	$services = json_decode($json);
	$command = $services->{$_GET['cmd']};
	$last_line = system($command, $retval);
	
	echo '</pre>';
}

?>

<br/>
<a href="<?php echo $_SERVER['HTTP_REFERER']; ?>">Return To Previous Page</a>
