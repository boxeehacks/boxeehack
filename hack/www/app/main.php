<?php session_start();
if($_SESSION['username'] == ""){
	require('index.php'); 
	die;
}


	require('_lib/classes/_ram.php'); 
	require('_lib/classes/_pitemp.php'); 
	require('_lib/classes/_hdd.php'); 
	require('_lib/classes/_cpu.php'); 
	require('_lib/classes/_uptime.php'); 
	require('_lib/includes/_header.php'); 
	require('_lib/classes/_network.php');
	require('_lib/classes/_who.php');
	require('_lib/classes/_versionCheck.php'); 
            
?>

	<div class="versionCheckContainer">
		<?php //$versionCheck = new versionCheck; $checkVersion = $versionCheck->checkVersion(); ?>
	</div>
    <div id="firstBlockContainer">
		
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
    </div>
    
    <?php require('_lib/includes/_footer.php'); ?>
