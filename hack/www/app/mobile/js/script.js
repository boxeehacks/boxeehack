$(document).ready(function () {
	//$.getJSON('../_lib/API/stats.php', function (data) {
	$.getJSON('../_lib/API/stats.php', function (data) {
		//UPTIME
		$('#uptime>p').html('<strong>'+data.uptime+'</strong>');
		
		//CPU
		var cpuHTML = 'Loads: 1 Min: <strong>'+data.CPU.loads[0]+'</strong> &middot; 5 Mins: <strong>'+data.CPU.loads[1]+'</strong> &middot; 15 Mins: <strong>'+data.CPU.loads[2]+'</strong><br/>';
		cpuHTML += 'CPU is running at <strong>'+data.CPU.curFreq+'</strong><br/>';
		cpuHTML += 'Min: <strong>'+data.CPU.minFreq+'</strong> Max: <strong>'+data.CPU.maxFreq+' '+data.CPU.freqGovernor+'</strong>';
		
		$('#cpu>p').html(cpuHTML);
		//CPU HEAT
		$('#cpu_heat>p').html('<strong>'+data.CPU.temp+'&deg;C</strong>');
		
		//MEMORY
		var memHTML = 'Free: <strong>'+data.memory.ram.free+'MB</strong> Used: <strong>'+data.memory.ram.used+'MB</strong> Total: <strong>'+data.memory.ram.total+'MB</strong><br/>';
		var swapHTML = 'Free: <strong>'+data.memory.swap.free+'MB</strong> Used: <strong>'+data.memory.swap.used+'MB</strong> Total: <strong>'+data.memory.swap.total+'MB</strong><br/>';
		$('#memory>p').html(memHTML);
		$('#swap>p').html(swapHTML);
		
		//STORAGE
		var storageHTML = '';
		var l = data.storage.length;
		for (var i = 0; i < l; i++) {
			storageHTML += 'Mount: <strong>'+data.storage[i].mount+'</strong><br/><div style="padding-left:20px;">';
			storageHTML += 'Total: <strong>'+data.storage[i].total+'</strong> &middot; Free: <strong>'+data.storage[i].free+'</strong> &middot; Format: <strong>'+data.storage[i].format+'</strong></div>';
		}
		$('#storage>p').html(storageHTML);
		
		//NETWORK
		var netHTML = '<strong>Ethernet</strong><br/><div style="padding-left:20px">Received: <strong>'+data.Ethernet.received+'</strong> &middot; Sent: <strong>'+data.Ethernet.sent+'</strong> &middot; Total: <strong>'+data.Ethernet.total+'</strong><br/>';
		netHTML += 'Active Network Connections: <strong>'+data.Ethernet.active+'</strong></div>';
		$('#network>p').html(netHTML);
		
		//USERS
		var userHTML = '';
		var l = data.users.length;
		if (l == 0) {
			userHTML = 'No users logged in.';
		}
		else {
			for (var i = 0; i < l; i++) {
				userHTML += 'User: <strong>'+data.users[i].user+'</strong><br/><div style="padding-left:20px;">IP: <strong>'+data.users[i].ip+'</strong> &middot; Since: <strong>'+data.users[i].since+'</strong></div>';
			}
		}
		$('#users>p').html(userHTML);
	})
});