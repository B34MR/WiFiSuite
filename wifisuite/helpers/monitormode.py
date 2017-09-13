# Module: monitormode
# Description: Helper - Places wireless interface in and out of Monitor Mode
# Author: Nick Sanzotta
# Contributors: 
# Version: v 1.09132017
try:
	import os
	from theme import *
except Exception as e:
	print('\n [!] Error %s' % (e))

def monitor_start(wirelessInt, channel):
	print(normal('i') + 'Starting Monitor Mode on : %s' % (wirelessInt))
	os.system('ifconfig ' + wirelessInt + ' down')
	os.system('iwconfig ' + wirelessInt + ' mode managed')
	os.system('ifconfig ' + wirelessInt + ' up')
	os.system('iwconfig ' + wirelessInt + ' channel ' + str(channel))
	os.system('ifconfig ' + wirelessInt + ' down')
	os.system('iwconfig ' + wirelessInt + ' mode monitor')
	os.system('ifconfig ' + wirelessInt + ' up')
	print(normal('*') + 'Interface locked on channel: ' + str(channel))
	return

def monitor_stop(wirelessInt):
	print(normal('i') + 'Stopping Monitor Mode on : %s' % (wirelessInt))
	os.system('ifconfig ' + wirelessInt + ' down')
	os.system('iwconfig ' + wirelessInt + ' mode monitor')
	os.system('ifconfig ' + wirelessInt + ' up')
	os.system('ifconfig ' + wirelessInt + ' down')
	os.system('iwconfig ' + wirelessInt + ' mode managed')
	os.system('ifconfig ' + wirelessInt + ' up')
	return