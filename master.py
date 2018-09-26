############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

import glob
import os
import subprocess
import time

if __name__ == "__main__":
    cmdk = "kill $(ps -ef | grep '[p]ython server.py' | awk '{print $2}') 2>/dev/null"
    os.system(cmdk)
    for spreadsheet in glob.glob('[A-Za-z]*.xlsx'):
        cmd = "nohup python server.py {}".format(spreadsheet)
        subprocess.Popen(cmd.split())

    cmd = "ps -ef | grep '[pP]ython server.py'"
    os.system("ps -ef | head -1")
    os.system(cmd)
    time.sleep(5)
    print("***** servers started *****")
    