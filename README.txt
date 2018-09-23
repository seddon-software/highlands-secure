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

To run http server (to request redirect to https):
	python -u server2.py
	
To start ftp server:
	sudo systemctl start vsftpd

Routing commands to use default ports for http and https:
	sudo iptables -A PREROUTING -t nat -i venet0 -p tcp --dport 443 -j REDIRECT --to-port 9097
	sudo iptables -A PREROUTING -t nat -i venet0 -p tcp --dport 80 -j REDIRECT --to-port 9096

To do:
	install a valid SSL certificate on server

Note:
	asssessmydeal.com is 68.66.241.111
	assessmydeal.com is 209.124.74.241

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
	
	