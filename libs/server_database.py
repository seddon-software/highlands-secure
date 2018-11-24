############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

import pandas as pd
import uuid
import datetime
import os
from ast import literal_eval

if __name__ == "__main__": 
    os.chdir("..")

from database import Database
from myglobals import MyGlobals
from excel import Excel

db = Database()
g = MyGlobals()
xl = Excel()

def saveResults(results, headers):
    connection = db.connect()
    try:
        resultsAsString = ','.join(str(e) for e in results)
        
        resultsAsTuple = literal_eval(resultsAsString)
        email = ""
        for keyValuePair in resultsAsTuple:
            if "email" in keyValuePair: 
                d = keyValuePair["email"]
                email = d["name"]
                break
            
        with connection.cursor() as cursor:
            # Create a new record
            sql = """INSERT INTO `{}` (`guid`, `timestamp`, `email`, `headers`, `result`) 
                               VALUES (   %s,          %s,      %s,      %s,       %s)""".format(g.get("table"))
            guid = str(uuid.uuid4())
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("**** {} ****".format(len(resultsAsString)))
            print("**** {} ****".format(resultsAsString))
            cursor.execute(sql, (guid, timestamp, email, str(headers), resultsAsString))
        # connection is not autocommit by default. So you must commit to save your changes.
        connection.commit()    
        print("1 record committed")
    except Exception as e:
        print("rollback")
        print(e)
        connection.rollback()
    finally:
        connection.close()

def printResults():
    db = Database()
    results = db.getDatabaseResults()
    for row in results:
        print(row)

def getResult(email):
    db = Database()
    results = db.getDatabaseResults()
    for row in results:
        if row['email'] == email: return row
    return None

def getPieChartQuestionsAndOptions():
    questions = xl.filterQuestions("radio")
    options = xl.filterOptions("radio")
    questionsAndOptions = pd.concat([questions, options], axis=1)
    return questionsAndOptions.values.tolist()

def getTableQuestionsAndOptions():
    questions = xl.filterQuestions("table")
    options = xl.filterOptions("table")
    questionsAndOptions = pd.concat([questions, options], axis=1)
    return questionsAndOptions.values.tolist()
    

def getEmailsAndClients():
    def getEmails(results):
        emails = []
        for row in results:
            emails.append(row['email'])
        return list(set(emails))  # pick out unique emails
    
    def getClients(results):
        clients = []
        for row in results:
            keyValuePairs = literal_eval(row['result'])
            for pair in keyValuePairs:
                if 'client' in pair:
                    clients.append(pair['client']['name'])
        return list(set(clients))  # pick out unique clients

    results = db.getDatabaseResults()
    emails = getEmails(results)
    clients = getClients(results)
    return sorted(emails), sorted(clients)


if __name__ == "__main__":
    print(getResult("chris@def.com"))
    