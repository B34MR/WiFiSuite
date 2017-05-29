# Module: openconnect.py
# Description: Simplifies the ability to connect to open Wi-Fi networks with broadcasts either enabled or disabled.
# Author: Nick Sanzotta/@Beamr
# Version: v 1.05212017

import os, threading, time
# WPA Supplicant required libs
from wpa_supplicant.core import WpaSupplicantDriver
from twisted.internet.selectreactor import SelectReactor
from twisted.internet import task
# Theme
from theme import *
# External IP Query
import json, urllib, socket
# Internal IP Query
import netifaces

# # Database
# from dbcommands import DB
# # Database connection
# # CHECK: needs to be relocated, used while testing database.py
# import sqlite3
# try:
#      # Connect to Database 
#      # ISSUE/TEMP hardcoded db_path
#      conn = sqlite3.connect('data/WiFiSuite.db', check_same_thread=False) # KEEP Thread Support
#      conn.text_factory = str # KEEP Interpret 8-bit bytestrings 
#      conn.isolation_level = None # KEEP Autocommit Mode
#      db = DB(conn)
# except Exception as e:
#      print(red('!') + 'Could not connect to database: ' +str(e))
#      sys.exit(1)

class openConnect():
	def __init__(self, ssid, supplicantInt, interface):
			# threading.Thread.__init__(self)
			# self.setDaemon(1) # Creates Thread in daemon mode
			self.ssid = ssid
			self.supplicantInt = supplicantInt
			self.interface = interface
			self.wirelessInt = str(self.interface.get_ifname())
	
	def get_external_address(self):
		''' Obtains External IP Address '''
		data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
		return data["ip"]

	def run(self):
		cls()
		banner()
		# Time Stamp
		curr_time2 = time.time()
		#DEBUG PRINT
		network_cfg = {
				"disabled": 0, 
				"ssid": self.ssid,
				"scan_ssid":1,
				"mode": 0,
				"key_mgmt": "NONE"
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
				# print(' Testing PSK        : ' + ' ' + password)
				print(' Interface          : ' + ' ' + self.interface.get_ifname())
				print(' Interface Status   : ' + ' ' + self.interface.get_state())
				print(' Authentication     : ' + ' Success: '+ colors.green + '[!]' + colors.normal)
				print(' Elapsed Time       :  %.1fs\n' % (time.time() - curr_time2))
				# db.wpabrute_commit(self.ssid, password)
				break
			elif self.interface.get_state() == 'disconnected':
				print(' SSID               : ' + ' ' + self.ssid)
				# print(' Testing PSK        : ' + ' ' + password)
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
				os.system('dhclient ' + self.wirelessInt)
				print('\n')
				# Obtain Internal IP Address
				netifaces.ifaddresses(self.wirelessInt)
				ip = netifaces.ifaddresses(self.wirelessInt)[2][0]['addr']
				print(blue('i')+self.wirelessInt.upper() + ' IP Address: ' + ip)

				# Testing Connectivity Check and Portal Page
				try:
					extipAddress = self.get_external_address()
				except (IOError, ValueError) as e:
					print(red('!')+ 'There maybe a signin page')
					pass

				# # Connectivity Check
				# try:
				# 	extipAddress = self.get_external_address()
				# except IOError:
				# 	print(red('!')+ 'No internet connectivity')
				# 	pass #CHECK
				# # # Testing for Portal Page
				# # try:
				# # 	extipAddress = self.get_external_address()
				# # except ValueError:
				# # 	print(red('!')+ 'There maybe a signin page')
				# # 	pass

				raw_input(blue('*')+'Press Enter to gracefully close the WiFi network connection:')
				# Remove from associated network, which results in state: 'inactive'
				self.interface.remove_network(self.supplicantInt+'/Networks/0')
				# Wait for inactive state, based on a timer.
				time.sleep(7)
				print(blue('i')+'WiFi Connection Terminated. ')
				# self.password.task_done()
		else:
			print('Done')
			# self.password.task_done()