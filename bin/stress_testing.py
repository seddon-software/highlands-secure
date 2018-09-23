############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################


import webbrowser
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
url = "https://127.0.0.1:9097/client.html?auto"
url = "https://asssessmydeal.com/"

count = 0
for i in range(10000):
    try:
        requests.get(url, verify=False)
    except:
        count += 1
    print(i)

print(count)
    
1

