debug = True
import cherrypy
import json
#from cherrypy.process.plugins import Daemonizer

import datetime
import os
import ssl
import sys
import random
import hashlib
import string
from functools import partial
import urllib.parse
import uuid
import re
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail



def switchOffCheeryPyLogging(cherrypy):
    access_log = cherrypy.log.access_log
    for handler in tuple(access_log.handlers):
        access_log.removeHandler(handler)

class Root(object):
    def do_POST(self):
        contentLength = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(contentLength))
        results = json.loads(rawbody)
        headers = cherrypy.request.headers
        headersAsString = ""
        for key in headers:
            headersAsString += f"{key}:{headers[key]}\n"

        sql.saveResults(results, headersAsString)
        radio.refresh()
        chart.refresh()
        return

    def do_GET(self, args, kwargs):
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
            cherrypy.response.status = code
            cherrypy.response.headers['Content-type'] = mimeType

        def hashPassword(password):
            return hashlib.sha1(password.encode()).hexdigest()
                    
        def authenticate():
            email = None
            if 'Authorization' in cherrypy.request.headers:
                email, password1 = cherrypy.request.headers['Authorization'].split("+")

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
                SENDGRID_API_KEY = xl.getSendgridAPI_KEY()
                if not SENDGRID_API_KEY: return 500
                sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
                from_email = Email(xl.getEmailFrom())
                to_email = Email(email)
                subject = xl.getEmailSubject()
                body_part1, body_part2 = xl.getEmailBody()
                content = Content("text/html", "{} {} {}".format(body_part1, code, body_part2))
                
                mail = Mail(from_email, subject, to_email, content)
                response = sg.client.mail.send.post(request_body=mail.get())
                return response.status_code
            except:
                log("send email failed for {}".format(email))
                
        def generateCode():
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        def log(message):
            my_logger.debug("{}: ({}) {}".format(datetime.datetime.now(), cherrypy.request.remote.ip, message))

        def parseInputUrl():
            fileName = "/".join(args)
            
            # make login.html the default pages
            if fileName == "": fileName = "login.html"
            if fileName == "login.html": log("website accessed")
            
            queryDictionary = kwargs
            if "uuid" in queryDictionary:
                theUuid = queryDictionary["uuid"]
            else:
                theUuid = "0"
            return fileName, theUuid, queryDictionary

        def doCompletedAssessments(queryDictionary, writeToClient):
            # must pass email as a parameter
            email = queryDictionary['email']
            if isAdmin() or isManager():
                fn = partial(Coach.getRecordSummaryByEmail, coach, None)
            else:
                fn = partial(Coach.getRecordSummaryByEmail, coach, email)
            return writeToClient(fn, security="other", mimeType="application/json")

        def doGenerateReport():
            match = re.search(guidPattern, fileName)
            guid = match.group(1)
            pdf = coach.generatePdf(guid)
            cherrypy.response.status = 200
            cherrypy.response.headers["Content-type"] = 'application/pdf'
            cherrypy.response.headers["Content-Disposition"] = 'attachment; filename="report.pdf"' 
            return pdf

        def doDownloadPdf():        # view PDF inline
            guid = queryDictionary['pdf']
            pdf = coach.generatePdf(guid)
            cherrypy.response.status = 200
            cherrypy.response.headers["Content-type"] = 'application/pdf'
            cherrypy.response.headers["Content-length"] = str(len(pdf))
            cherrypy.response.headers["Content-Disposition"] = 'inline; filename="report.pdf"' 
            return pdf
        
        def doSystemLogs():
            if not isAdmin():
                raise Exception()
            reply = {}
            for fileName in "syslog", "alternatives.log", "auth.log", "dpkg.log", "fontconfig.log", "mail.log", "vsftpd.log":
                fullName = "/var/log/{fileName}"
                try:
                    f = open(fullName, "r", encoding="UTF-8")
                    data = f.read()
                except:
                    data = f"<p><p>{fileName}: not available"
                reply[fileName] = data
            
            sendHeaders()
            reply = json.dumps(reply)
            return str(reply).encode()


        def doChangePassword():
            email = queryDictionary['email']
            oldPassword1hash = db.getPassword(email)
            if oldPassword1hash == "": # not registered
                sendHeaders(code=401)
                message = "change password attempted for unregistered email: {}".format(email)
                log(message)
                return message.encode()
                
            else:
                oldPassword2 = queryDictionary['oldPassword']
                oldPassword2hash = hashPassword(oldPassword2)
                if oldPassword1hash == oldPassword2hash:
                    sendHeaders()
                    db.createUser(queryDictionary['email'], queryDictionary['newPassword'], "")
                    log("password updated for {}".format(queryDictionary['email']))
                    return '["password changed"]'.encode()
                else:
                    sendHeaders(code=401)
                    log("password update failed for {}".format(queryDictionary['email']))
                    return '["incorrect password"]'.encode()
    
        def doStartRegistration():
            def sendRegistrationDetails(code, message, logMessage):
                sendHeaders(code=code)
                log(logMessage)
                return message.encode()

            email = queryDictionary['email']
            code = generateCode()
            msgInvalidDomain = "Please use a business email.  You won't be able to register using the email you entered below"
            logInvalidDomain = f"registration rejected for {email}"
            msgRegistrationCodeSent = '["registration code sent"]'
            logRegistrationCodeSent = f"registration code {code} sent to {email}"
            msgInternalServerError = 'internal server error - please contact Highlands'
            logInternalServerError = "internal server error: SENDGRID_API_KEY missing from setup tab on spreadsheet"
            msgDomainNotAllowed = "The domain your are using for your email is not a permitted domain"
            logDomainNotAllowed = "domain invalid - not on white list"

            # check for invalid emails and invalid and valid email domains
            mode = xl.getAllowOrDenyMode()
            if mode == 'deny' and xl.getDenyDomains(email):
                sendRegistrationDetails(401, msgInvalidDomain, logInvalidDomain)
            elif mode == 'allow' and not xl.getAllowDomains(email):
                sendRegistrationDetails(401, msgDomainNotAllowed, logDomainNotAllowed)
            else:
                response = sendCodeInEmail(email, code)
                if response == 202:
                    db.createUser(email, "", code)
                    sendRegistrationDetails(200, msgRegistrationCodeSent, logRegistrationCodeSent)
                else:
                    sendRegistrationDetails(response, msgInternalServerError, logInternalServerError)
            # the returned data is ignored on success, but used as an error message on failure
            return f'["{msgInternalServerError}"]'.encode()
    
        def doCompleteRegistration():
            code1 = db.getCode(queryDictionary['email'])
            code2 = queryDictionary['code']
            if code1 == code2:
                sendHeaders()
                db.createUser(queryDictionary['email'], queryDictionary['password'], queryDictionary['code'])
                log("{} is now registered".format(queryDictionary['email']))
                return '["registration succeeded"]'.encode()
            else:
                sendHeaders(code=401)
                log("{} failed to register".format(queryDictionary['email']))
                return '["registration failed"]'.encode()
    
        def doAuthenticate():
            theEmail, response = authenticate()
            if response == "valid":
                fileName = "client.html"
                sendHeaders(mimeType="application/json")
                managerType = xl.getManagerType(theEmail)
                f = open(fileName, "r", encoding="UTF-8")
                data = f.read()
                reply = {}
                if managerType == "admin":
                    reply["uuid"] = UUID1
                elif managerType == "manager":
                    reply["uuid"] = UUID2
                else:
                    reply["uuid"] = UUID3
                reply["email"] = theEmail
                reply["manager-type"] = managerType
                reply["source"] = data
                reply = json.dumps(reply)
                log("{} login succeeded".format(theEmail))
                return str(reply).encode()
                
            else:
                sendHeaders(code=401)
                log("{} failed to login".format(theEmail))
                return '["login failed"]'.encode()
                


        def doSendRegularFiles(fileName):
            def isInvalidRequest():
                # check for automatic testing
                if fileName == "client.html": 
                    return not g.get("auto")
                elif(extension == "html" or extension == "js" or extension == "css" or extension == "pdf"):
                    return False
                elif(fileName == "log"):
                    return False
                else:
                    return True

            extension = fileName.split(".")[-1]
            if (extension == "png" or extension == "jpg" or extension == "gif" or extension == "ico"):
                sendHeaders()
                f = open(fileName, "rb")
                data = f.read()
                return data
            elif (isInvalidRequest()):
                sendHeaders(code=404)
            else:
                try:
                    if fileName == "log":
                        if not (isAdmin() or isManager()):
                            raise Exception()
                        fileName = g.getLogFileName()
                    f = open(fileName, "r", encoding="UTF-8")
                    data = f.read()
                    sendHeaders()
                    return data
                except:
                    sendHeaders(code=404)
    
        def filesToBeIgnored(fileName):
#            ignore = ["favicon.ico",
            ignore = ["apple-touch-icon.png",
                      "apple-touch-icon-precomposed.png",
                      "apple-touch-icon-152x152.png",
                      "apple-touch-icon-152x152-precomposed.png",
                      "apple-touch-icon.png",
                      "apple-touch-icon-precomposed.png",
                      "apple-touch-icon-152x152.png",
                      "apple-touch-icon-152x152-precomposed.png"]
            return fileName in ignore
        
        def isAdmin():   return theUuid == UUID1
        def isManager(): return theUuid == UUID2
        def isOther():   return theUuid == UUID3
        
        def writeToClient(method, security="assessment", mimeType=None):
                if   security == "admin"   and not (isAdmin()):
                    raise Exception()
                elif security == "manager" and not (isAdmin() or isManager()):
                    raise Exception()
                elif security == "other"   and not (isAdmin() or isManager() or isOther()):
                    raise Exception()
            
                if mimeType:
                    sendHeaders(mimeType=mimeType)
                else:
                    sendHeaders()
                try:
                    jsonString = json.dumps(method())
                    jsonAsBytes = jsonString.encode("UTF-8")
                    return jsonAsBytes
                except Exception as e:
                    print(e)
                    raise e
        try:
            fileName, theUuid, queryDictionary = parseInputUrl()
            if(filesToBeIgnored(fileName)):
                sendHeaders()
                return
            elif(fileName == "questions"):                  return writeToClient(xl.getQuestions)
            elif(fileName == "options"):                    return writeToClient(xl.getOptions)
            elif(fileName == "emails-and-clients"):         return writeToClient(sql.getEmailsAndClients, security="manager")
            elif(fileName == "chart-data"):                 return writeToClient(chart.getChartData, security="manager")
            elif(fileName == "table-data"):                 return writeToClient(table.getTableData, security="manager")           
            elif(fileName == "checkbox-data"):              return writeToClient(checkbox.getCheckboxData, security="manager")
            elif(fileName == "scatter-data"):               return writeToClient(scatter.getScatterChartData, security="manager")
            elif(fileName == "piechart-data"):              return writeToClient(radio.getPieChartData, security="manager")
            elif(fileName == "piechart-questions-options"): return writeToClient(sql.getPieChartQuestionsAndOptions, security="manager")
            elif(fileName == "excel-data"):                 return writeToClient(db.getExcelData, security="admin", mimeType="application/json")
            elif(fileName == "registered-users"):           return writeToClient(db.getRegisteredUsers, security="admin")
            elif(fileName == "completed-assessments"):      return doCompletedAssessments(queryDictionary, writeToClient)
            elif(re.search(guidPattern, fileName)):         return doGenerateReport()
            elif(fileName == "download-pdf"):               return doDownloadPdf()
            elif(fileName == "system-logs"):                return doSystemLogs()
            elif(fileName == "change-password"):            return doChangePassword()
            elif(fileName == "start-registration"):         return doStartRegistration()
            elif(fileName == "complete-registration"):      return doCompleteRegistration()
            elif(fileName == "authentication"):             return doAuthenticate()                
            else:                                           
                return doSendRegularFiles(fileName)
        except:
            my_logger.error(f"**** Can't download {fileName}")
            sendHeaders(code=403)    

    @cherrypy.expose
    def default(self, *args, **kwargs):
        method = cherrypy.request.method
        if method == "GET": 
            return self.do_GET(args, kwargs)
        if method == "POST": 
            self.do_POST()

sys.path.append("libs")
from myglobals import MyGlobals
g = MyGlobals()
PORT = g.get("port")
SERVER = g.get("server")

from cherrypy.process.plugins import Daemonizer

if not debug:
    d = Daemonizer(cherrypy.engine)
    d.subscribe()
cherrypy.config.update(
    { 'server.socket_port': PORT,
      'engine.autoreload.on' : False,
      'environment': 'embedded',
      'server.socket_host': SERVER,
      'server.ssl_certificate':'certs/fullchain1.pem',
      'server.ssl_private_key':'certs/privkey1.pem'
    } )


# my libraries
from checkbox import Checkbox
from scatter import Scatter
from piechart import Radio
from chart import Chart
from excel import Excel
from table import Table
from database import Database
from coach import Coach
import server_database as sql


UUID1 = str(uuid.uuid4())
UUID2 = str(uuid.uuid4())
UUID3 = str(uuid.uuid4())
guidPattern = r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})[.]pdf$"
checkbox = Checkbox()
scatter = Scatter()
radio = Radio()
chart = Chart()
xl = Excel()
table = Table()
db = Database()
coach = Coach()
if not debug:
    switchOffCheeryPyLogging(cherrypy)
my_logger = g.setupLogging()
my_logger.debug("server started at {}".format(datetime.datetime.now()))


print("cherrypy server:", SERVER)
print("port:", PORT)
print("database:", g.get("database"))
print("table:", g.get("table"))
print("users table:", g.get("usersTable"))
print("spreadsheet:", g.get("excelFile"))
if(g.get("auto")): print("automatic testing")
print("")

# Note:
#
# If you load a module in the current directory, and the current directory isn't in sys.path, you'll get an absolute path. 
# If you load a module in the current directory, and the current directory is in sys.path, you'll get a relative path.

cherrypy.quickstart(Root(), '/',
    {
        '/favicon.ico': 
        {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client/images/favicon.ico')
#            'tools.staticfile.filename': 'client/images/favicon.ico'
#            'tools.staticfile.filename': os.path.join(os.path.dirname(__file__), '/client/images/favicon.ico')
        }
    }
)
