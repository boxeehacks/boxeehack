<?php
class usersLoggedIn{
	function getusersLoggedIn($statsOnly = 0) {

	$whoUsersType = shell_exec("/data/hack/bin/who -a | grep -v exit");	
	$whoUsersType2 = shell_exec("/data/hack/bin/busybox who -a | grep -v exit");	
	$whoUsersFormatted = str_replace(" ", " &middot ", $whoUsersType);	
	if (!$statsOnly) {
	?>

	
	
	<div class="userIcon">
		  	<img src='_lib/images/user.png' align='middle'>
		  </div> 
		  
		  <div class="userTitle">
		  	Active Users
		  </div>
		  
		  <div class="userText">
		  	<div style="width: 500px">
		  	<?php }
				if($whoUsersFormatted == ""){
					if ($statsOnly) {
						echo '"[]"';
						return;
					}
					echo "<strong>No users logged in</strong>";
		  	}else{
		  		$s = "";
				if ($statsOnly) {
					echo '[';
					$statsText = '';
				}
				//Split lines into individual array elements
				$lines = explode ("\n", $whoUsersType);
				$lines2 = explode ("\n", $whoUsersType2);
				
				$i= -1;	
				foreach ($lines as $line)
				{
				$i++;
					//Replace multiple spaces with single space
					$line = preg_replace("/ +/", " ", $line);

					if (strlen($line)>0)
					{
						
						$tmp = explode("[", $lines2[$i]);
						$tmp = explode("]", $tmp[1]);
						$tmp2 = substr($tmp[0], 7);
						//Now split fields into multiple values
						$fields = explode(" ", $line);
						if ($statsOnly) {
							$statsText .= '{
								"user" : "'.$fields[0].'",
								"ip" : "'.$tmp2.'",
								"since" : "'.$fields[4].'"
							},';
							continue;
						}
						$s .= "<div style='float: left; padding-bottom: 30px; padding-right: 20px;'><strong>User:</strong>Root<br />";
						$s .= "<strong>IP From:</strong> " . $tmp2 . "<br />";
						$s .= "<strong>Since:</strong> " . $fields[4] . "</div>";

						$s .= "";
					}
				}
				if ($statsOnly) {
					echo substr($statsText, 0, -1);
					echo ']';
					return;
				}
				echo $s;
		  	}
			?>
		  	</div>		  	
		  </div>
	
	<div style="clear:both"></div>
	
	
<?php
}
}

