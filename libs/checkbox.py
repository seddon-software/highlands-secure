import pandas as pd
from ast import literal_eval
#import server_excel as xl
from database import Database
from excel import Excel

xl = Excel()

class Checkbox:
    def __init__(self):
        pass
    
    def getCheckboxData(self):
        '''
        var checkboxData = [
                'number':36,
                'question':<the text of the question>,        
                'data': {
                    'all': [
                        ['option1', frequency(%)],
                        ['option2', frequency(%)],
                        ...
                    ],
                    'client1': [
                        ['option1', frequency(%)],
                        ['option2', frequency(%)],
                        ...
                    ],
                    'client2': [
                        ['option1', frequency(%)],
                        ['option2', frequency(%)],
                        ...
                    ],
                    ...
                    'email1@def.com': [
                        ['option1', frequency(%)],
                        ['option2', frequency(%)],
                        ...
                    ],
                    'email2@def.com': [
                        ['option1', frequency(%)],
                        ['option2', frequency(%)],
                        ...
                    ]
                },
                'number':36,
                'question':<the text of the question>,        
                'data': {
                    ...
                }
            ]
        '''
        # this routine assumes the client always comes before other results        
        questions = xl.filterQuestions("checkbox")
        options = xl.filterOptions("checkbox")
        questions.columns = ["Number", "Section", "Question", "Type", "Ignore"]
        options.columns = ["Options", "Marks"]
    
        # filter out unwanted columns
        questions = questions[["Number", "Question"]]    
        options = options[["Options"]]
    
        # join the two dataframes
        df = pd.concat([questions, options], axis=1)
        checkboxData = []    
        for i, row in df.iterrows():
            checkboxData.append({
                'Number':   row['Number'],
                'Question': row['Question'],
                'data': {}
            });
    
        # extract results from database
        def getOptions(df, question):
            df = df[df['Number'] == question]
            return df['Options'].tolist()[0]
        
        def findDataObject(question):
            for entry in checkboxData:
                if entry['Number'] == question:
                    return entry['data']
            raise("Question not found in checkboxData array")
        
        def updateObject(key, question, options, selections):
            data = findDataObject(question)
            selections = [int(n) for n in selections.split()]
            if data and key in data:
                percentIndex = 1
                for i, option in enumerate(options):
                    if i in selections:
                        data[key][i][percentIndex] += 100/rowCount  # update percentage        
            else:
                data[key] = []
                for i, option in enumerate(options):
                    if i in selections:
                        data[key].append([option, 100/rowCount])     # option, frequency%
                    else:
                        data[key].append([option, 0])                    
        
        db = Database()
        results = db.getDatabaseResults()
        rowCount = len(results)
        for row in results:
            email = row["email"]
            keyValuePairs = literal_eval(row['result'])
            for pair in keyValuePairs:
                if 'client' in pair:
                    client = pair['client']['name']
                if 'checkbox' in pair:
                    question = pair['checkbox']['question']
#                    optionCount = pair['checkbox']['optionCount']
                    options = getOptions(df, question)
    
                    # update selections
                    selections = pair['checkbox']['selection'].strip()
                    updateObject('all', question, options, selections)
                    updateObject(client, question, options, selections)
                    updateObject(email, question, options, selections)
        
        return { 'record':checkboxData, 'recordCount':rowCount }
