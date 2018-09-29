############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################


import logging.handlers
import datetime
import sys
import smtplib
import random
import hashlib
import string
from email.mime.text import MIMEText
import http.server
import urllib.parse, json

# my libraries
sys.path.append("libs")
from myglobals import MyGlobals
from checkbox import Checkbox
from scatter import Scatter
from piechart import Radio
from chart import Chart
from excel import Excel
from table import Table
from database import Database


checkbox = Checkbox()
scatter = Scatter()
radio = Radio()
chart = Chart()
xl = Excel()
table = Table()
db = Database()
g = MyGlobals()

LOG_FILENAME = "logs/{}-{}-{}-{}.log".format(
    g.get("database"), 
    g.get("table"), 
    g.get("usersTable"),
    g.get("port"))

def setupLogging():
    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    
    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1000000, backupCount=10)
    my_logger.addHandler(handler)
    return my_logger

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # this routine handles log messages from http.server
        # by leaving this function empty we effectively block server messages
        # remove or rename this routine to see sever messages
        return
   
    def do_POST(self):
        jsonResponse = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.end_headers()

        jsonAsString = jsonResponse.decode("UTF-8")
        results = json.loads(jsonAsString)

        sql.saveResults(results, self.headers)
        radio.refresh()
        chart.refresh()
        return

    def do_GET(self):
        def getMimeType():
            extension = fileName.split(".")[-1]
            if(extension == "ico"): return "image/x-icon"
            if(extension == "css"): return "text/css"
            if(extension == "jpg"): return "image/jpeg"
            if(extension == "png"): return "image/png"
            if(extension == "svg"): return "image/svg+xml"
            return "text/html"
            
        def sendHeaders(code=200):
            if code == 200:
                self.send_response(code)
                self.send_header("Content-type", getMimeType())
            else:
                self.send_response(code)
            self.end_headers()

        def hashPassword(password):
            return hashlib.sha1(password.encode()).hexdigest()
                    
        def authenticate():
            email = None
            for entry in self.headers._headers:
                if entry[0] == "Authorization": 
                    email, password1 = entry[1].split("+")

                    # passwords are stored as SHA1 hashes in the database                    
                    password1hash = hashPassword(password1)
                    password2hash = db.getPassword(email)
                    if password1hash == password2hash: 
                        return email, "valid"
                    else:
                        return email, None
            return None
        
        def sendCodeInEmail(email, code):
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("assess.my.deal.2018", "My-team-is-spurs.")
                msg = MIMEText(str(code))
                msg['Subject'] = 'Highlands AssessMyDeal Registration Code'
                msg['From'] = 'assess my deal'
                msg['To'] = email 
                server.send_message(msg)
            except:
                log("send email failed for {}".format(email))
            finally:
                server.quit()
                
        def generateCode():
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        def log(message):
            my_logger.debug("{}: ({}) {}".format(datetime.datetime.now(), self.client_address[0], message))
 
        parsedUrl = urllib.parse.urlparse(self.path) # returns a 6-tuple
        fileName = parsedUrl[2]
        queryString = parsedUrl[4]
        fileName = fileName[1:]  # remove leading '/'

        # make login.html the default pages
        if fileName == "": fileName = "login.html"
        if fileName == "login.html": log("website accessed")
        data = urllib.parse.parse_qs(queryString)

        if(fileName == "favicon.ico"):
            sendHeaders()
            return
        elif(fileName == "questions"):
            sendHeaders()
            jsonString = json.dumps(xl.getQuestions())
            jsonAsBytes = jsonString.encode("UTF-8")
            self.wfile.write(jsonAsBytes)
        elif(fileName == "options"):
            sendHeaders()
            jsonString = json.dumps(xl.getOptions())
            jsonAsBytes = jsonString.encode("UTF-8")
            self.wfile.write(jsonAsBytes)
        elif(fileName == "emails-and-clients"):
            sendHeaders()
            jsonString = json.dumps(sql.getEmailsAndClients())
            jsonAsBytes = jsonString.encode("UTF-8")
            self.wfile.write(jsonAsBytes)
        elif(fileName == "chart-data"):
            sendHeaders()
            jsonString = json.dumps(chart.getChartData())
            jsonAsBytes = jsonString.encode("UTF-8")
            self.wfile.write(jsonAsBytes)
        elif(fileName == "table-data"):
            sendHeaders()
            jsonString = json.dumps(table.getTableData())
            jsonAsBytes = jsonString.encode("UTF-8")
            self.wfile.write(jsonAsBytes)
        elif(fileName == "checkbox-data"):
            sendHeaders()
            jsonString = json.dumps(checkbox.getCheckboxData())
            jsonAsBytes = jsonString.encode("UTF-8")
            self.wfile.write(jsonAsBytes)
        elif(fileName == "scatter-data"):
            sendHeaders()
            jsonString = json.dumps(scatter.getScatterChartData())
            jsonAsBytes = jsonString.encode("UTF-8")
            self.wfile.write(jsonAsBytes)
        elif(fileName == "piechart-data"):
            sendHeaders()   
            jsonString = json.dumps(radio.getPieChartData())
            jsonAsBytes = jsonString.encode("UTF-8")
            self.wfile.write(jsonAsBytes)
        elif(fileName == "piechart-questions-options"):
            sendHeaders()
            jsonString = json.dumps(sql.getPieChartQuestionsAndOptions())
            jsonAsBytes = jsonString.encode("UTF-8")
            self.wfile.write(jsonAsBytes)
        elif(fileName == "change-password"):
            oldPassword1hash = db.getPassword(data['email'][0])
            oldPassword2 = data['oldPassword'][0]
            oldPassword2hash = hashPassword(oldPassword2)

            if oldPassword1hash == oldPassword2hash:
                sendHeaders()
                db.createUser(data['email'][0], data['newPassword'][0], "")
                self.wfile.write('["password changed"]'.encode())
                log("password updated for {}".format(data['email'][0]))
            else:
                sendHeaders(401)
                self.wfile.write('["incorrect password"]'.encode())
                log("password update failed for {}".format(data['email'][0]))
        elif(fileName == "start-registration"):
            sendHeaders()
            code = generateCode()
            sendCodeInEmail(data['email'][0], code)
            db.createUser(data['email'][0], "", code)
            self.wfile.write('["registration code sent"]'.encode())
            log("registration code {} sent to {}".format(code, data['email'][0]))
        elif(fileName == "complete-registration"):
            code1 = db.getCode(data['email'][0])
            code2 = data['code'][0]
            if code1 == code2:
                sendHeaders()
                db.createUser(data['email'][0], data['password'][0], data['code'][0])
                self.wfile.write('["registration succeeded"]'.encode())
                log("{} is now registered".format(data['email'][0]))
            else:
                sendHeaders(401)
                self.wfile.write('["registration failed"]'.encode())
                log("{} failed to register".format(data['email'][0]))
        elif(fileName == "authentication"):
            theEmail, success = authenticate()
            if success:
                fileName = "client.html"
                sendHeaders()
                f = open(fileName, "r", encoding="UTF-8")
                data = f.read()
                self.wfile.write(theEmail.encode())
                self.wfile.write(";".encode())
                self.wfile.write(data.encode())
                log("{} login succeeded".format(theEmail))                
            else:
                sendHeaders(401)
                self.wfile.write('["login failed"]'.encode())
                log("{} failed to login".format(theEmail))                
        else:
            def isInvalidRequest():
                if(fileName == "client.html" and queryString != "auto"): return True
                if(extension == "html" or extension == "js" or extension == "css"):
                    return False
                elif(fileName == "log"):
                    return False
                else:
                    return True
                
            extension = fileName.split(".")[-1]        
            if(extension == "png" or extension == "jpg" or extension == "gif" ):
                sendHeaders()
                f = open(fileName, "rb")
                data = f.read()
                self.wfile.write(data)
            elif(isInvalidRequest()):
                sendHeaders(404) 
            else:
                try:
                    if fileName == "log": 
                        fileName = LOG_FILENAME
                    f = open(fileName, "r", encoding="UTF-8")
                    data = f.read()
                    sendHeaders()
                    self.wfile.write(data.encode())
                except:
                    sendHeaders(404)

import server_database as sql
my_logger = setupLogging()
my_logger.debug("server started at {}".format(datetime.datetime.now()))

PORT = g.get("port")
SERVER = g.get("server")

try:
    httpd = http.server.HTTPServer((SERVER, PORT), Handler)
except OSError as e:
    print(e)
    print("server:", SERVER)
    print("port:", PORT)
    sys.exit()
    
import ssl
httpd.socket = ssl.wrap_socket(httpd.socket,
                                     server_side=True,
                                     keyfile='certs/privkey1.pem',
                                     certfile='certs/fullchain1.pem',
                                     ssl_version=ssl.PROTOCOL_TLSv1_2)

print("server:", SERVER)
print("port:", PORT)
print("database:", g.get("database"))
print("table:", g.get("table"))
print("users table:", g.get("usersTable"))
print("")
httpd.serve_forever()




