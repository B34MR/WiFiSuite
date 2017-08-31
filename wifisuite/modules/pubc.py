# Module: PubC
# Description:
# Author: Nick Sanzotta
# Contributors: 
# Version: v 1.08312017
try:
	import os, sys, time, datetime, signal, threading
	from subprocess import Popen, PIPE
	from theme import *
except Exception as e:
	print('\n [!] Error ' +str(e))

class crtb(threading.Thread):
	def __init__(self, certname, email, dryrun, debug):
		threading.Thread.__init__(self)
		self.setDaemon(0) # Creates thread in non-daemon mode
		self.certname = certname
		self.email = email
		self.dryrun = dryrun
		self.debug = debug

	def run(self):
		self.dependency_check()
		# httpProc.wait()

		if self.debug:
			print(white('Debug')+'Certbot STDOUT/STDERR below:')
		
		if self.dryrun:
			p1 = Popen(["certbot", "-n", "--dry-run",  "certonly", "--standalone", "--preferred-challenges", "http", "-m " + self.email, "-d " + self.certname], stdout=PIPE, stderr=PIPE)
		else:
			p1 = Popen(["certbot", "-n", "certonly", "--standalone",  "--agree-tos", "-m " + self.email, "-d " + self.certname], stdout=PIPE, stderr=PIPE)
			# httpProc = Popen(["python", "-m", "SimpleHTTPServer", "80"], stdout=PIPE, stderr=PIPE)
			# time.sleep(30)

		if self.debug:
			# print(p1.communicate())
			for line in iter(p1.stdout.readline, ''):
				sys.stdout.write(line)

			for line in iter(p1.stderr.readline, ''):
				sys.stderr.write(line)
		# else:

		# print('Saving Certs to: data/certs/DOMAIN/')
		# self.server_cert = 'data/certs/DOMAIN'
		# self.private_key = 'data/certs/DOMAIN'

	def external_ip(self):
		print('Place holder')

	def dependency_check(self):
		'''Checks if hostapd-wpe is installed, if not installs it'''
		p1 = Popen(['which', 'certbot'], stdout=PIPE)
		if p1.communicate()[0]:
			p2 = Popen(["certbot", "--version"], stdout=PIPE, stderr=PIPE)
			if self.debug:
				print(white('Debug')+'Running %s' % (p2.communicate()[1]))
		else:
			print(blue('i')+'Installing certbot ...')
			p3 = Popen(['apt-get install -y certbot'], shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
			p3.wait()
			print(' [*] Installation completed')
			os.system('which certbot')
			os.system('certbot --version')
			print('\n')