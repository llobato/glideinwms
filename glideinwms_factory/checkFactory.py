#!/usr/bin/env python
#
# Project:
#   glideinWMS
#
# File Version: 
#   $Id: checkFactory.py,v 1.4.8.2 2010/09/24 15:30:36 parag Exp $
#
# Description:
#   Check if a glideinFactory is running
# 
# Arguments:
#   $1 = glidein submit_dir (i.e. factory dir)
#
# Author:
#   Igor Sfiligoi Jul 9th 2008
#

import sys
import glideFactoryPidLib

try:
    startup_dir = sys.argv[1]
    factory_pid = glideFactoryPidLib.get_factory_pid(startup_dir)
except:
    print "Not running"
    sys.exit(1)

print "Running"
sys.exit(0)

