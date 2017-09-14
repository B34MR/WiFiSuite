# Module: eapconnect.py
# Description: Simplifies the ability to connect to Extensible Authentication Protocol (EAP) networks from Kali.
# Author: Nick Sanzotta/@Beamr
# Version = v 1.09142017

import sys, threading, time
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

class eapConnect(threading.Thread):
	def __init__(self, ssid, user, password, ca_cert, ca_path, client_cert, supplicantInt, interface):
		threading.Thread.__init__(self)
		self.setDaemon(1) # daemon
		self.ssid = ssid
		self.user = user
		self.password = password
		self.ca_cert = ca_cert
		self.ca_path = ca_path
		self.client_cert = client_cert
		self.supplicantInt = supplicantInt
		self.interface = interface
		self.wirelessInt = str(self.interface.get_ifname())
	
	def get_external_address(self):
		''' Obtains External IP Address '''
		data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
		return data["ip"]

	def run(self):
		while not self.user.empty():
			for user in self.user.get():
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
				        # "ca_cert": self.ca_cert,
				        # "ca_path": self.ca_path,
				        # "client_cert": self.client_cert,
				        "phase1": "peapver=0", #Chaning this from peapver=1 to peapver=0, resolved connecitivy issues!
				        "phase2": "auth=MSCHAPV2",		

				}	
				# Conf Added
				self.interface.add_network(network_cfg)		
				# Connect to Network Profile 0
				self.interface.select_network(self.supplicantInt+'/Networks/0')			

				while True:
					if self.interface.get_state() == 'completed':
						cls()
						banner()
						print(' SSID               : ' + ' ' + self.ssid)
						print(' Testing Credentials: ' + ' ' + user + ':' + self.password)
						print(' Interface          : ' + ' ' + self.interface.get_ifname())
						print(' Authentication     : ' + ' Success: '+ colors.green + '[!]\n' + colors.normal)
						db.eapspray_commit(self.ssid, user, self.password)
						break
					elif self.interface.get_state() == 'disconnected':
						cls()
						banner()
						print(' SSID               : ' + ' ' + self.ssid)
						print(' Testing Credentials: ' + ' ' + user + ":" + self.password)
						print(' Interface          : ' + ' ' + self.interface.get_ifname())
						print(' Authentication     : ' + ' Failed: '+ colors.red + '[!]' + colors.normal)
						# Remove from associated network, which results in state: 'inactive'
						self.interface.remove_network(self.supplicantInt+'/Networks/0')
						# Wait for inactive state, based on a timer.
						time.sleep(7)
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
						self.user.task_done()

				else:
					self.user.task_done()
