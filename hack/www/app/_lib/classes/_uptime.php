<?php
	class systemUptime {
		function getSystemUptime($statsOnly = 0){
		
		 	$uptime = shell_exec("cat /proc/uptime");
			$uptime = explode(" ", $uptime);          
		        $uptime = $this->secondsToReadableTime($uptime[0]);
				if ($statsOnly) {
					echo '"'.$uptime.'"';
					return;
				}
				?>
				
					<div class="uptimeIcon">
						<img src='_lib/images/uptime.png' align='middle'>
					</div> 
		  
					<div class="uptimeTitle">
						Uptime
					</div>
		  
					<div class="uptimeText">
						<strong><?php echo $uptime?></strong>
					</div>
				<?php
		}


		function secondsToReadableTime($seconds){

			$y = floor($seconds / 60/60/24/365);
			$d = floor($seconds/60/60/24) % 365;
			$h = floor(($seconds / 3600) % 24);
			$m = floor(($seconds / 60) % 60);
			$s = $seconds % 60;

			$string = '';

			if($y > 0)
			{
			$yw = $y > 1 ? ' years ' : ' year ';
			$string .= $y . $yw;
			}

			if($d > 0)
			{
			$dw = $d > 1 ? ' days ' : ' day ';
			$string .= $d . $dw;
			}

			if($h > 0)
			{
			$hw = $h > 1 ? ' hours ' : ' hour ';
			$string .= $h . $hw;
			}

			if($m > 0)
			{
			$mw = $m > 1 ? ' minutes ' : ' minute ';
			$string .= $m . $mw;
			}

			if($s > 0)
			{
			$sw = $s > 1 ? ' seconds ' : ' second ';
			$string .= $s . $sw;
			}

			return preg_replace('/\s+/',' ',$string);
		}


	}
	
