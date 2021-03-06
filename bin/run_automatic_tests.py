############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

import socket
import pandas as pd
import os, sys, re
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.chdir("..")
sys.path.append("libs")

from myglobals import MyGlobals
g = MyGlobals()

browser = None

def startBrowser(url):
    print("URL:", url)
    global browser
    os.environ["PATH"] = "testing" + os.pathsep + os.environ["PATH"]

    try:
        browser = webdriver.Chrome(executable_path=r"chromedriver.exe")
    except: pass
    try:
        browser = webdriver.Chrome(executable_path=r"chromedriver_linux")
    except: pass
    try:
        browser = webdriver.Chrome(executable_path=r"chromedriver_macos")
    except: pass
    try:
        r = requests.get(url, verify=False)
        if r.status_code == 404:
            raise Exception("Page not found: have you switched on automatic testing?")

        browser.get(url)
        wait = WebDriverWait(browser, 60)
        
#        wait.until(lambda browser: browser.execute_script("return jQuery.active == 0"))
    except Exception as e:
        print(e)
        print("aborting ...")
        sys.exit()

def stopBrowser():
    global browser
    browser.close()

def scrollTo(element):
    global browser
    browser.execute_script("arguments[0].scrollIntoView();", element)
    
def enterText(question, text):
    global browser
    try:
        selector = "input#text-{}".format(question)
        wait = WebDriverWait(browser, 60)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        element = browser.find_element_by_css_selector(selector)
        scrollTo(element)
        element.clear()
        element.send_keys(text);
    except Exception as e:
        print(e, selector)

def enterTextArea(question, text):
    global browser
    selector = "textarea#text-{}".format(question)
    element = browser.find_element_by_css_selector(selector)
    scrollTo(element)
    element.clear()
    element.send_keys(text);   

def clickTable(question, row, col):
    selector = "input#radio-{}-{}-{}".format(question, row, col)
    clickIt(selector)
    
def clickTable2(question, row, col):
    selector = "input#radio-{}-{}-{}".format(question, row, col)
    clickIt(selector)
    
def clickRadio(question, col):
    selector = "input#radio-{}-{}".format(question, col-1)
    clickIt(selector)

def clickCheckbox(question, col):
    selector = "input#check-{}-{}".format(question, col-1)
    clickIt(selector)

def submit(choice):
    global browser
    
    clickIt("#showResults")

    wait = WebDriverWait(browser, 60)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-dialog-titlebar')))
    wait = WebDriverWait(browser, 60)
    wait.until(EC.element_to_be_clickable((By.ID, 'continue-yes')))
    wait = WebDriverWait(browser, 60)
    wait.until(EC.element_to_be_clickable((By.ID, 'continue-no')))

    try:
        if choice == "Yes": clickIt("#continue-yes")
        if choice == "No": clickIt("#continue-no")
    except Exception as e:
        print(e)
        print("Popup not displayed in 60 secs")

def clickIt(selector):
    global browser
    element = browser.find_element_by_css_selector(selector)
    scrollTo(element)
    element.click();   

def isServerRunning(g):
    theSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = g.get("server")
    port = int(g.get("port"))
    result = theSocket.connect_ex((server, port))
    if result == 0:
        return True
    else:
        return False

def readExcelFile(page):
    table = pd.read_excel(excelFile, page, converters={'Question':str})
    return table
    
    
def doValidation(table):
    validation = table[pd.notnull(table["OptionCount"])]
    validation = validation.dropna(axis="columns")
    validation = validation.drop(["Section", "Text"], axis="columns")
    rows, cols = validation.shape       #@UnusedVariable

    for testNo in range(1, cols-3): # 3 non test columns
        for index, row in validation.iterrows():        #@UnusedVariable
            question = row["Question"]
            category = row["Category"]
            optionCount = row["OptionCount"]
            data = "Test{}".format(testNo)
            values = row[data]
            if category == "radio":
                if optionCount < values or values < 1: 
                    print("Option out of range in test {}, question {}".format(testNo, question))
                    sys.exit()
            if category == "table":  
                values = values.strip()
                values = [int(x) for x in re.split("[ ]+", values)]
                items, Max = [int(x) for x in optionCount.split(",")]
                if len(values) != items:
                    print("Not enough values in test {}, question {}".format(testNo, question))
                    sys.exit()
                if max(values) > Max or min(values) < 1:
                    print("Option out of range in test {}, question {}".format(testNo, question))
                    sys.exit()
            if category == "table2": 
                values = values.strip()
                rowValue, colValue = [int(x) for x in re.split("[ ]+", values)]
                rowMax, colMax = [int(x) for x in optionCount.split(",")]
                if rowValue > rowMax or rowValue < 1 or colValue > colMax or colValue < 1:
                    print("Option out of range in test {}, question {}".format(testNo, question))
                    sys.exit()
            if category == "checkbox":
                if isinstance(values, int):
                    values = [values]
                else:
                    values = [int(x) for x in re.split("[ ]+", values)]
                if len(values) > optionCount:
                    print("Too many values in test {}, question {}".format(testNo, question))
                    sys.exit()
                if max(values) > optionCount or min(values) < 1: 
                    print("Option out of range in test {}, question {}".format(testNo, question))
                    sys.exit()
    
excelFile = g.get("excelFile")
pd.set_option('display.width', 1000)
table = readExcelFile('tests')
table = table[pd.notnull(table['Question'])]
doValidation(table)
table = table.dropna(axis="columns")
table.drop(axis=1, labels="Text", inplace=True)
if not isServerRunning(g): 
    print("Server not running ...\nexiting")
    sys.exit()

print("server:", g.get("server"))
print("port:", g.get("port"))
print("database:", g.get("database"))
print("table:", g.get("table"))

try:
    rows, cols = table.shape
    
    startBrowser("https://{}:{}/client.html?auto".format(g.get("server"), g.get("port")))
    for testNo in range(1, cols-1):  # 1 non test column
        print("Starting Test {}".format(testNo))
        data = "Test{}".format(testNo)
        df = table[["Question", "Category", data]]
        for index, row in df.iterrows():
            question = row["Question"]
            category = row["Category"]
            values = row[data]
            if category == "text":     enterText(question, values)
            if category == "textarea": enterTextArea(question, values)
            if category == "radio":    clickRadio(question, values)
            if category == "email":    enterText(question, values)
            if category == "client":   enterText(question, values)
            if category == "table":
                for i, value in enumerate(values.split()):
                    clickTable(question, i+1, value)
            if category == "table2":
                values = str(values)
                row, col = values.split()
                clickTable2(question, row, col)
            if category == "checkbox":
                values = str(values)
                for value in values.split():
                    clickCheckbox(question, int(value))
        if testNo < cols-2:
            submit("Yes")
        else:
            submit("No")
    stopBrowser()
        
except Exception as e:
    print(e)

print("Completed Tests")
