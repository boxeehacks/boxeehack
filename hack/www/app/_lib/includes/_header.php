<?php
session_start();

if(!isset($_SESSION['username']))
{
  $_Username = "";
}
else
{
  $_Username = $_SESSION['username'];
}
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">

<html>
<head>
    <title>Boxcontrol - Boxee Box Control Centre</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link rel="stylesheet" href="_lib/styles/style.css" type="text/css" media="screen" charset="utf-8">
    <link rel="stylesheet" href="_lib/styles/menu.css" type="text/css" media="screen" charset="utf-8">
<script src="../js/boxcontrol.js">
</script>


</head>

<body onload="init()">
    <div id="topContainer">
        <div class="topWrapper">
            <div style="float: left;">
               <h1><img src="_lib/images/smallLogo.png" style="float: left; margin-top: -15px;"> Boxcontrol.</h1>

                <h2>The Boxee Box Control Centre</h2>

            </div>

			<?php
			    if( $_Username == "")
			    {
			    } else
			    {
			      $distroTypeRaw = exec("cat /etc/*-release | grep PRETTY_NAME=", $out);
			      $distroTypeRawEnd = str_ireplace('PRETTY_NAME="', '', $distroTypeRaw);
			      $distroTypeRawEnd = str_ireplace('"', '', $distroTypeRawEnd);

			      $kernel = exec("uname -mrs");
                             $revision = exec("cat /opt/boxee/VERSION");
	
				$ip = exec("ifconfig | grep inet | grep 192 | awk '{print $2}'");
				$ip = substr($ip, 5);

				$access = exec("/data/hack/bin/busybox who -a | awk '{print $7}'");
				$tmp = explode("[", $access);
				$tmp2 = explode("]", $tmp[1]);
				
				$tmp3 = substr($tmp2[0], 7);
				 
				$access = $tmp3;	
						
				?>
				

				<div style="text-align: right; padding-top: 4px; color: #FFFFFF; font-family: Arial; font-size: 13px; float: right; width:500px;">
		                <strong>Hostname:</strong> <?php echo gethostname(); ?> &middot; 
		                <strong>Internal IP:</strong> <?php echo $ip ?><br/>
		                <strong>Accessed From:</strong> <?php echo $access; ?> &middot; 
		                
		                <strong>HTTP:</strong> <?php echo $_SERVER['SERVER_SOFTWARE']; ?><br/><br/>
		                <?php echo "<strong>Distribution:</strong>";?> Debian? <br/>
		                <?php echo "<strong>Kernel:</strong> ".$kernel; ?><br/>
                        <?php echo "<strong>Firmware:</strong> Boxee Box";?><br/>
						<?php echo "<strong>Revision:</strong> ".$revision; ?></br>

		            </div>

				<?php }
			?>
            
        </div>
    </div>

	<div class="clear"></div>
<?php
	if($_Username == ""){				
	}else{ ?>
			
    <div id="subNavContainer">
        <div class="subNavWrapper">
            
			<ul id="menu">
				<li>
					<a href="#">Home</a>
					<ul>
						<li><a href="index.php">Reload page</a></li>
						<li><a href="#" onclick="Boxee('reboot',0)">Reboot Boxee Box</a></li>
						<li><a href="#" onclick="Boxee('poweroff',0)">Poweroff Boxee Box</a></li>
					</ul>
				</li>
				<li>
					<a href="#">System</a>
					<ul>
		            			<li><a href="../cgi-bin/index.cgi">Boxee support tool</a></li>
		            			<li><a href="#" onclick="Boxee('ftp','ftp')"><span id="ftp">FTP server</span></a></li>
		            			<li><a href="#" onclick="Boxee('telnetd', 'telnetd')"><span id="telnetd">Telnet server</span></a></li>
		            			<li><a href="#" onclick="Boxee('www', 'www')"><span id="www">www server</span></a></li>
		            	</li>
					</ul>
				</li>
				<li>
					<a href="#">Services</a>
					<ul>
						<?php
							$json = file_get_contents(dirname(__FILE__)."/services.json");
							$services = json_decode($json);
							foreach ($services as $key => $value) {
								echo '<li><a href="_lib/includes/services.php?cmd='.$key.'">'.$key.'</a></li>';
								}
						?>
						<li><a href="#" onclick="Boxee('bGreen',0)" >Bright Green</a></li>
						<li><a href="#" onclick="Boxee('green',0)" >Green led</a></li>
						<li><a href="#" onclick="Boxee('ledoff',0)" >Led off</a></li>
						<li><a href="#" onclick="Boxee('red',0)" >Red led</a></li>
						<li><a href="#" onclick="Boxee('yellow',0)" >Yellow led</a></li>
					</ul>
				</li>
				<li><a href="#">About</a></li>
				<li><a href="#">Contact</a></li>
			</ul>           

        </div>
    </div>

<?php
	}

