#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
import traceback
import sys, os, os.path, string, time
import stat
import re
import optparse

from . import common
from . import VOFrontend
from . import Factory
from . import UserCollector
from . import Certificates  
from .Condor import Condor
from .Configuration import ConfigurationError
#-------------------------
#os.environ["PYTHONPATH"] = ""

wmscollector_options = [ 
"install_type",
"hostname", 
"username",
"service_name", 
"condor_location", 
"x509_cert_dir",
"frontend_users",
"x509_cert", 
"x509_key", 
"x509_gsi_dn", 
"condor_tarball", 
"condor_admin_email", 
"number_of_schedds",
"glideinwms_location",
"install_vdt_client",
"vdt_location",
"pacman_location",
]

frontend_options = [ "x509_gsi_dn",
"service_name",
]

factory_options = [ "hostname",
"username",
]

usercollector_options = [ "hostname",
]

submit_options = []

valid_options = { "WMSCollector": wmscollector_options,
                  "Factory": factory_options,
                  "UserCollector": usercollector_options,
                  "Submit": submit_options,
                  "VOFrontend": frontend_options,
}




class WMSCollector(Condor):

  def __init__(self,inifile,optionsDict=None):
    global valid_options
    self.inifile = inifile
    self.ini_section = "WMSCollector"
    if inifile == "template":  # for creating actions not requiring ini file
      return
    if optionsDict != None:
      valid_options = optionsDict
    Condor.__init__(self, self.inifile, self.ini_section, valid_options[self.ini_section])
    self.not_validated = True
    self.use_gridmanager = True
    self.schedd_name_suffix = "glideins"
    self.daemon_list = "COLLECTOR, NEGOTIATOR, SCHEDD"
    self.colocated_services = []
    self.frontend      = None     # VOFrontend object
    self.factory       = None     # Factory object
    self.usercollector = None     # User collector object

  #--------------------------------
  def get_frontend(self):
    if self.frontend == None:
      self.frontend = VOFrontend.VOFrontend(self.inifile, valid_options)
  #--------------------------------
  def get_factory(self):
    if self.factory == None:
      self.factory = Factory.Factory(self.inifile, valid_options)
  #--------------------------------
  def get_usercollector(self):
    if self.usercollector == None:
      self.usercollector = UserCollector.UserCollector(self.inifile, valid_options)
  #--------------------------------
  def frontend_users(self):
    mydict = {}
    self.get_factory()
    self.get_frontend()
    mydict[self.frontend.service_name()] = self.factory.username()
    return mydict
  #--------------------------------
  def install(self):
    self.get_factory()
    self.get_frontend()
    common.logit("======== %s install starting ==========" % self.ini_section)
    common.ask_continue("Continue")
    self.validate()
    self.__install_condor__()
    self.configure()
    common.logit("======== %s install complete ==========" % self.ini_section)
    common.start_service(self.glideinwms_location(), self.ini_section, self.inifile) 

  #-----------------------------
  def validate(self):
    if self.not_validated:
      self.get_factory()
      self.get_frontend()
      self.verify_no_conflicts()
      self.install_vdtclient()
      self.install_certificates()
      self.validate_condor_install()
    self.not_validated = False
    
  #-----------------------------
  def configure(self):
    self.validate()
    common.logit("Configuring Condor")
    self.get_condor_config_data()
    self.__create_condor_mapfile__(self.condor_mapfile_users())
    self.__create_condor_config__()
    self.__create_initd_script__()
    common.logit("Configuration complete")

  #--------------------------------
  def condor_mapfile_users(self):
    users = []
    users.append([self.frontend.service_name(), self.frontend.x509_gsi_dn(), self.frontend.service_name()])
    users.append(["WMS Collector", self.x509_gsi_dn(), self.username()])
    return users

  #--------------------------------
  def condor_config_daemon_users(self):
    users = []
    users.append(["VOFrontend", self.frontend.x509_gsi_dn(), self.frontend.service_name()])
    users.append(["WMSCollector", self.x509_gsi_dn(), self.username()])
    return users

  #--------------------------------
  def verify_no_conflicts(self):
    self.get_usercollector()
    if self.hostname() != self.usercollector.hostname():
      return  # -- no problem, on separate nodes --
    if self.collector_port() == self.usercollector.collector_port():
      common.logerr("""The WMS and User collector are being installed on the same node. 
They both are trying to use the same port: %(port)s.
If not already specified, you may need to specifiy a 'collector_port' option 
in your ini file for either the WMSCollector or UserCollector sections, or both.
If present, are you really installing both services on the same node.
""" %  { "port": self.collector_port(),})

    if int(self.collector_port()) in self.usercollector.secondary_collector_ports():
      common.logerr("""The WMS collector and User collector are being installed on the same node. 
The WMS collector port (%(wms_port)s) conflicts with one of the secondary
User Collector ports that will be assigned: 
  %(secondary_ports)s.
If not already specified, you may need to specifiy a 'collector_port' option
in your ini file for either the WMSCollector or UserCollector sections, or both.
If present, are you really installing both services on the same node.
""" % { "wms_port": self.collector_port(),
        "secondary_ports": self.usercollector.secondary_collector_ports(), })

  #-------------------------
  def create_template(self):
    global valid_options
    print("; ------------------------------------------")
    print("; %s minimal ini options template" % self.ini_section)
    for section in valid_options.keys():
      print("; ------------------------------------------")
      print("[%s]" % section)
      for option in valid_options[section]:
        print("%-25s =" % option)
      print()

#### end of class ####

#---------------------------
def show_line():
    x = traceback.extract_tb(sys.exc_info()[2])
    z = x[len(x)-1]
    return "%s line %s" % (z[2], z[1])

#---------------------------
def validate_args(args):
    usage = """Usage: %prog --ini ini_file 

This will install a WMS collector service for glideinWMS using the ini file
specified.
"""
    parser = optparse.OptionParser(usage)
    parser.add_option("-i", "--ini", dest="inifile",
                      help="ini file defining your configuration")
    (options, args) = parser.parse_args()
    if options.inifile == None:
        parser.error("--ini argument required")
    if not os.path.isfile(options.inifile):
      raise common.logerr("inifile does not exist: %s" % options.inifile)
    common.logit("Using ini file: %s" % options.inifile)
    return options


##########################################
# Main function, primarily used for debugging
#
#def main(argv):
#  try:
#    create_template()
    #options = validate_args(argv)
    #wms = WMSCollector(options.inifile)
    #wms.install()
    #wms.__validate_collector_port__()
    #wms.__create_initd_script__()
    #wms.configure_gsi_security()
    #wms.configure_secondary_schedds()
#  except KeyboardInterrupt, e:
#    common.logit("\n... looks like you aborted this script... bye.")
#    return 1
#  except EOFError:
#    common.logit("\n... looks like you aborted this script... bye.");
#    return 1
#  except ConfigurationError, e:
#    print;print "ConfigurationError ERROR(should not get these): %s"%e;return 1
#  except common.WMSerror:
#    print;return 1
#  return 0


#--------------------------
#if __name__ == '__main__':
#  sys.exit(main(sys.argv))

