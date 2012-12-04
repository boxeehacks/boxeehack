<?php session_start();
if($_SESSION['username'] == ""){
	header('Location: ../../index.php');
	die;
}

	require('../classes/_ram.php'); 
	require('../classes/_pitemp.php'); 
	require('../classes/_hdd.php'); 
	require('../classes/_cpu.php'); 
	require('../classes/_uptime.php'); 
	require('../classes/_network.php');
	require('../classes/_who.php');
?>
		<div class="firstBlockWrapper">

			<?php $uptime = new systemUptime; $getSystemUptime = $uptime->getSystemUptime();?>
        	
        	<div class="clear"></div>
        	
        	<br/><br/>

	        <?php $load = new cpuLoad; $getLoad = $load->getCpuLoad();?>
        	
        	<div class="clear"></div>
        	
        	<br/><br/>
        	
        	<?php $ram = new ramPercentage; $percentage = $ram->freeMemory(); $percentage = $ram->freeSwap();?>
        	
        	<div class="clear"></div>
		<br/>
		<br/>
        	<?php $heat = new heatPercentage; $heatpercent = $heat->getCurrentTemp(); ?>
        	<div class="clear"></div>
        	
        	<br/><br/>

        	<?php $hdd = new hddPercentage; $storagepercentage = $hdd->freeStorage();?>
        	
        	<div class="clear"></div>
        	
        	<br/><br/>        	
            
            <?php //$net = networkUsage(); echo "Received: ".$net['rx']." Megabytes Sent: ".$net['tx']." Megabytes Total: ".($net['rx']+$net['tx'])." Megabytes"; ?>
            <?php $network = new network; $networkUseage = $network->networkUsage(); ?>

            <div class="clear"></div>
        	
        	<br/><br/>

        	<?php $users = new usersLoggedIn; $getusers = $users->getusersLoggedIn();?>
       	</div>
		<br/><br/>