Excel File defaults to highlands.xlsx, but can be called anything as long as it has an .xlsx extension

The Excel File has 2 or 3 tabs:
	setup tab:				defines users, table, host, port	
	questions tab:			defines questions	
	tests tab (optional):	defines automatic tests
	
To initilize the system:
	python initialize_database.py [excelFile] 

To run the server:
	python server.py [excelFile]
	
To run automatic tests you will need to install selenium:
	pip install selenium

To run the automatic tests
	python run_tests.py [excelFile]
	
To start the client assessment in a browser:
	https://<server-ip>:<port>
	https://assessmydeal.com:9097

To start the client with the charts in a browser:
	use the normal URL but login as manager
	https://<server-ip>:<port>

To run server on A2Hosting server:
	ssh -p 7822 <user-name>@assessmydeal.com
	ssh -p 7822 chris@assessmydeal.com
	cd /opt/highlands/h-workshop/Python/src/_Highlands/highlands-secure
	python -u server.py [excelFile]

To get updates:
	sudo apt-get update

Installing a new A2 Server:

1. To create a new user on Ubuntu:
	sudo adduser chris
	
2. To add user to the sudo group:
	sudo usermod -aG sudo

3. To install and start ftp server:
	sudo apt-get install vsftpd
	sudo systemctl start vsftpd

4. Routing commands to use default ports for https:
	sudo iptables -A PREROUTING -t nat -i venet0 -p tcp --dport 443 -j REDIRECT --to-port 9097

	sudo iptables -t nat --line-numbers -L		# list routings
	sudo iptables -t nat -D PREROUTING 3		# remove routing number 3
	
5. To install git:
	sudo apt-get install git-core
	git clone https://github.com/seddon-software/highlands-secure.git

6. To install and start MySQL:
	sudo apt-get install mysql-server
	mysql_secure_installation
	sudo systemctl start mysql

7. To install Anaconda 3.4:
	wget http://repo.continuum.io/archive/Anaconda3-4.3.0-Linux-x86_64.sh
   	bash Anaconda3-4.3.0-Linux-x86_64.sh
   	pip install pymysql
	must create log directory
	must set up certs   
Note:
	asssessmydeal.com is 68.66.241.111
	assessmydeal.com is 199.195.116.16

Certs:
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/asssessmydeal.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/asssessmydeal.com/privkey.pem
   Your cert will expire on 2018-12-21. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot
   again. To non-interactively renew *all* of your certificates, run
   "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
	
	