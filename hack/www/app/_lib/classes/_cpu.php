<?php
	class cpuLoad {
		function getCpuLoad($statsOnly = 0){
		  $getLoad = sys_getloadavg();

		  $cpuCurFreq = round(shell_exec("cat /proc/cpuinfo | grep 'cpu MHz' | awk '{print $4}'")) . "MHz";
		  $cpuMinFreq = round(shell_exec("cat /proc/cpuinfo | grep 'cpu MHz' | awk '{print $4}'")) . "MHz";
		  $cpuMaxFreq = round(shell_exec("cat /proc/cpuinfo | grep 'cpu MHz' | awk '{print $4}'")) . "MHz";
		//  $cpuFreqGovernor = file_get_contents("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor");

          if ($getLoad[0] > 1) {
              $warning = "<img src=\"_lib/images/warning.png\" height=\"18\" />";
          } else {
              $warning = "<img src=\"_lib/images/ok.png\" height=\"18\" />";
          }
		  
		  if ($statsOnly) {
			$heat = new heatPercentage;
			echo '{
				"loads" : ['.$getLoad[0].','.$getLoad[1].','.$getLoad[2].'],
				"curFreq" : "'.$cpuCurFreq.'",
				"minFreq" : "'.$cpuMinFreq.'",
				"maxFreq" : "'.$cpuMaxFreq.'",
				"freqGovernor" : "'.substr($cpuFreqGovernor, 0, -1).'",
				"temp" : ';
				$heatpercent = $heat->getCurrentTemp(true);
			echo '}';
			return;
		  }
          ?>

		  <div class="cpuIcon">
		  	<img src='_lib/images/cpu.png' align='middle'>
		  </div>

		  <div class="cpuTitle">
		  	CPU 
		  </div>

		  <div class="cpuWarning">
		  	<?php echo $warning ?>
		  </div>

		  <div class="cpuText">
			  Loads: 1 Min: <strong> <?php echo $getLoad[0]; ?> </strong> &middot
			  5 Mins: <strong><?php echo $getLoad[1]; ?> </strong> &middot
			  15 Mins: <strong><?php echo $getLoad[2]; ?> </strong> <br/><br/> CPU is running at <strong><?php echo $cpuCurFreq; ?></strong><br/><br/>
			  Min: <strong><?php echo $cpuMinFreq; ?> </strong> Max: <strong><?php echo $cpuMaxFreq; ?> </strong>  <strong><?php echo $cpuFreqGovernor; ?> </strong> 
		  </div>
<?php
		}
		}
