#! /bin/bash

############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################


kill $(ps -ef | grep '[p]ython -u server.py' | awk '{print $2}')
