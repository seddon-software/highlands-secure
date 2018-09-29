import pandas as pd
import numpy as np;
import json, re
from io import StringIO

fileName = "RecordData_20180619_1035.Json"
fileName = "test_results.Json"
with open(fileName, "r") as f:
    data = json.load(f)
    
def searchTestResults(rawPattern):
    result = []
    pattern = re.compile(rawPattern)    
    testResults = data["TestResults"]
    floatPattern = "[0-9.]+"
    floatAntiPattern = "[^0-9.]+"
    for testResult in testResults:
        for line in testResult["TestResultLines"]:
            out = "{} {} {}".format(testResult['Created'], testResult['Title'], line)
            if pattern.search(out):
                try:
                    minValue = re.search("({0}){1}({0})".format(floatPattern, floatAntiPattern), line["NormalRange"]).group(1)
                    maxValue = re.search("({0}){1}({0})".format(floatPattern, floatAntiPattern), line["NormalRange"]).group(2)
                except:
                    minValue = ""
                    maxValue = ""
                try:
                    value = re.search("({})".format(floatPattern), line["Result"]).group(1)
                    result.append("{}, {}, {}, {}\n".format(testResult['Created'], minValue, maxValue, value))
                except:
                    pass

    df = pd.read_csv(StringIO("".join(result)), header=None)
    df.columns = ["date", "minValue", "maxValue", "value"]
    return df

def testResults():
    result = []
    testResults = data["TestResults"]
    for testResult in testResults:
        for line in testResult["TestResultLines"]:
            out = "{} {} {}".format(testResult['Created'], testResult['Title'], line)
            print(out)
    
    return result

title = "Serum vitamin D"
title = "TSH"
title = "Systolic"
title = "Diastolic"
print(testResults())
df = searchTestResults(title)
print(df)

#from datetime import datetime
import datetime

# datetime_object = datetime.strptime('1 Jun 2005  1:33PM', '%d %b %Y')

df['date'] = pd.to_datetime(df['date'], format='%d %b %Y')
df = df.reindex(index=df.index[::-1])
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
myFmt = mdates.DateFormatter('%d %b %Y')
ax = df.plot(x='date', y='value', rot=45, title=title)
ax.xaxis_date()
# plt.xlim(xmin=datetime.date(2004, 1, 1),
#          xmax=datetime.date(2019, 1, 1))
plt.tight_layout()
myFmt = mdates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(myFmt)
#print(testResults())
plt.show()
