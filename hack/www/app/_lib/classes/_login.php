<?php session_start(); 
if(isset($_POST['login'])){
	$handle = file_get_contents("/data/hack/boxcontrol/database.aptmnt");
	$db = json_decode($handle);
	$username = $db->{'user'};
	$password = $db->{'password'};
	$_POST['homepath'] = substr($_SERVER['SCRIPT_FILENAME'], 0, strlen($_SERVER['SCRIPT_FILENAME']) - strlen(strrchr($_SERVER['SCRIPT_FILENAME'], "/"))); 

	if($_POST['username'] == $username && $_POST['password'] == $password){
		
		$_SESSION['username'] = $username; ?>
		
		<script type="text/javascript">
		<!--
		window.location = "main.php"
		//-->
		</script>
		
		<?php
		
	}else{
		
		$wrong = 1;
		
	}
	
}
