function ajaxTimeout(command) {
	document.getElementById(command).innerHTML = "no";
}

function Boxee(command, id)
{
	var com = "../cgi-bin/boxcontrol.cgi?" + command;
        var httpRequest = new XMLHttpRequest();
        httpRequest.open('GET', com, false);
        httpRequest.send(null);

	var httpTimeOut=setTimeout("ajaxTimeout(command);",2000);
	
        var txt = new String(httpRequest.responseText);
        document.getElementById(id).innerHTML = txt;
}
                                                                                                
function Status(command)
{
	var com = "../cgi-bin/boxstatus.cgi?" + command;
	var httpRequest = new XMLHttpRequest();
	httpRequest.open('GET', com, false);
	httpRequest.send(null);
	
	var httpTimeOut=setTimeout("ajaxTimeout(command);",2000);
	
	var txt = new String(httpRequest.responseText);
	document.getElementById(command).innerHTML = txt;
}

function init() {
	Status("ftp");
	Status("telnetd");
	Status("www");
}
