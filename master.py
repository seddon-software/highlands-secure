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
    cmdk = "kill $(ps -ef | grep '[p]ython -u server.py' | awk '{print $2}')"
    os.system(cmdk)
    for spreadsheet in glob.glob('[A-Za-z]*.xlsx'):
        cmd = "python -u server.py {}".format(spreadsheet)
        subprocess.Popen(cmd.split())

    time.sleep(10)
    print("***** servers started *****")
    