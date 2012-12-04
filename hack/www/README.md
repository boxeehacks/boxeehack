# [Raspcontrol](http://raspcontrol.com)

Raspcontrol has been drastically improved since the inital release, we now have improved security, standalone deployment and many new awesome features!

### Getting Started Guide
##### Typical Requirements:

Raspcontrol is intended to be used with the PHP 5.4 inbuilt web server.

If your distribution does not support PHP 5.4 then you will need to build it from source or use a HTTP server such as Apache to access Raspcontrol.


***

## How to setup:

### Getting the source

#### .zip Download

You can download this as a _.zip_ from the GitHub Repository via the following link: 

	https://github.com/Bioshox/Raspcontrol/zipball/master
		
#### Git Clone

If you have Git installed you can clone the repo

	git clone https://github.com/Bioshox/Raspcontrol.git

### Getting it running

Raspcontrol is developed to be deployed with PHP 5.4, although it is possible to deploy it with any other HTTP server too.

#### Deploying with PHP 5.4

Navigate to the location you downloaded Raspcontrol to, from that location we need to give ./start.sh Read/Write/Execute Permissions

	sudo chmod 0777 ./start.sh
	
Now we can deploy the server by running the command from the same location
	
	sudo ./start.sh
	
You can now access Raspcontrol from _localhost_ directly on your Pi, or the Internal IP from a different computer on your LAN and externally if you're using Port Forwarding. (Raspcontrol binds to the IP 0.0.0.0:80 by default)

__This will work with PHP 5.4 ONLY__ you can check your PHP version by running the command
	
	php -v
	
#### With Apache

__Running Raspcontrol under Apache is considered insecure and not recomended.__

Add www-data on Apache to the SUDOERS file

	sudo VISUDO

On the last line add the following

	www-data ALL=(ALL) NOPASSWD: ALL
	
__Raspcontrol is not designed for production use, adding www-data to a SUDOERS file is dangerous and is not a permanent solution.__
		
If you're accessing Apaches web avaliable directory on your Raspberry Pi (using startx) you can navigate to localhost/raspcontrol, if you're accessing it from another computer on your Network you will need to navigate to http://your.internal.ip/raspcontrol.

### Setting up your account
				
Now you will be promted to setup a new account, this will create the initial user to login to the system.

***	
		
### Thanks!

Please feel free to contribute to this development!

[raspcontrol.com](http://raspcontrol.com)

Hosting proudly supplied by [Fusion Strike](http://fusionstrike.com)
