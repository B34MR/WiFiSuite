# Module: macchanger.py
# Description: Wrapper for built-in linux tool macchanger.
# Author: Nick Sanzotta/@Beamr
# Version: v 1.05162017

import os
import time
# from wpa_supplicant.core import WpaSupplicantDriver
from theme import *

def getMAC(interface):
	wirelessInt = str(interface.get_ifname())
	os.system('ifconfig ' + str(wirelessInt) +\
	" | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'")
	return

def macRandom(interface):
	wirelessInt = str(interface.get_ifname())
	print('Current MAC Address: ')
	getMAC(interface)
	os.system('ifconfig ' + wirelessInt + ' down')
	os.system('macchanger -r ' + wirelessInt + ' > /dev/null')
	os.system('ifconfig ' + wirelessInt + ' up')
	print(' \nNew MAC Address: ')
	getMAC(interface)
	print('\n')

def macManual(interface, macaddress):
	wirelessInt = str(interface.get_ifname())
	print('Current MAC Address: ')
	getMAC(interface)
	os.system('ifconfig ' + wirelessInt + ' down')
	os.system('macchanger -m ' + macaddress + ' ' + wirelessInt + ' > /dev/null')
	os.system('ifconfig ' + wirelessInt + ' up')
	print(' \nNew MAC Address: ')
	getMAC(interface)
	print('\n')