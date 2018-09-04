import sys, os
import pandas as pd

class MyGlobals:
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

    def parseCommandLine(self):
        # default excel file is "highlands.xlsx", but can be changed on command line:
        #    python server.py [excel-file]
        if len(sys.argv) > 2:
            print("Useage: python server.py [excel-file]")
            sys.exit()
        if len(sys.argv) == 1:
            excelFile = "highlands.xlsx"
        else:
            excelFile = sys.argv[1].replace(".xlsx", "") + ".xlsx"
        
        if not os.path.isfile(excelFile):
            print("{} does not exist".format(excelFile))
            sys.exit()
    
        self.excelFile = excelFile
