<?php
/*
function networkUsage() {
}
 * */

class network{
	function networkUsage($statsOnly = 0) {
	
	$netType = shell_exec("ifconfig");
	$netTypeRaw = explode(" ", $netType); 
	$netTypeFormatted = str_replace("encap:", "", $netTypeRaw);
	
	
    $string = exec("ifconfig eth0 | grep RX");
   
    $tmp = explode(":", $string);
    $tmp2 = explode("(", $tmp[1]);
    $tmp3 = explode("(", $tmp[2]);
    
    
     
	$rx = $tmp2[0];
	$tx = $tmp3[0];   
   
     	$totalRxTx = $rx + $tx;
	$rx = round($rx / 1024 / 1024, 2);  
	$tx = round($tx / 1024 / 1024, 2);  
  
   	$totalRxTx = round($totalRxTx /1024 / 1024, 2);
   

		$iTotalConnections = shell_exec("/data/hack/bin/netstat -nta --inet | wc -l");
		$iTotalConnections--;
		
	if ($statsOnly) {
		echo '"'.$netTypeFormatted[7].'" : {
			"received" : "'.$rx.'",
			"sent" : "'.$tx.'",
			"total" : "'.$totalRxTx.'MB",
			"active" : "'.substr($iTotalConnections, 0, -1).'"
		}';
		return;
	}
	?>

	
	
	<div class="networkIcon">
		  	<img src='_lib/images/network.png' align='middle'>
		  </div> 
		  
		  <div class="networkTitle">
		  	Network
		  </div>
		  
		  <div class="networkText">
			<strong> <?php echo $netTypeFormatted[7]; ?> | </strong> Received: <strong><?php echo $rx; ?> MB</strong> &middot Sent: <strong><?php echo $tx; ?> MB</strong> &middot Total: <strong><?php echo $totalRxTx; ?> MB</strong> <br /> Active Network Connections: <strong><?php echo $iTotalConnections; ?></strong>
		  </div>
	
	
	
<?php
}
}

