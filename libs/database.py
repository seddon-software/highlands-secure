############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

import pymysql.cursors
import os, sys
import re
import pandas as pd
from ast import literal_eval
import collections

if __name__ == "__main__": os.chdir("..")

from myglobals import MyGlobals
from excel import Excel
g = MyGlobals()
xl = Excel()

class Database:
    def __init__(self):
        pass
    
    def connect(self):
        connection = pymysql.connect(host='localhost',
                                     user=g.get("manager"),
                                     password=g.get("managerPassword"),
                                     db=g.get("database"),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    def checkIfTableExists(self):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                try:
                    sql = "SELECT * FROM `{}`".format(g.get("table"))
                    cursor.execute(sql)
                except Exception as e:
                    print("Can't fire up server")
                    print(e)
                    print("Have you run initialize_database.py?")
                    sys.exit()
        finally:
            connection.close()

    def getDatabaseResults(self):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `{}`".format(g.get("table"))
                cursor.execute(sql)
                results = cursor.fetchall()
        finally:
            connection.close()
        return results

    def createUser(self, email, password, code):
        # This routine will create a user if it doesn't exist or update the user otherwise
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                try:
                    sql = """REPLACE INTO {} SET email = '{}', password = SHA1('{}'), code = '{}'
                    """.format(g.get("usersTable"), email, password, code)
                    cursor.execute(sql)
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    print(e)
        finally:
            connection.close()

    def getPassword(self, email):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT password FROM {} WHERE email = '{}'""".format(g.get("usersTable"), email)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    
                except Exception as e:
                    connection.rollback()
                    print(e)
        finally:
            connection.close()
        
        return result['password'] if result else ""

    def getCode(self, email):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT code FROM {} WHERE email = '{}'
                    """.format(g.get("usersTable"), email)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    
                except Exception as e:
                    connection.rollback()
                    print(e)
        finally:
            connection.close()
        return result['code']

    def getField(self, fieldName, fieldValue):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                try:
                    sql = """SELECT code FROM {} WHERE email = '{}'
                    """.format(g.get("usersTable"), fieldName, fieldValue)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    
                except Exception as e:
                    connection.rollback()
                    print(e)
        finally:
            connection.close()
        return result['password']

    def printUsers(self):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `{}`".format(g.get("usersTable"))
                cursor.execute(sql)
                results = cursor.fetchall()
                for result in results:
                    print(result)
        finally:
            connection.close()

    def getRegisteredUsers(self):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `{}`".format(g.get("usersTable"))
                cursor.execute(sql)
                results = cursor.fetchall()
        finally:
            connection.close()
        users = []
        for record in results:
            email = record['email'].lower()
            managerType = xl.getManagerType(email)
            users.append([email, managerType])
        users.sort()
        users.insert(0, ["USER", "PERMISSIONS"])
        return users
        
    def getExcelData(self):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `*` FROM `{}`".format(g.get("table"))
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
                                            if k == 'piechart': theValue = int(theValue) + 1
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
        excelData = chartData.values.tolist()       # convert values to 2D list
        columnNames = list(chartData.head(0))       # get column headings
        excelData.insert(0, columnNames)            # add column names to front of 2D list
        excelData = str(excelData)                  # convert to string
        excelData = excelData.replace("'",'"')      # change single quoutes into double (for JSON)
        def convertTimestamps(s):
            pattern = r'Timestamp[(]([^)]+)[)]'
            replacement = r"\1"
            return re.sub(pattern, replacement, s)
#             excelData = convertTimestamps(excelData)
#             return excelData
        return convertTimestamps(excelData)
            
if __name__ == "__main__": 
    import json, re
    db = Database()
    results = db.getDatabaseResults()
    records = db.getRegisteredUsers()
    print(records)
    for r in results:
        print(r)
