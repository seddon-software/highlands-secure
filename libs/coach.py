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
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, LETTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER,TA_LEFT, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

PAGE_HEIGHT = LETTER[1]
PAGE_WIDTH = LETTER[0]

if __name__ == "__main__": os.chdir("..")
from database import Database
from myglobals import MyGlobals
from excel import Excel

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
                questionSeries = questionsAndOptions.loc[questionsAndOptions['Id'] == questionId]
                questionId = questionSeries['Id'].values[0]
                question = questionSeries['Question'].values[0]
                option = questionSeries[selectionId].values[0]
            
                record = coaching.loc[coaching['Question'] == questionId]
                advice = record[["Question", selectionId]].values[0][1]
                if not type(advice) is str: advice = "****"

                results.append([questionId, question, option, advice])
        return results
    
    def selectRecordByGuid(self, guid):
        records = db.getDatabaseResults()
        for r in records:
            pattern = r"{}$".format(guid)
            match = re.search(pattern, r['guid'])
            if match: return r
        return None

    def getEmailByGuid(self, guid):
        records = db.getDatabaseResults()
        for r in records:
            pattern = r"{}$".format(guid)
            match = re.search(pattern, r['guid'])
            if match: return r['email']
        return None
        
        
    def selectRecordsByEmail(self, email):
        records = db.getDatabaseResults()
        # return all records for mangers and admin (email will be None in this case)
        if not email: return records
        # only return their own records otherwise
        results = []
        for r in records:
            if r['email'] == email or r['email'] == None: results.append(r)
        return results

    def generatePdf(self, guid):
        def customColor(n):
            n = float(n)
            return colors.Color(red=(n/255),green=(n/255),blue=(n/255))
                                
        def myFirstPage(canvas, doc):
            canvas.saveState()
            # Footer
            canvas.setFont('Times-Roman', 8)
            canvas.drawString(MARGIN_LEFT, MARGIN_BOTTOM, f'Page {doc.page}')
            canvas.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, MARGIN_BOTTOM*0.95, "© Highlands Negotiations, 2018")
            canvas.restoreState()
        
        def myOtherPages(canvas, doc):
            canvas.saveState()
            # Header
            canvas.setFont('Times-Roman', 8)
            canvas.drawString(MARGIN_LEFT, PAGE_HEIGHT - MARGIN_TOP, f'Page {doc.page}')
            canvas.drawRightString(PAGE_WIDTH - MARGIN_LEFT, PAGE_HEIGHT - MARGIN_TOP, client)
            # Footer.
            canvas.drawString(MARGIN_LEFT, MARGIN_BOTTOM, f'Page {doc.page}')
            canvas.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, MARGIN_BOTTOM*0.95, "© Highlands Negotiations, 2018")
            canvas.restoreState()
            
        MARGIN_LEFT = 0.5*inch
        MARGIN_RIGHT = 0.5*inch
        MARGIN_TOP = 0.3*inch
        MARGIN_BOTTOM = 0.3*inch
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=LETTER, leftMargin=MARGIN_LEFT, rightMargin=MARGIN_RIGHT, bottomTop=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM)
              
        # container for the 'Flowable' objects
        p = ParagraphStyle('myStyle', 
                           alignment = TA_LEFT,
                           fontSize = 8,
                           fontName="Times-Roman")
        
        p2 = ParagraphStyle('myStyle', 
                           alignment = TA_CENTER,
                           fontSize = 16,
                           fontName="Times-Roman")
        
        elements = []         
        coach = Coach()
        answers = coach.extractAnswers(coach.selectRecordByGuid(guid))

        record = self.selectRecordByGuid(guid)
        client = self.determineClient(record)
        email = self.getEmailByGuid(guid)
        headerText = Paragraph(f"This is the report on {client}<br/><br/>prepared for<br/><br/>{email}", p2)
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
            data = [[questionId, questionText],["Your Answer", yourAnswerText],["Coaching", adviceText]]
            t=Table(data, colWidths=[1 * inch, 6 * inch], hAlign='LEFT')
            t.setStyle(TableStyle(
                            [
                                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                ('BACKGROUND', (0, 0), (1, 0), customColor(220)),
                                ('BACKGROUND', (0, 1), (1, 1), customColor(220)),
                                ('BACKGROUND', (0, 2), (1, 2), customColor(255)),
                                ('FONTSIZE', (0, 0), (-1, -1), 8),
                                ('ALIGN',(0,0),(-1,-1),'LEFT'),
                                ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ]
                        ))
            elements.append(t)
            elements.append(Spacer(1,0.25*inch))

        # create the document in memory
        doc.build(elements, onFirstPage=myFirstPage, onLaterPages=myOtherPages )
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def determineClient(self, r):
            client = ""
            keyValuePairs = literal_eval(r['result'])
            for pair in keyValuePairs:
                if "client" in pair: 
                    client = pair["client"]["name"]
                    break
            return client
        
    def getRecordSummaryByEmail(self, email):
        records = self.selectRecordsByEmail(email)
        summary = [["", "eMail", "Timestamp", "Client", "Report", "View"]]
        for i,r in enumerate(records):
            client = self.determineClient(r)
            fileName = f"{r['guid']}.pdf"
            server = g.get("server")
            port = g.get("port")
            url = f"https://{server}:{port}/{fileName}"
            downloadName = f"""Report on {client} ({r["timestamp"]:%d %B %Y %H.%M}).pdf"""
            downloadHtml = f'''<a href="{url}" download="{downloadName}">download</a>'''
            viewPdf = f'''<input type="button" id="{r['guid']}" class="pdfView ui-state-default ui-corner-all" value="view">'''
            summary.append([i+1, r['email'], f'{r["timestamp"]:%d %B %Y %H:%M}', client, downloadHtml, viewPdf])
        return summary              

if __name__ == "__main__":
    c = Coach()
    summary = c.getRecordSummaryByEmail("seddon-software@keme.co.uk")
    for s in summary:
        print(s)
