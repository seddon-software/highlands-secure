import pandas as pd
from ast import literal_eval
from database import Database
from myglobals import MyGlobals

g = MyGlobals()
db = Database()

class Radio:
    def __init__(self):
        self.refresh()
        
    def refresh(self):
        self.pieChartData = self.setPieChartData()
        self.pieChartData2 = self.setPieChartData2()
    
    def getPieChartData(self):
        return self.pieChartData
    
    def getPieChartData2(self):
        return self.pieChartData2
    
    def setPieChartData(self):
        ''' this routine returns pie chart data for the query:
                frequencies for all questions
                
            results are returned as a 2D list in the form:
                [ [frequencies for all questions-1], [frequencies for all questions-2], ...]
        '''
        results = db.getDatabaseResults()
        
        chartData = []
        for row in results:
            arr = []
            keyValuePairs = literal_eval(row['result'])
            for pair in keyValuePairs:
                if 'radio' in pair:
                    arr.append((pair["radio"]["selection"],pair["radio"]["optionCount"]))
            chartData.append(arr)    
        chartData = pd.DataFrame(chartData)
        
        def seriesAsFrequencies(series):
            # pd.value_count doesn't return anything for missing indices and sorts highest frequency first
            # so convert to a list in order including zero counts
            optionCount = int(series.index.values.tolist()[0][1])
            frequencies = [0]*optionCount
            for (value,size),count in series.iteritems():   #@UnusedVariable
                frequencies[int(value)] = count
            return frequencies
            
        recordCount = chartData.shape[1]
        frequencies = []
        for i in range(recordCount):
            series = pd.value_counts(chartData[i])
            frequencies.append(seriesAsFrequencies(series))
        chartData = pd.DataFrame(frequencies)
        chartData.fillna(-1, inplace=True)
        chartData = chartData.astype(int)
    
        return pd.DataFrame(chartData).values.tolist()

    def setPieChartData2(self):
        ''' this routine returns pie chart data for three types of query:
                all: frequencies for all questions
                email: frequencies for questions filtered by email
                client: frequencies for questions filtered by client
            results are returned as a dictionary of 2D arrays in the form:
                { 'all': <frequencies for all questions>,
                  'email-1': [ [frequencies for questions-1], [frequencies for questions-2], ...],
                  'email-2': [ [frequencies for questions-1], [frequencies for questions-2], ...],
                  ...
                  'client-1': [ [frequencies for questions-1], [frequencies for questions-2], ...],
                  'client-2': [ [frequencies for questions-1], [frequencies for questions-2], ...],
                  ...
                }
        '''
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
    
        def getClient(row):
            keyValuePairs = literal_eval(row['result'])
            for pair in keyValuePairs:
                if 'client' in pair:
                    return pair['client']['name']
            raise("client missing from record")
        
        def getEmail(row):
            return row['email']
        
        def seriesAsFrequencies(series):
            # pd.value_count doesn't return anything for missing indices and sorts highest frequency first
            # so convert to a list in order including zero counts
            optionCount = int(series.index.values.tolist()[0][1])
            frequencies = [0]*optionCount
            for (value,size),count in series.iteritems():   #@UnusedVariable
                frequencies[int(value)] = count
            return frequencies
            
        def calculateFrequencies(chartData):
            recordCount = chartData.shape[1]
            frequencies = []
            for i in range(recordCount):
                series = pd.value_counts(chartData[i])
                frequencies.append(seriesAsFrequencies(series))
            chartData = pd.DataFrame(frequencies)
            chartData.fillna(-1, inplace=True)
            chartData = chartData.astype(int)
            return chartData
        
        def getData(results, filterType = "", filter_ = "all"):
            chartData = []
            for row in results:
                if filterType == 'email': 
                    if getEmail(row) != filter_: continue
                if filterType == 'client': 
                    if getClient(row) != filter_: continue
                arr = []
                keyValuePairs = literal_eval(row['result'])
                for pair in keyValuePairs:
                    if 'radio' in pair:
                        arr.append((pair["radio"]["selection"],pair["radio"]["optionCount"]))
                chartData.append(arr)
            return chartData
             
        def gatherPieInformation():
            def convertToList(key):
                chartData = pd.DataFrame(pie[key])
                chartData = calculateFrequencies(chartData)
                return pd.DataFrame(chartData).values.tolist()

            results = db.getDatabaseResults()
            emails = getEmails(results)
            clients = getClients(results)
            pie = {}
            pie['all'] = getData(results)
            for email in emails:
                pie[email] = getData(results, 'email', email)
            for client in clients:
                pie[client] = getData(results, 'client', client)
    
            allPies = {}
            for key in pie:
                allPies[key] = convertToList(key)
            return allPies

        return gatherPieInformation()
