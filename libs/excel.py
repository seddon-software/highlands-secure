import pandas as pd
import sys
from myglobals import MyGlobals

g = MyGlobals()

class Excel:
    def isAutoFill(self, field):
        if(isinstance(field, str)): 
            return field.strip() == "autofill"
        else:
            return False
        
    def extractQuestions(self, df):
        '''questions will be a list of [QuestionNo, Section, Question, Type, Autofill] tuples'''
        questions = []    
        for row in df.itertuples():
            if(isinstance(row[3], str)):
                questions.append([str(row[1]), row[2], row[3], row[4], self.isAutoFill(row[5])])
        return questions
    
    
    def extractOptions(self, df):
        df.drop(['Number', 'Section', 'Question','Type'], axis = 1, inplace = True)
        df = df.fillna(value='')
        options = []
        row = []
        for t in df.itertuples():
            if(t[1] != ''):
                row.append([i for i in t[1:] if i != ''])
            else:            
                if(row): options.append(row)
                row = []
        if(row): options.append(row)    # for last row
            
        return options
        
    def filterQuestions(self, questionType):
        listQuestions = []
        for question, option in zip(self.questions, self.options):    #@UnusedVariable
            if(question[3] == questionType): listQuestions.append(question)
        return pd.DataFrame(listQuestions)
     
    def filterOptions(self, questionType):
        listOptions = []
        for question, option in zip(self.questions, self.options):
            if(question[3] == questionType): listOptions.append(option)
        return pd.DataFrame(listOptions)
    
    def getQuestions(self):
        return self.questions
    
    def getOptions(self):
        return self.options
    
    def __init__(self):
        def validate():
            validated = True
            previousRowIsAQuestion = False
            previousRowIsAnOption = False

            '''
            check each question row is not followed by a blank row
            but is preceded by a blank row
            '''
            for row in table.itertuples():
                thisRowIsAQuestion = isinstance(row.Question, str)
                thisRowIsAnOption = isinstance(row.Option1, str)

                def questionIsFollowedByABlankRow():
                    if(previousRowIsAQuestion and not thisRowIsAnOption):
                        number = table[row.Index-1:row.Index]['Number'].to_string(index=False)
                        if number == "0": number = " "
                        question = table[row.Index-1:row.Index]['Question'].to_string(index=False)
                        print("Error, blank row after: {}. {}".format(number, question))
                        return False
                    else:
                        return True
                    
                def questionPrecededByABlankRow():
                    if thisRowIsAQuestion:
                        if previousRowIsAnOption:
                            number = table[row.Index:row.Index+1]['Number'].to_string(index=False)
                            if number == "0": number = " "
                            question = table[row.Index:row.Index+1]['Question'].to_string(index=False)
                            print("Error, no blank row before: {}. {}".format(number, question))
                            return False
                        else:
                            return True
                    else:
                        return True
                
                if not questionIsFollowedByABlankRow(): validated = False
                if not questionPrecededByABlankRow(): validated = False
                previousRowIsAQuestion = thisRowIsAQuestion
                previousRowIsAnOption = thisRowIsAnOption
            if not validated: 
                print("\nErrors exist in Questions in {} ... exiting".format(excelFile))
                sys.exit()
        global excelFile, questions, options
        excelFile = g.get("excelFile")
        pd.set_option('display.width', 1000)
        table = pd.read_excel(excelFile, 'questions', converters={'Number':str})
        table = table.drop(['Comments'], axis=1)
        table[['Number']] = table[['Number']].fillna(value="")
        table[['Section']] = table[['Section']].fillna(value="")
        validate()
        pd.options.display.max_rows = 999999
        self.questions = self.extractQuestions(table[['Number', 'Section', 'Question', 'Type', 'Option1']])
        self.options = self.extractOptions(table)
