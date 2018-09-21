############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

import datetime
import pymysql.cursors
import pandas as pd
import sys, os
from ast import literal_eval
import collections


def connect():
    connection = pymysql.connect(host='localhost',
                                 user=manager,
                                 password=managerPassword,
                                 db=database,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def getNamesAndPasswords():
    pd.set_option('display.width', 1000)
    table = pd.read_excel(excelFile, 'setup')
    rootFrame = table[(table.TYPE == "user") & (table.NAME == "root")]
    managerFrame = table[(table.TYPE == "user") & (table.NAME == "manager")]
    databaseFrame = table[table.TYPE == "database"]
    hostFrame = table[table.TYPE == "host"]
 
    root = rootFrame["NAME"].tolist()[0]
    rootPassword = rootFrame["OPTION"].tolist()[0]
    manager = managerFrame["NAME"].tolist()[0]
    managerPassword = managerFrame["OPTION"].tolist()[0]
    database = databaseFrame["NAME"].tolist()[0]
    table = databaseFrame["OPTION"].tolist()[0]
    server = hostFrame["NAME"].tolist()[0]
    port = hostFrame["OPTION"].tolist()[0]
    return [root, rootPassword, manager, managerPassword, database, table, server, port]

def getExcelData():
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `*` FROM `{}`".format(table)
            cursor.execute(sql)
            results = cursor.fetchall()
 
            resultsArray = []
            for row in results:
                orderedDict = collections.OrderedDict()
                
                section = ""
                for key in row:
                    if key == 'result':
                        keyValuePairs = literal_eval(row['result'])
                        for key in keyValuePairs:
                            for k in key:   # should only be 1 key
                                entry = key[k]
                                question = entry['question']
                                for key in entry:
                                    theKey = "{}-{}".format(question, key)
                                    theValue = entry[key]
                                    
                                    if key == 'question': continue
                                    if key == 'optionCount': continue
                                    if key == 'section': 
                                        if (theValue == section): 
                                            continue
                                        else:
                                            section = theValue
                                    if key == 'selection':
                                        if k == 'radio': theValue = int(theValue) + 1
                                        if k == 'table': pass # theValue is correct
                                        if k == 'table2':  pass # theValue is correct
                                        if k == 'checkbox':  pass # theValue is correct
                                    orderedDict[theKey] = theValue
                                pass
                    else:
                        orderedDict[key] = row[key]
                resultsArray.append(orderedDict)
        chartData = pd.DataFrame(resultsArray)
    finally:
        connection.close()
    return chartData

def parseCommandLine():
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

    return excelFile
    
excelFile = parseCommandLine()


root, rootPassword, manager, managerPassword, database, table, server, port = getNamesAndPasswords()
today = datetime.datetime.now().strftime("%Y-%m-%d")
outFile = "spreadsheets/{}_{}_{}.xlsx".format(database, table, today)
getExcelData().to_excel(outFile, index = False)
print("MySql database table exported to Excel [{}]".format(outFile))
