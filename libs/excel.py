############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

import pandas as pd
import sys, os
from validate_email import validate_email
from myglobals import MyGlobals

if __name__ == "__main__": os.chdir("..")

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
 
    def getManagerType(self, theManager):
        table = pd.read_excel(excelFile, 'managers')
        table = table[['MANAGER','TYPE']]
        table = table[table.MANAGER.notnull()]
        
        theManager = theManager.strip().lower()
        for _, row in table.iterrows():
            if row['MANAGER'].strip().lower() == theManager: return row['TYPE'].strip().lower()
        return "assessment"
    
    def getAllowOrDenyMode(self):
        table = pd.read_excel(excelFile, 'setup')
        table = table[['TYPE', 'NAME']]
        table = table[table.TYPE.notnull()]
        for _, row in table.iterrows():
            if row['TYPE'] == 'allow_or_deny':
                mode = row['NAME'].strip().lower()
                if mode == 'allow' or mode == 'deny':
                    return mode
        return 'deny'
        
    def getAllowDomains(self, email):
        try:
            if not validate_email(email): return False
        except:
            return False
        pass
        domain = email.split('@')[1]
        try:
            table = pd.read_excel(excelFile, 'allow')
            table = table[['ALLOW']]
            table = table[table.ALLOW.notnull()]
            for _, row in table.iterrows():
                if domain.endswith(row['ALLOW']): return True
        except:
            # no allow table present
            return False        
        return False
        
    def getDenyDomains(self, email):
        try:
            if not validate_email(email): return True
        except:
            return True
        domain = email.split('@')[1]
        try:
            table = pd.read_excel(excelFile, 'deny')
            table = table[['DENY']]
            table = table[table.DENY.notnull()]
            for _, row in table.iterrows():
                if row['DENY'] == domain: return True
        except:
            # no deny table present
            return False        
        return False
    
    def getSendgridAPI_KEY(self):
        try:
            table = pd.read_excel(excelFile, 'setup')
            table = table[['TYPE', 'NAME']]
            table = table[table.TYPE.notnull()]
            for _, row in table.iterrows():
                if row['TYPE'] == 'SENDGRID_API_KEY': return row['NAME']
        except:
            return False        
        return False
        
    def getEmailFrom(self):
        try:
            table = pd.read_excel(excelFile, 'setup')
            table = table[['TYPE', 'NAME']]
            table = table[table.TYPE.notnull()]
            for _, row in table.iterrows():
                if row['TYPE'] == 'email_from': from_ = row['NAME']
            if not validate_email(from_): raise Exception()
            return from_
        except:
            # no entry present
            return "registration@assessmydeal"        
        
    def getEmailSubject(self):
        subject = "Assess My Deal Registration Code"
        try:
            table = pd.read_excel(excelFile, 'setup')
            table = table[['TYPE', 'NAME']]
            table = table[table.TYPE.notnull()]
            for _, row in table.iterrows():
                if row['TYPE'] == 'email_subject': subject = row['NAME']
            return subject
        except:
            # no entry present
            return subject
    
    def getEmailBody(self):
        part1 = ""
        part2 = ""
        body = (part1, part2)
        try:
            table = pd.read_excel(excelFile, 'setup')
            table = table[['TYPE', 'NAME']]
            table = table[table.TYPE.notnull()]
            for _, row in table.iterrows():
                if row['TYPE'] == 'email_body_part1': part1 = row['NAME'].strip()
                if row['TYPE'] == 'email_body_part2': part2 = row['NAME'].strip()
                if part1 != "" and part2 != "": body = (part1, part2)
            return body
        except:
            # no entry present
            return body        
    
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
        try:
            table = table.drop(['Important'], axis=1)
        except:
            pass        # may have left this (unused) column in old spreadsheet
        table[['Number']] = table[['Number']].fillna(value="")
        table[['Section']] = table[['Section']].fillna(value="")
        validate()
        pd.options.display.max_rows = 999999
        self.questions = self.extractQuestions(table[['Number', 'Section', 'Question', 'Type', 'Option1']])
        self.options = self.extractOptions(table)

            

if __name__ == "__main__":
    xl = Excel()
#     print(xl.getManagerType("  peter.SMith@highlands.com   "))
#     print(xl.getAllowOrDenyMode())
#     print(xl.getAllowDomains("peter.SMith@highlands.ibm.com"))
    print(xl.getEmailFrom())
    print(xl.getEmailSubject())
    print(xl.getEmailBody())

    
    
    