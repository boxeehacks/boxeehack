 <?php session_start();

// PiControl API

	$handle = file_get_contents("/etc/raspcontrol/database.aptmnt");
	$db = json_decode($handle);
	$username = $db->{'user'};
	$password = $db->{'password'};
	
	if($_GET['username'] == $username && $_GET['password'] == $password){
		
		$_SESSION['username'] = $username; ?>
		
		
		
		<?php
                if($_GET['action'] == 'reboot'){
                        system('sudo reboot');
                }
	
                if($_GET['action'] == 'stats'){
                        $uptime = shell_exec("cat /proc/uptime");
			$uptime = explode(" ", $uptime);          
		        $seconds = $uptime[0];
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

			$uptime = "Uptime:\n" . preg_replace('/\s+/',' ',$string);
$getLoad = sys_getloadavg();
		  
		  $rawCPUSpeed = shell_exec('cat /proc/cpuinfo | grep BogoMIPS');
		  $cpuSpeed = str_replace("BogoMIPS	: ", "", "$rawCPUSpeed");
                        $cpu = "CPU Load:\n1 min: " . $getLoad[0] . "\n" . "5 mins: " . $getLoad[1] . "\n" . "15 mins: " . $getLoad[2] . "\n" . "CPU Speed: " . $cpuSpeed . " MHz";

 exec('free -mo', $out);
		    preg_match_all('/\s+([0-9]+)/', $out[1], $matches);
		    list($total, $used, $free, $shared, $buffers, $cached) = $matches[1];
$percentage = round(($used - $buffers - $cached) / $total * 100);
                  $ram = "RAM: " . $percentage . "%" . "\n" . "Free: " . ($free + $buffers + $cached) . " MB" . "\n" . "Used: " . ($used - $buffers - $cached) . " MB" . "\n" . "Total: " . $total . " MB";
 exec('free -mo', $out);
		    preg_match_all('/\s+([0-9]+)/', $out[2], $matches);
		    list($total, $used, $free) = $matches[1];
		    
		    $percentage = round($used / $total * 100);
$swap = "Swap: " . $percentage . "%" . "\n" . "Free: " . $free . " MB" . "\n" . "Used: " . $used . " MB" . "\n" . "Total: " . $total . " MB";

    $bytes = disk_free_space("."); 
			    $si_prefix = array( 'B', 'KB', 'MB', 'GB', 'TB', 'EB', 'ZB', 'YB' );
			    $base = 1024;
			    $class = min((int)log($bytes , $base) , count($si_prefix) - 1);
			    $free =  sprintf('%1.2f' , $bytes / pow($base,$class));
				
				
				
			    $bytes = disk_total_space("."); 
			    $si_prefix = array( 'B', 'KB', 'MB', 'GB', 'TB', 'EB', 'ZB', 'YB' );
			    $base = 1024;
			    $class = min((int)log($bytes , $base) , count($si_prefix) - 1);
			    $total = sprintf('%1.2f' , $bytes / pow($base,$class));
		    
			
				
				$used = $total - $free;
				$percentage = round($used / $total * 100);

$hdd = "SD Card: " . $percentage . "%" . "\n" . "Free: " . $free . "GB" . "\n" . "Used: " . $used . "GB" . "\n" . "Total: " . $total . "GB";


	$netType = shell_exec("ifconfig");
	$netTypeRaw = explode(" ", $netType); 
	$netTypeFormatted = str_replace("encap:", "", $netTypeRaw);
	
	
    $dataThroughput = exec("ifconfig wlan0 | grep RX\ bytes", $out);
    $dataThroughput = str_ireplace("RX bytes:", "", $dataThroughput);
    $dataThroughput = str_ireplace("TX bytes:", "", $dataThroughput);
    $dataThroughput = trim($dataThroughput);
    $dataThroughput = explode(" ", $dataThroughput);
    
    
    
    $rxRaw = $dataThroughput[0] / 1024 / 1024;
    $txRaw = $dataThroughput[4] / 1024 / 1024;
	$rx = round($rxRaw, 2)." ";
	$tx = round($txRaw, 2);
	$totalRxTx = $rx + $tx;

$network = "Ethernet:\n" . "Received: " . $rx . "MB" . "\n" . "Sent: " . $tx . "MB" . "\n" . "Total: " . $totalRxTx . "MB";
                  
$whoUsersType = shell_exec("users");	
	$whoUsersFormatted = str_replace(" ", "\n", $whoUsersType);

$users = "Active Users:" . "\n" . $whoUsersFormatted;
Print $uptime . "\n\n" . $cpu . "\n\n" . $ram . "\n\n" . $swap . "\n\n" . $hdd . "\n\n" . $network. "\n\n" . $users;

                     }

 if($_GET['action'] == 'status'){
Print "Good";
}
                
		//Print "Auth Good";
	}else{
		Print "Auth Bad";
		$wrong = 1;
		
	}
	

