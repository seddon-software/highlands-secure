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
import uuid

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


UUID = str(uuid.uuid4())
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
            
        def sendHeaders(**d):
            code = d["code"] if "code" in d else 200
            mimeType = d["mimeType"] if "mimeType" in d else getMimeType()
            self.send_response(code)
            self.send_header("Content-type", mimeType)
            self.end_headers()

        def sendHeaders2(code=200):
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
                        return email, "invalid password, please try again"
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
        managerMode = queryString == UUID       # charts are only available if query string contains UUID
        fileName = fileName[1:]  # remove leading '/'

        # make login.html the default pages
        if fileName == "": fileName = "login.html"
        if fileName == "login.html": log("website accessed")
        data = urllib.parse.parse_qs(queryString)

        try:
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
                if not managerMode: raise Exception()
                sendHeaders()
                jsonString = json.dumps(sql.getEmailsAndClients())
                jsonAsBytes = jsonString.encode("UTF-8")
                self.wfile.write(jsonAsBytes)
            elif(fileName == "chart-data"):
                if not managerMode: raise Exception()
                sendHeaders()
                jsonString = json.dumps(chart.getChartData())
                jsonAsBytes = jsonString.encode("UTF-8")
                self.wfile.write(jsonAsBytes)
            elif(fileName == "table-data"):
                if not managerMode: raise Exception()
                sendHeaders()
                jsonString = json.dumps(table.getTableData())
                jsonAsBytes = jsonString.encode("UTF-8")
                self.wfile.write(jsonAsBytes)
            elif(fileName == "checkbox-data"):
                if not managerMode: raise Exception()
                sendHeaders()
                jsonString = json.dumps(checkbox.getCheckboxData())
                jsonAsBytes = jsonString.encode("UTF-8")
                self.wfile.write(jsonAsBytes)
            elif(fileName == "scatter-data"):
                if not managerMode: raise Exception()
                sendHeaders()
                jsonString = json.dumps(scatter.getScatterChartData())
                jsonAsBytes = jsonString.encode("UTF-8")
                self.wfile.write(jsonAsBytes)
            elif(fileName == "piechart-data"):
                if not managerMode: raise Exception()
                sendHeaders()   
                jsonString = json.dumps(radio.getPieChartData())
                jsonAsBytes = jsonString.encode("UTF-8")
                self.wfile.write(jsonAsBytes)
            elif(fileName == "piechart-questions-options"):
                if not managerMode: raise Exception()
                sendHeaders()
                jsonString = json.dumps(sql.getPieChartQuestionsAndOptions())
                jsonAsBytes = jsonString.encode("UTF-8")
                self.wfile.write(jsonAsBytes)
            elif(fileName == "excel-data"):
                if not managerMode: raise Exception()
#                 self.send_response(200)
#                 self.send_header("Content-type", "application/json")
#                 self.end_headers()
                sendHeaders(mimeType="application/json")
                jsonString = json.dumps(db.getExcelData())
                jsonAsBytes = jsonString.encode("UTF-8")
                self.wfile.write(jsonAsBytes)
            elif(fileName == "registered-users"):
                if not managerMode: raise Exception()
                sendHeaders()
                jsonString = json.dumps(db.getRegisteredUsers())
                jsonAsBytes = jsonString.encode("UTF-8")
                self.wfile.write(jsonAsBytes)
            elif(fileName == "system-logs"):
                if not managerMode: raise Exception()
                reply = {}
                for fileName in ("syslog", "alternatives.log", "auth.log", "dpkg.log", "fontconfig.log", "mail.log", "vsftpd.log"):
                    fullName = f"/var/log/{fileName}"
                    try:
                        f = open(fullName, "r", encoding="UTF-8")
                        data = f.read()
                    except:
                        data = f"{fileName}: not available"
                    reply[fileName] = data
                sendHeaders()
                reply = json.dumps(reply)
                self.wfile.write(str(reply).encode())
            elif(fileName == "change-password"):
                email = data['email'][0]
                oldPassword1hash = db.getPassword(email)
                if oldPassword1hash == "":      # not registered
                    sendHeaders(code=401)
                    message = "change password attempted for unregistered email: {}".format(email);
                    self.wfile.write(message.encode())
                    log(message)
                else:
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
                # check for invalid emails and invalid email domains
                invalidDomain = "Please use a business email.  You won't be able to register using the email you entered below"
                email = data['email'][0]
                if xl.getDenyDomains(email):
                    sendHeaders(code=401)
                    self.wfile.write(invalidDomain.encode())
                    log("registration rejected for {}".format(email))
                else:    
                    sendHeaders()
                    code = generateCode()
                    sendCodeInEmail(email, code)
                    db.createUser(email, "", code)
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
                    sendHeaders(code=401)
                    self.wfile.write('["registration failed"]'.encode())
                    log("{} failed to register".format(data['email'][0]))
            elif(fileName == "authentication"):
                theEmail, response = authenticate()
                if response == "valid":
                    fileName = "client.html"
#                     self.send_response(200)
#                     self.send_header("Content-type", "application/json")
#                     self.end_headers()
                    sendHeaders(mimeType="application/json")
                    managerType = xl.getManagerType(theEmail)
                    f = open(fileName, "r", encoding="UTF-8")
                    data = f.read()
                    reply = {}
                    reply["uuid"] = UUID
                    reply["email"] = theEmail
                    reply["manager-type"] = managerType
                    reply["source"] = data
                    reply = json.dumps(reply)
                    self.wfile.write(str(reply).encode())
                    log("{} login succeeded".format(theEmail))                
                else:
                    sendHeaders(401)
                    self.wfile.write('["login failed"]'.encode())
                    log("{} failed to login".format(theEmail))                
            else:
                def isInvalidRequest():
                    # check for automatic testing
                    if fileName == "client.html": 
                        return not g.get("auto")
                    elif(extension == "html" or extension == "js" or extension == "css"):
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
                    sendHeaders(code=404) 
                else:
                    try:
                        if fileName == "log": 
                            if not managerMode: raise Exception()
                            fileName = LOG_FILENAME
                        f = open(fileName, "r", encoding="UTF-8")
                        data = f.read()
                        sendHeaders()
                        self.wfile.write(data.encode())
                    except:
                        sendHeaders(code=404)
        except:
            sendHeaders(code=403)    

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
print("spreadsheet:", g.get("excelFile"))
if(g.get("auto")): print("automatic testing")
print("")
httpd.serve_forever()




