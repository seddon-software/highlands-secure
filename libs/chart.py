############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

import os
import pandas as pd
from ast import literal_eval
if __name__ == "__main__": os.chdir("..")
from database import Database
from myglobals import MyGlobals


g = MyGlobals()
db = Database()

class Chart:
    def __init__(self):
        self.refresh()
        
    def refresh(self):
        self.chartData = self.setChartData()

    def getChartData(self):
        return self.chartData
    
    def setChartData(self):
        """
        Summary of marks for each database record
        xaxis: marks
        yaxis: [section, client]
        tooltip: email
        """
        connection = db.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `{}`".format(g.get("table"))
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

            def getCompositeKeys(keyNo):
                # keys are returned sorted
                data = []
                for key in chartData:
                    data.append(key[keyNo])
                data = list(set(data))
                data.sort()
                return data

            # chartData has composite keys: (<aspect>, <client>, <email>, <guid>) 

            def getCategoriesAndToolTips():
                categories = []
                toolTips = []
                firstAspect = next(iter(chartData))[0]
                for key in chartData:
                    aspect = key[0]
                    client = key[1]
                    email = key[2]
                    if aspect == firstAspect: 
                        categories.append(client)
                        toolTips.append(email)
                return categories, toolTips
                
            def getAll():
                data = []
                for aspect in getCompositeKeys(0):
                    row = [aspect]
                    for key in chartData:
                        if key[0] == aspect:
                            row.append(int(chartData[key]))
                    data.append(row)
                return {'all' : data }
            
            def getFilteredData(_filter, keyNo):
                data = []
                for aspect in getCompositeKeys(0):
                    row = [aspect]
                    for key in chartData:
                        if key[0] == aspect and key[keyNo] == _filter:
                            row.append(int(chartData[key]))
                    data.append(row)
                return {_filter: data }

            def generateGroups():
                aspects = getCompositeKeys(0)
                groups = []
                for aspect in aspects:
                    if "*" not in aspect:
                        groups.append([aspect, aspect + '*'])
                return groups
                
            def generateResult():
                # chartData has composite keys: (<aspect>, <client>, <email>, <guid>) 
                data = {}
                data['all'] = getAll()
                for client in getCompositeKeys(1):
                    data[client] = getFilteredData(client, 1)
                for email in getCompositeKeys(2):
                    data[email] = getFilteredData(email, 2)
                categories, toolTips = getCategoriesAndToolTips()
                
                return { 'categories':categories, 'toolTips':toolTips, 'data':data, 'groups':generateGroups() }

            entries = generateResult()
        finally:
            connection.close()
        return entries    # return a dict
    
if __name__ == "__main__": 
    #   chartData is formed from
    #       radio:    a single mark
    #       checkbox: a string of marks
    #       table:    a list of marks

    chart = Chart()
    results = chart.getChartData7();
    print(type(results))
    for key in results:
        print(key, results[key])
    
    