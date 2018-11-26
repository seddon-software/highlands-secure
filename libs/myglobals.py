############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

import sys, os
import logging.handlers
import pandas as pd

if __name__ == "__main__": os.chdir("..")

class MyGlobals:
    logger = None
    logFileName = None
    
    def __init__(self):
        self.parseCommandLine()
        self.getNamesAndPasswords()
        
    def getNamesAndPasswords(self):
        global root, rootPassword, manager, managerPassword, database, table, server, port
        pd.set_option('display.width', 1000)
        table = pd.read_excel(self.excelFile, 'setup')
        table = table.drop(['COMMENTS'], axis=1)
        rootFrame = table[(table.TYPE == "user") & (table.NAME == "root")]
        managerFrame = table[(table.TYPE == "user") & (table.NAME == "manager")]
        databaseFrame = table[table.TYPE == "database"]
        hostFrame = table[table.TYPE == "host"]
        usersFrame = table[table.TYPE == "users"]
    
        self.root = rootFrame["NAME"].tolist()[0]
        self.rootPassword = rootFrame["OPTION"].tolist()[0]
        self.manager = managerFrame["NAME"].tolist()[0]
        self.managerPassword = managerFrame["OPTION"].tolist()[0]
        self.database = databaseFrame["NAME"].tolist()[0]
        self.table = databaseFrame["OPTION"].tolist()[0]
        self.server = hostFrame["NAME"].tolist()[0]
        self.port = hostFrame["OPTION"].tolist()[0]
        self.usersTable = usersFrame["OPTION"].tolist()[0]

    def setupLogging(self):
        LOG_FILENAME = "logs/{}-{}-{}-{}.log".format(
            self.get("database"), 
            self.get("table"), 
            self.get("usersTable"),
            self.get("port"))

        # Set up a specific logger with our desired output level
        my_logger = logging.getLogger('MyLogger')
        my_logger.setLevel(logging.DEBUG)
        
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1000000, backupCount=10)
        my_logger.addHandler(handler)
        MyGlobals.logger = my_logger
        MyGlobals.logFileName = LOG_FILENAME
        return self.logger

    def getLogger(self):
        return MyGlobals.logger
            
    def getLogFileName(self):
        return MyGlobals.logFileName
            
    def get(self, name):
            if name == "root": return self.root
            if name == "rootPassword": return self.rootPassword
            if name == "manager": return self.manager
            if name == "managerPassword": return self.managerPassword
            if name == "database": return self.database
            if name == "table": return self.table
            if name == "server": return self.server
            if name == "port": return self.port
            if name == "excelFile": return self.excelFile
            if name == "usersTable": return self.usersTable
            if name == "auto": return self.auto
            
    def parseCommandLine(self):
        # default excel file is "highlands.xlsx", but can be changed on command line:
        #    python server.py [excel-file]

        # check for automatic testing (must supply "-auto" as last command line arg
        lastArg = sys.argv[-1]
        if lastArg == "-auto":
            self.auto = True
        else:
            self.auto = False

        argLengthWithoutAuto = len(sys.argv)
        if self.auto: argLengthWithoutAuto -= 1
        
        if argLengthWithoutAuto > 2:
            print("Useage: python server.py [excel-file]")
            sys.exit()
        if argLengthWithoutAuto == 1:
            excelFile = "highlands.xlsx"
        else:
            excelFile = sys.argv[1].replace(".xlsx", "") + ".xlsx"
        
        if not os.path.isfile(excelFile):
            print("{} does not exist".format(excelFile))
            sys.exit()
    
        self.excelFile = excelFile

if __name__ == "__main__":
    g = MyGlobals()
    
