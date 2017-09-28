# Module: openconnect.py
# Description: Simplifies the ability to connect to open Wi-Fi networks with broadcasts either enabled or disabled.
# Author: Nick Sanzotta/@Beamr
# Version: v 1.09282017
try:
	import os, sys, threading, time
	from subprocess import Popen, PIPE
	from wpa_supplicant.core import WpaSupplicantDriver
	from twisted.internet.selectreactor import SelectReactor
	from twisted.internet import task
	from theme import *
	import json, urllib, socket
	import netifaces
except Exception as e:
	print('\n [!] OPENCONNECT - Error: ' % (e))
	sys.exit(1)

class openConnect():
	def __init__(self, ssid, supplicantInt, interface):
			# threading.Thread.__init__(self)
			# self.setDaemon(1) # Creates Thread in daemon mode
			self.ssid = ssid
			self.supplicantInt = supplicantInt
			self.interface = interface
			self.wirelessInt = str(self.interface.get_ifname())
	
	def run(self):
		cls()
		banner()
		curr_time2 = time.time()
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
		# print(interface.get_current_network())

		while True:
			if self.interface.get_state() == 'completed':
				print(' SSID               : ' + ' ' + self.ssid)
				print(' Interface          : ' + ' ' + self.interface.get_ifname())
				print(' Interface Status   : ' + ' ' + self.interface.get_state())
				print(' Authentication     : ' + ' Success: '+ colors.green + '[!]' + colors.normal)
				print(' Elapsed Time       :  %.1fs\n' % (time.time() - curr_time2))
				break
			elif self.interface.get_state() == 'disconnected':
				print(' SSID               : ' + ' ' + self.ssid)
				print(' Interface          : ' + ' ' + self.interface.get_ifname())
				print(' Interface Status   : ' + ' ' + self.interface.get_state())
				print(' Authentication     : ' + ' Failed: '+ colors.red + '[!]' + colors.normal)
				print(' Elapsed Time       :  %.1fs\n ' % (time.time() - curr_time2))
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
				try:
					netifaces.ifaddresses(self.wirelessInt)
					ip = netifaces.ifaddresses(self.wirelessInt)[2][0]['addr']
					print(green('*')+self.wirelessInt.upper() + ' IP Address: ' + ip)
				except Exception as e:
					print('Error Gaining an IP address from DHCP: %s' % (e))
					print('Please wait, or attempt to reconnect\n')
				# Testing Connectivity Check and Portal Page
				try:
					extipAddress = self.get_external_address()
				except (IOError, ValueError) as e:
					print(red('!')+ 'There maybe a signin page')
					pass
				raw_input(normal('*')+'Press Enter to gracefully close the WiFi network connection:')
				# Remove from associated network, which results in state: 'inactive'
				self.interface.remove_network(self.supplicantInt+'/Networks/0')
				# Wait for inactive state, based on a timer.
				time.sleep(7)
				print(normal('i')+'WiFi Connection Terminated. ')
				# self.password.task_done()
		else:
			print('Done')
			# self.password.task_done()

	def get_external_address(self):
		data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
		return data["ip"]