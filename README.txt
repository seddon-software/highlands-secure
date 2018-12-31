The installation directory must have two subdirectories:
	logs
	certs   

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

2a. To add usr to adm group:
	sudo usermod -a -G adm userName

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

7. To install Anaconda 5.3.1:
	wget http://repo.continuum.io/archive/Anaconda3-5.3.1-Linux-x86_64.sh
   	bash Anaconda3-5.3.1-Linux-x86_64.sh
	pip install --upgrade pip
	
8. To install additional Python libraries
	pip install --ignore-installed six
	pip install cherrypy
   	pip install pymysql
	pip install sendgrid
	pip install validate_email
	pip install reportlab

Note:
	asssessmydeal.com is 68.66.241.111
	assessmydeal.com is 199.195.116.16

To renew Certificates:
	sudo certbot renew --standalone --preferred-challenges http

	
	