############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

# testing GIT

import os
import pandas as pd
from ast import literal_eval
if __name__ == "__main__": os.chdir("..")
from database import Database
from myglobals import MyGlobals
from excel import Excel
from server_database import getResult

g = MyGlobals()
db = Database()
xl = Excel()

class Coach:
    def getAssessment(self):
        return getResult("chris@def.com")
    
    def getAnswers(self, email):
        connection = db.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `{}`".format(g.get("table"))
                cursor.execute(sql)
                results = cursor.fetchall()
        except:
            print("oops")

        chartData = pd.DataFrame(columns=['guid', 'client','section','email','marks'])
        
        if(len(results) == 0): return {}    # return empty dict if no records found
        for row in results:
            guid = row['guid']
            keyValuePairs = literal_eval(row['result'])

            for pair in keyValuePairs:
                if "client" in pair: 
                    d = pair["client"]
                    client = d["name"]
                    break
            
            for pair in keyValuePairs:
                if "email" in pair: 
                    d = pair["email"]
                    email = d["name"]
                    break
                    

              

if __name__ == "__main__":
    c = Coach()
    print(c.getAnswers("chris@def.com"))

