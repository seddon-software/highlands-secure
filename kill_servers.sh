#! /bin/bash

############################################################
#
#    Highlands Server
#
#    © Highlands Negotiations, 2018, v1.0
#
############################################################

# cd . is only there to avoid errors when no processes are found
kill $(cd .;ps -ef | grep '[p]ython -u server.py' | awk '{print $2}') 2>/dev/null
