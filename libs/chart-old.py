import pandas as pd
from ast import literal_eval
from database import Database
from myglobals import MyGlobals

g = MyGlobals()
db = Database()

class Chart:
    def __init__(self):
        self.refresh()
        
    def refresh(self):
        self.chartData = self.setChartData()
        self.chartData2 = self.setChartData2()
        self.chartData3 = self.setChartData3()
        
    def getChartData(self):
        return self.chartData
    
    def getChartData2(self):
        return self.chartData2
    
    def getChartData3(self):
        return self.chartData3
    
    def setChartData(self):
        """
        Summary of marks for each database record
        xaxis: marks
        yaxis: [section, client]
        tooltip: email
        """
#         try:
#             client
#         except NameError:
#             client = ""
        connection = db.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `*` FROM `{}`".format(g.get("table"))
                cursor.execute(sql)
                results = cursor.fetchall()
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
                    
                    for pair in keyValuePairs:
                        def addItem(section, marks): # last parameter must be a list
                            for mark in marks:
                                data = {
                                        'guid'   : guid,
                                        'client' : client,
                                        'section': section,
                                        'email'  : email,
                                        'marks'  : mark
                                       }
                                return chartData.append(data, ignore_index=True)
                        # marks are presented differently in radio, checkbox and table entries:
                        #   radio:    a single mark which needs to be put in a list
                        #   checkbox: a string of marks which need to be split() into a list
                        #   table:    marks are already a list
                        if 'radio' in pair:
                            chartData = addItem(pair["radio"]["section"], [pair["radio"]["marks"]])
                        if 'checkbox' in pair:
                            chartData = addItem(pair["checkbox"]["section"], pair["checkbox"]["marks"].split())
                        if 'table' in pair:
                            chartData = addItem(pair["table"]["section"], pair["table"]["marks"])
            chartData[['marks']] = chartData[['marks']].apply(pd.to_numeric)
            chartData = chartData.groupby(['section', 'client','email','guid']).sum()
            chartData = chartData.to_dict()['marks']
            chartData = {"{},{} <{}>,{}".format(compositeKey[0], compositeKey[1], compositeKey[2], compositeKey[3]):chartData[compositeKey] for compositeKey in chartData}
        finally:
            connection.close()
        return chartData    # return a dict

    def setChartData2(self):
        """
        Summary of marks grouped by {section,client} pairs
        xaxis: marks
        yaxis: [section, client]
        """
#         try:
#             client
#         except NameError:
#             client = ""
        connection = db.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `*` FROM `{}`".format(g.get("table"))
                cursor.execute(sql)
                results = cursor.fetchall()
                chartData = pd.DataFrame(columns=['client','section','marks'])
                if not results: return ""
                
                for row in results:
                    keyValuePairs = literal_eval(row['result'])
    
                    for pair in keyValuePairs:
                        if "client" in pair: 
                            d = pair["client"]
                            client = d["name"]
                            break
                    
                    # not used at present
                    for pair in keyValuePairs:
                        if "email" in pair: 
                            d = pair["email"]
                            email = d["name"]
                            break
                    
                    for pair in keyValuePairs:
                        def addItem(section, marks): # last parameter must be a list
                            for mark in marks:
                                data = {
                                        'client' : client,
                                        'section': section,
                                        'email': email,
                                        'marks'  : mark
                                       }
                                return chartData.append(data, ignore_index=True)
                        # marks are presented differently in radio, checkbox and table entries:
                        #   radio:    a single mark which needs to be put in a list
                        #   checkbox: a string of marks which need to be split() into a list
                        #   table:    marks are already a list
                        if 'radio' in pair:
                            chartData = addItem(pair["radio"]["section"], [pair["radio"]["marks"]])
                        if 'checkbox' in pair:
                            chartData = addItem(pair["checkbox"]["section"], pair["checkbox"]["marks"].split())
                        if 'table' in pair:
                            chartData = addItem(pair["table"]["section"], pair["table"]["marks"])
            chartData[['marks']] = chartData[['marks']].apply(pd.to_numeric)  
            chartData = chartData.groupby(['section', 'client']).sum()
            chartData = chartData.to_dict()['marks']
            chartData = {"{},{}".format(compositeKey[0], compositeKey[1]):chartData[compositeKey] for compositeKey in chartData}
        finally:
            connection.close()
        return chartData
    
    def setChartData3(self):
        """
        Summary of marks grouped by {section,client,email} triples
        xaxis: marks
        yaxis: [section, client, email]
        """
#         try:
#             client
#         except NameError:
#             client = ""
        connection = db.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `*` FROM `{}`".format(g.get("table"))
                cursor.execute(sql)
                results = cursor.fetchall()
                
                chartData = pd.DataFrame(columns=['client','section','email','marks'])
                
                for row in results:
                    keyValuePairs = literal_eval(row['result'])
    
                    for pair in keyValuePairs:
                        if "client" in pair: 
                            d = pair["client"]
                            client = d["name"]
                            break
                    
                    # not used at present
                    for pair in keyValuePairs:
                        if "email" in pair: 
                            d = pair["email"]
                            email = d["name"]
                            break
                    
                    for pair in keyValuePairs:
                        def addItem(section, marks): # last parameter must be a list
                            for mark in marks:
                                data = {
                                        'client' : client,
                                        'section': section,
                                        'email': email,
                                        'marks'  : mark
                                       }
                                return chartData.append(data, ignore_index=True)
                        # marks are presented differently in radio, checkbox and table entries:
                        #   radio:    a single mark which needs to be put in a list
                        #   checkbox: a string of marks which need to be split() into a list
                        #   table:    marks are already a list
                        if 'radio' in pair:
                            chartData = addItem(pair["radio"]["section"], [pair["radio"]["marks"]])
                        if 'checkbox' in pair:
                            chartData = addItem(pair["checkbox"]["section"], pair["checkbox"]["marks"].split())
                        if 'table' in pair:
                            chartData = addItem(pair["table"]["section"], pair["table"]["marks"])
            chartData[['marks']] = chartData[['marks']].apply(pd.to_numeric)  
            chartData = chartData.groupby(['section', 'client', 'email']).sum()
            chartData = chartData.to_dict()['marks']
            chartData = {"{},{},{}".format(compositeKey[0], compositeKey[1], compositeKey[2]):chartData[compositeKey] for compositeKey in chartData}
        finally:
            connection.close()
        return chartData
