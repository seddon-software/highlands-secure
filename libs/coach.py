############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

# testing GIT

import os, re
import pandas as pd
from ast import literal_eval
#from PIL import Image
from io import StringIO
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER,TA_LEFT, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

if __name__ == "__main__": os.chdir("..")
from database import Database
from myglobals import MyGlobals
from excel import Excel
# from server_database import getResult, printResults

g = MyGlobals()
db = Database()
xl = Excel()

import itertools

class Coach:    
    def extractAnswers(self, row):
        def getQuestionsAndOptions():
            listOfQuestionsAndOptions = []
            for q, o in zip(xl.getQuestions(), xl.getOptions()):
                if q[3] == "radio": 
                    qo = [q, o[0]]
                    listOfQuestionsAndOptions.append(list(itertools.chain(*[q, o[0]])))
            return listOfQuestionsAndOptions

        def renameColumns(questionsAndOptions):
            columnNames = list(questionsAndOptions.columns)
            columnNames[0:4] = ['Id','Section','Question', 'Type']
            
            for i in range(0, len(columnNames)-4):
                columnNames[i+4] = f'Option{i+1}'
            questionsAndOptions.columns = columnNames
        
        results = []
        coaching = xl.extractCoaching()
        questionsAndOptions = pd.DataFrame(getQuestionsAndOptions())
        questionsAndOptions.drop([4], axis=1, inplace=True)
        renameColumns(questionsAndOptions)
        
        keyValuePairs = literal_eval(row['result'])
        for d in keyValuePairs:
            key = list(d.keys())[0]
            value = d[key]
            if key == "radio": 
                questionId = value['question']
                selectionId = f"Option{int(value['selection'])+1}"
                record = coaching.loc[coaching['Question'] == questionId]
                questionSeries = questionsAndOptions.loc[questionsAndOptions['Id'] == questionId]
                questionId = questionSeries['Id'].values[0]
                question = questionSeries['Question'].values[0]
                option = questionSeries[selectionId].values[0]
                advice = record[["Question", selectionId]].values[0][1]
                results.append([questionId, question, option, advice])
        return results
    
    def selectRecordByGuid(self, guid):
        records = db.getDatabaseResults()
        for r in records:
            pattern = r"{}$".format(guid)
            match = re.search(pattern, r['guid'])
            if match: return r
        return None

    def selectRecordsByEmail(self, email):
        records = db.getDatabaseResults()
        results = []
        for r in records:
            if r['email'] == email: results.append(r)
        return results

    def generatePdf(self, guid):
        buffer = StringIO()
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=0.1*inch)
              
        # container for the 'Flowable' objects
        p = ParagraphStyle('myStyle', 
                           alignment = TA_LEFT,
                           fontSize = 8,
                           fontName="Times-Roman")
        
        p2 = ParagraphStyle('myStyle', 
                           alignment = TA_CENTER,
                           fontSize = 32,
                           fontName="Times-Roman")
        
        elements = []         
        coach = Coach()
        answers = coach.extractAnswers(coach.selectRecordByGuid(guid))

        headerText = Paragraph("This is the report for ...", p2)
        elements.append(headerText)
        logo = 'client/images/highlands.png'
        image = Image(logo, 2*inch, 2*inch)
        image.hAlign = 'LEFT'
        elements.append(image)
        
        for answer in answers:
            questionId = Paragraph(f"Question: {answer[0]}", p)
            questionText = Paragraph(answer[1], p)
            yourAnswerText = Paragraph(answer[2], p)
            adviceText = Paragraph(answer[3], p)
            data = [[questionId, questionText],["Your Answer", yourAnswerText],["Advice", adviceText]]
            t=Table(data, colWidths=[1 * inch, 6 * inch], hAlign='LEFT')
            t.setStyle(TableStyle(
                            [
                                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                ('BACKGROUND', (0, 0), (1, 0), colors.yellow),
                                ('BACKGROUND', (0, 1), (1, 1), colors.palegreen),
                                ('BACKGROUND', (0, 2), (1, 2), colors.goldenrod),
                                ('FONTSIZE', (0, 0), (-1, -1), 8),
                                ('ALIGN',(0,0),(-1,-1),'LEFT'),
                                ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ]
                        ))
            elements.append(t)
            elements.append(Spacer(1,0.25*inch))

        # create the document in memory
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def getRecordSummaryByEmail(self, email):
        records = self.selectRecordsByEmail(email)
        summary = [["GUID", "eMail", "Timestamp", "Client", "Download PDF"]]
        for r in records:
            client = ""
            keyValuePairs = literal_eval(r['result'])
            for pair in keyValuePairs:
                if "client" in pair: 
                    client = pair["client"]["name"]
                    break
            fileName = f"{r['guid']}.pdf"
            downloadHtml = f'''<a href="https://localhost:7001/{fileName}" download="{fileName}">download</a>'''
            summary.append([r['guid'], r['email'], f'{r["timestamp"]:%d %B %Y %H:%M}', client, downloadHtml])
        print(str(summary))
        return summary              

if __name__ == "__main__":
    c = Coach()
    summary = c.getRecordSummaryByEmail("seddon-software@keme.co.uk")
    for s in summary:
        print(s)
