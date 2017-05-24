import argparse
from argparse import RawTextHelpFormatter
# Colors, Banner and cls
from theme import *

# Removes arg parse default usage Prefix
class HelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = ''
        return super(HelpFormatter, self).add_usage(
            usage, actions, groups, prefix)

def parse_args():
  ''' CLI Argument Options'''
  cls()
  # General Help
  general_help = colors.blue + ' Modules' + colors.normal + \
  '\n' + '   SCAN, ENUM, SPRAY, CONNECT, MAC, DATABASE\n' + \
  '\n' +colors.blue + ' Interface' + colors.normal + """
    [-i, --interface] Defines interface ex: wlan0
  """
  # SCAN Help
  scan_help = '\n' + colors.blue + ' SCAN' + colors.normal + """
    Usage Example: 
    eapsuite.py -i wlan0 scan
    
    Basic Options: 
    [--location] Tag your access point scans with a location: --location CoffeeShop]
    """
  # ENUM Help
  enum_help = '\n'+ colors.blue + ' ENUM' + colors.normal + """
    Usage Example: 
    eapsuite.py enum -i wlan0 -c 4 -d 10:da:43:a8:61:e4
    
    Basic Options:
    [-c, --channel] Define access point channel for enum mode ex: --channel 11]
    [-d, --deauth] Deauthenticate clients for enum mode ex: --deauth 10:10:10:A9:72:E6]
  
    Advanced Options:
    [--packets] Define number of deauth packets to send ex: --packets=30]
    [--seconds] Define Duration to Sniff Packets ex: --seconds=360]  
    """
  # SPRAY/CONNECT Help
  spray_help = '\n' + colors.blue + ' SPRAY/CONNECT' + colors.normal + """
    Usage Example: 
    eapsuite.py spray -i wlan0 -s FreeWiFi -u users.txt -p Summer2017
    
    Basic Options: 
    [-s, --ssid] Define SSID ex: --ssid FreeWiFi]
    [-u, --user] Define user or user list ex: --user jsmith ex: users.txt
    [-p, --password] Define password ex: --password Summer2017
    
    Advanced Options:
    [--client_cert] Define client side certificate ex: --client_cert
    [--server_cert] Define server side Certificate Authority (CA) ex: --ca_cert /RadiusServer.pem]
    """
  cheat_sheet = '\n' + colors.blue + ' Cheat Sheet' + colors.normal + """
    SCAN:           python wifisuite.py -iwlan0 scan --location="CoffeeShop"
    ENUM:           python wifisuite.py -iwlan0 -d 10:10:10:A9:72:E6 -c4 enum --seconds=30 --packets=5
    SPRAY (EAP):    python wifisuite.py -iwlan0 -s"RadiusX" -u data/users.txt -pWelcome1 spray
    SPRAY (WPA):    python wifisuite.py -iwlan0 -s"CompanyXYZ Hotspot" -p data/passwords.txt spray
    CONNECT (EAP):  python wifisuite.py -iwlan0 -s"RadiusX" -ubeamr -pWelcome1 connect
    CONNECT (WPA):  python wifisuite.py -iwlan0 -s"CompanyXYZ Hotspot" -p Password123 connect
    CONNECT (Open): python wifisuite.py -iwlan0 -s"CompanyXYZ Hotspot" connect
    MAC (Randomize):python wifisuite.py -iwlan0 mac
    MAC (Manual):   python wifisuite.py -iwlan0 -m 10:10:10:A9:72:E6 mac
    DATABASE:       python wifisuite.py database
   """
  # Custom Help
  Custom_help = general_help + scan_help + enum_help + spray_help + cheat_sheet

  # Create Parser
  parser = argparse.ArgumentParser(formatter_class=HelpFormatter, description=' '+
    str(banner()), usage=Custom_help, add_help=False)

  # MODULES
  mode_group = parser.add_argument_group(colors.blue + ' Modules' + colors.normal)
  mode_group.add_argument('mode', choices=['scan', 'enum', 'spray', 'connect', 'mac','database'], type=str.lower,\
  metavar='SCAN, ENUM, SPRAY, CONNECT, MAC, DATABASE', default='scan', help='')

  # INTERFACE
  interface_group = parser.add_argument_group(colors.blue + ' Interface' + colors.normal)
  interface_group.add_argument('-i','--interface', type=str, metavar='', nargs='?', help='')

  # SCAN OPTIONS
  scan_group = parser.add_argument_group(colors.blue + ' SCAN' + colors.normal)
  scan_group.add_argument('--location', type=str.upper, metavar='', help='')

  # ENUM OPTIONS
  enum_group = parser.add_argument_group(colors.blue + ' ENUM' + colors.normal)
  enum_group.add_argument('-c','--channel', type=int, metavar='',default=11, help='')
  enum_group.add_argument('-d','--deauth', type=str, metavar='', help='')
  enum_group.add_argument('--packets', type=int, metavar='', default=30, help='')
  enum_group.add_argument('--seconds', type=int, metavar='', default=360, help='')

  # SPRAY OPTIONS
  spray_group = parser.add_argument_group(spray_help)
  spray_group.add_argument('-s','--ssid', type=str, metavar='', help='')
  spray_group.add_argument('-u','--user', type=str, metavar='', help='')
  spray_group.add_argument('-p','--password', type=str, metavar='', help='')
  spray_group.add_argument('--client_cert', type=str, metavar='', help='')
  spray_group.add_argument('--server_cert', type=str, metavar='', help='')
  
  # MAC OPTIONS
  mac_group = parser.add_argument_group(colors.blue + ' MAC' + colors.normal)
  mac_group.add_argument('-m','--mac', type=str, metavar='', help='')

  # Create parser instance
  args = parser.parse_args()
  # Checks for Modules that require -i/--interface option.
  if args.mode != 'database' and args.interface is None:
    parser.error('\n'+red('!') + args.mode + ' requires -i/--interface')
  # Return arg values
  return args

    