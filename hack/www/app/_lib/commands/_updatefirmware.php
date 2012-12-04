<?php
session_start();

if($_SESSION['username'] == ""){
	die("You are not logged in");
}

$last_line = system('sudo rpi-update > /dev/null &');
$last_line = system('sudo ldconfig');

header("location: ".$_SERVER['HTTP_REFERER']);
