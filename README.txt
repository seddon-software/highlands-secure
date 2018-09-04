Excel File defaults to highlands.xlsx, but can be called anything as long as it has an .xlsx extension

The Excel File has 2 or 3 tabs:
	setup tab:				defines users, table, host, port	
	questions tab:			defines questions	
	tests tab (optional):	defines automatic tests
	
To initilize the system:
	python initialize_database.py [excelFile] 

To run the server:
	python server.py [excelFile]
	
To run the automatic tests:
	python run_tests.py [excelFile]
	
To start the client assessment in a browser:
	http://<server-ip>:<port>/client.html

To start the client with the charts in a browser:
	http://<server-ip>:<port>/client.html?charts

To run automatic tests you will need to install selenium:
	pip install selenium

To run server on A2Hosting server:
	ssh -p 7822 chris@68.66.241.111
	cd /opt/highlands/h-workshop/Python/src/_Highlands
	nohup python server.py & disown
	
To start ftp server:
	sudo systemctl start vsftpd
	

