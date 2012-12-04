<!DOCTYPE html>
<html>
	<head>
		<title>Raspcontrol</title>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="js/jquery.mobile-1.2.0.min.css" type="text/css"/>
		<script type="text/javascript" src="js/jquery.min.js"></script>
		<script type="text/javascript" src="js/jquery.mobile-1.2.0.min.js"></script>
		<script type="text/javascript" src="js/script.js"></script>
	</head>
	<body>
		<div data-role="page" id="home">
			<div data-role="header">
				<div class="">
					<h3><img style="float:left;margin-top:-15px;" src="img/smallLogo.png"/>Raspcontrol.</h3>
					<h6 style="margin-top:-20px">The Raspberry Pi Control Centre</h6>
				</div>
				<h1>Home</h1>
			</div>
			<div data-role="content">
				<ul data-role="listview">
					<li id="uptime">
						<img class="ui-li-icon" src="img/uptime.png"/>
						<h1>Uptime</h1>
						<p>Loading...</p>
					</li>
					<li id="cpu">
						<img class="ui-li-icon" src="img/cpu.png"/>
						<h1>CPU</h1>
						<p>Loading...</p>
					</li>
					<li id="cpu_heat">
						<img class="ui-li-icon" src="img/cpu_temp.png"/>
						<h1>CPU Heat</h1>
						<p>Loading...</p>
					</li>
					<li id="memory">
						<img class="ui-li-icon" src="img/memory.png"/>
						<h1>Memory</h1>
						<p>Loading...</p>
					</li>
					<li id="swap">
						<img class="ui-li-icon" src="img/swap.png"/>
						<h1>Swap</h1>
						<p>Loading...</p>
					</li>
					<li id="storage">
						<img class="ui-li-icon" src="img/sd.png"/>
						<h1>Storage</h1>
						<p>Loading...</p>
					</li>
					<li id="network">
						<img class="ui-li-icon" src="img/network.png"/>
						<h1>Network</h1>
						<p>Loading...</p>
					</li>
					<li id="users">
						<img class="ui-li-icon" src="img/user.png"/>
						<h1>Active Users</h1>
						<p>Loading...</p>
					</li>
				</ul>
			</div>
			<div data-role="footer">
				<h4>Raspcontrol</h4>
			</div>
		</div>
	</body>
</html>