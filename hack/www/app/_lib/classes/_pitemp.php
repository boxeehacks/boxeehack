<?php
	class heatPercentage {
		private function c2f($celsius) {
			return(round($celsius * 9 / 5 + 32));
		}

		function getCurrentTemp($statsOnly = 0){
			$maxtemp = 85;

			$currenttemp = shell_exec("/opt/local/bin/dtool 2");
			$degrees_c = round($currenttemp);
			$percentage = round($degrees_c / $maxtemp * 100);
			if ($statsOnly) {
				echo '"' . $degrees_c . '"';
				return;
			}
			if($percentage >= '80'){
			    $warning = "<img src=\"_lib/images/danger.png\" height=\"18\" />";
			    $bar = "barRed";
			}
			elseif($percentage >= '60'){
			    $warning = "<img src=\"_lib/images/warning.png\" height=\"18\" />";
			    $bar = "barAmber";
	          	} else {
	            		$warning = "<img src=\"_lib/images/ok.png\" height=\"18\" />";
	            		$bar = "barGreen";
	          	} ?>
			<div class="heatIcon">
				<img src="_lib/images/cpu_temp.png" align="middle">
			</div>			
			<div class="heatTitle">
				 CPU Heat 
			</div>
			<div class="heatWarning">
				<?php echo $warning; ?>
			</div>
			<div class="heatText">
				<div class="graph">
					<strong class="<?php echo $bar; ?>" style="width:<?php echo $percentage; ?>%;"><?php echo $percentage; ?>%</strong>
				</div> 
				<div class="clear"></div>
				<br/>
				Celsius: <strong><?php echo $degrees_c; ?>&deg;C</strong>(of <?php echo $maxtemp; ?>) &middot Fahrenheit: <strong><?php echo $this->c2f($degrees_c); ?>&deg;F</strong>(of <?php echo $this->c2f($maxtemp); ?>)<br/></div>		
			<div class="clear"></div><?php 
		}	
	}
