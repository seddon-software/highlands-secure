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
    reply = input("switch on automatic testing? [y/n] ")
    if reply == 'y':
        auto = "-auto"
    else:
        auto = ""
        
    print(auto)
    os.system("rm nohup.out")

    cmdk = "kill $(ps -ef | grep '[p]ython server.py' | awk '{print $2}') 2>/dev/null"
    os.system(cmdk)
    for spreadsheet in glob.glob('[A-Za-z]*.xlsx'):
        cmd = "nohup python server.py {} {}".format(spreadsheet, auto)
        subprocess.Popen(cmd.split())

    cmd = "ps -ef | grep '[pP]ython server.py'"
    os.system("ps -ef | head -1")
    os.system(cmd)
    time.sleep(5)
    os.system("cat nohup.out > $(tty)")
    print("***** servers started *****")
    