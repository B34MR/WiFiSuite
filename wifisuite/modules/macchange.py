# Module: macchanger.py
# Description: Wrapper for built-in linux tool macchanger.
# Author: Nick Sanzotta/@Beamr
# Version: v 1.05162017

import os, time
from subprocess import Popen, PIPE 
from theme import *

def macRandom(interface):
	wirelessInt = str(interface.get_ifname())
	p1 = Popen(["ifconfig " + wirelessInt + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'"], shell=True, stdout=PIPE)
	print(normal('i') + 'Current MAC Address: %s' % (p1.communicate()[0].rstrip('\n')))
	os.system('ifconfig ' + wirelessInt + ' down')
	os.system('macchanger -r ' + wirelessInt + ' > /dev/null')
	os.system('ifconfig ' + wirelessInt + ' up')
	p2 = Popen(["ifconfig " + wirelessInt + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'"], shell=True, stdout=PIPE)
	print(blue('*') + 'New MAC Address: %s' % (p2.communicate()[0].rstrip('\n')))

def macManual(interface, macaddress):
	wirelessInt = str(interface.get_ifname())
	p1 = Popen(["ifconfig " + wirelessInt + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'"], shell=True, stdout=PIPE)
	print(normal('i') + 'Current MAC Address: %s' % (p1.communicate()[0].rstrip('\n')))
	os.system('ifconfig ' + wirelessInt + ' down')
	os.system('macchanger -m ' + macaddress + ' ' + wirelessInt + ' > /dev/null')
	os.system('ifconfig ' + wirelessInt + ' up')
	p2 = Popen(["ifconfig " + wirelessInt + " | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'"], shell=True, stdout=PIPE)
	print(blue('*') + 'New MAC Address: %s' % (p2.communicate()[0].rstrip('\n')))
