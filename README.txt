Excel File defaults to highlands.xlsx, but can be called anything as long as it has an .xlsx extension

The Excel File has 2 or 3 tabs:
	setup tab:				defines users, table, host, port	
	questions tab:			defines questions	
	tests tab (optional):	defines automatic tests
	
To initilize the system:
	python initialize_database.py [excelFile] 

To run the server:
	python server.py [excelFile]
	
To run the automatic tests (these are broken at present):
	python run_tests.py [excelFile]
	
To start the client assessment in a browser:
	https://<server-ip>:<port>
	https://assessmydeal.com:9097

To start the client with the charts in a browser:
	https://<server-ip>:<port>/client.html?charts
	https://assessmydeal.com:9097/client.html?charts

To run automatic tests you will need to install selenium:
	pip install selenium

To run server on A2Hosting server:
	ssh -p 7822 <user-name>@assessmydeal.com
	ssh -p 7822 chris@assessmydeal.com
	cd /opt/highlands/h-workshop/Python/src/_Highlands/highlands-secure
	nohup python server.py & disown

To run http server (to request redirect to https):
	nohup python server2.py & disown
	
To start ftp server:
	sudo systemctl start vsftpd

To do:
	make server a genuine daemon process
	install a valid SSL certificate on server

Note:
	realpath .	# print real path of a directory
	assessmydeal.com is 68.66.241.111
	assessmydeal.com is 209.124.74.241
	redirect commands:
		sudo iptables -A PREROUTING -t nat -i venet0 -p tcp --dport 443 -j REDIRECT --to-port 9097
		sudo iptables -A PREROUTING -t nat -i venet0 -p tcp --dport 80 -j REDIRECT --to-port 9096

	
	