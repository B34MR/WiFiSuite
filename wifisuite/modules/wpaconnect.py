# Module: wpaconnect.py
# Description: Simplifies the ability to connect to Wi-Fi Protected Access (WPA) networks from Kali.
# Author: Nick Sanzotta/@Beamr
# Version: v 1.09142017

import threading, time
from subprocess import Popen, PIPE
from wpa_supplicant.core import WpaSupplicantDriver
from twisted.internet.selectreactor import SelectReactor
from twisted.internet import task
from theme import *
import json, urllib, socket
import netifaces

try:
	from dbcommands import DB
	import sqlite3
	conn = sqlite3.connect('data/WiFiSuite.db', check_same_thread=False) # Thread Support
	conn.text_factory = str # Interpret 8-bit bytestrings 
	conn.isolation_level = None # Autocommit Mode
	db = DB(conn)
except Exception as e:
	print(red('!')+'Could not connect to database: %s' % (e))
	sys.exit(1)

class wpaConnect(threading.Thread):
	def __init__(self, ssid, password, supplicantInt, interface):
			threading.Thread.__init__(self)
			self.setDaemon(1) # daemon
			self.ssid = ssid
			self.password = password
			self.supplicantInt = supplicantInt
			self.interface = interface
			self.wirelessInt = str(self.interface.get_ifname())
	
	def get_external_address(self):
		''' Obtains External IP Address '''
		data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
		return data["ip"]

	def run(self):
		while not self.password.empty():
			cls()
			banner()
			for password in self.password.get():
				# Time Stamp for each user
				curr_time2 = time.time()
				#DEBUG PRINT
				network_cfg = {
						"disabled": 0,
						"ssid": self.ssid, 
						"mode": 0,
						"proto": "WPA2",
						"key_mgmt": "WPA-PSK",
						"pairwise": "CCMP",
						"psk": password,	

				}		

			# Conf Added
				self.interface.add_network(network_cfg)	
				# Connect to Network Profile 0
				self.interface.select_network(self.supplicantInt+'/Networks/0')	
				# DEBUG: Print Current WPA CONF
				# print(interface.get_current_network())	

				while True:
					if self.interface.get_state() == 'completed':
						print(' SSID               : ' + ' ' + self.ssid)
						print(' Testing PSK        : ' + ' ' + password)
						print(' Interface          : ' + ' ' + self.interface.get_ifname())
						print(' Interface Status   : ' + ' ' + self.interface.get_state())
						print(' Authentication     : ' + ' Success: '+ colors.green + '[!]' + colors.normal)
						print(' Elapsed Time       :  %.1fs\n' % (time.time() - curr_time2))
						db.wpabrute_commit(self.ssid, password)
						break
					elif self.interface.get_state() == 'disconnected':
						print(' SSID               : ' + ' ' + self.ssid)
						print(' Testing PSK        : ' + ' ' + password)
						print(' Interface          : ' + ' ' + self.interface.get_ifname())
						print(' Interface Status   : ' + ' ' + self.interface.get_state())
						print(' Authentication     : ' + ' Failed: '+ colors.red + '[!]' + colors.normal)
						print(' Elapsed Time       :  %.1fs\n ' % (time.time() - curr_time2))
						# Remove from associated network, which results in state: 'inactive'
						try:
							self.interface.remove_network(self.supplicantInt+'/Networks/0')
						except Exception as e:
							print(' [!] Error: ' + str(e))
							print(' [i] Attempting to recover.\n')
							time.sleep(1.5) # Testing might be able to lower this value
							pass
						# Wait for inactive state, based on a timer.
						time.sleep(7) # May be able to lower this value for WPA?
					elif self.interface.get_state() == 'inactive':
						break
				
				if self.interface.get_state() == 'completed':
						p1 = Popen(['dhclient', self.wirelessInt], stdout=open("/dev/null", "w"), stderr=open("/dev/null", "w"))
						print('\n')
						# Obtain Internal IP Address
						netifaces.ifaddresses(self.wirelessInt)
						ip = netifaces.ifaddresses(self.wirelessInt)[2][0]['addr']
						print(blue('i')+self.wirelessInt.upper() + ' IP Address: ' + ip)
						# Connectivity Check
						try:
							extipAddress = self.get_external_address()
						except IOError:
							print(red('!')+ 'No internet connectivity')
							pass #CHECK
						raw_input(blue('*')+'Press Enter to gracefully close the WiFi network connection:')
						# Remove from associated network, which results in state: 'inactive'
						self.interface.remove_network(self.supplicantInt+'/Networks/0')
						# Wait for inactive state, based on a timer.
						time.sleep(7)
						print(blue('i')+'WiFi Connection Terminated. ')
						self.password.task_done()

				else:
					self.password.task_done()