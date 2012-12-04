<?php
	class versionCheck {
		function checkVersion(){
		    $version = "0.6.1"; //Version of the script, to check against CSV
		    $critical = FALSE; //Set Critical Variable to False 
		    $update = FALSE; //Set None Critical to Fasle too
		    $url = "http://fusionstrike.com/raspcontrol/version.csv"; //Link to your external CSV to check against
		    $fp = @fopen ($url, 'r') or print ('<center>Failed to check for the latest version.</center><br/><br/>'); //If the server is unreachable
		    $read = fgetcsv ($fp); //PHP fgetcsv
		    fclose ($fp); // Closes the connection
		    if ($read[0] > $version && $read[2] == "1") { $critical = TRUE; } // If its 1, set ciritcal to true
		    if ($read[0] > $version) { $update = TRUE; } // Anything other than 1 set update to true
		    if ($critical) { 
		        print '<center><font color="red">There is a critical update available (Version: '.$read[0].')!</font><br/>You can get it at <a href="'.$read[3].'">'.$read[3].'</a> (Description: '.$read[1].') <br/><br/></center>'; 
		        
		        ?>
		      
		       <!-- <a href="_lib/commands/_updateraspcontrol.php"><div class="subUpdateButton">
				<div style="float: left; padding-top: 8px; padding-right: 10px;"><img src="_lib/images/updateraspcontrol.png"></div> <div style="float: left; padding-top: 8px;">Auto-update Raspcontrol</div>
				</div></a> -->
				<br/><br/>
				
				<?php
		    }else if ($update){
		        print '<center><font color="green">There is a non critical update available (Version: '.$read[0].')!</font><br/>You can get it at <a href="'.$read[3].'">'.$read[3].'</a> (Description: '.$read[1].') <br/></center>';
		    
			?>
		    
			<!--<a href="_lib/commands/_updateraspcontrol.php"><div class="subUpdateButton">
				<div style="float: left; padding-top: 8px; padding-right: 10px;"><img src="_lib/images/updateraspcontrol.png"></div> <div style="float: left; padding-top: 8px;">Auto-update Raspcontrol</div>
				</div></a> -->
				<br/><br/>
		    <?php	
		    }	
		}
	}

