# Module: PubC
# Description:
# Author: Nick Sanzotta
# Contributors: 
# Version: v 1.09032017
try:
	import os, sys, time, datetime, signal, threading
	from subprocess import Popen, PIPE
	import SocketServer, SimpleHTTPServer, multiprocessing
	from theme import *
except Exception as e:
	print('\n [!] Error ' +str(e))

class crtb(threading.Thread):
	def __init__(self, certname, email, debug):
		threading.Thread.__init__(self)
		self.setDaemon(0) # Creates thread in non-daemon mode
		self.certname = certname
		self.email = email
		self.debug = debug
		self.cwd = os.getcwd()
		self.webserver_directory = '/var/www/WiFiSuite/'
		self.port = 80

	def run(self):
		self.dependency_check()
		self.datafolders_check()

		# Setup SimpleHTTPServer
		Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
		httpd = SocketServer.TCPServer(("", self.port), Handler)
		httpd.allow_reuse_address = True
		
		# Launch SimpleHTTPServer in a seperate Process
		os.chdir(self.webserver_directory)
		server_process = multiprocessing.Process(target=httpd.serve_forever)
		server_process.daemon = True
		server_process.start()
		print('HTTP Server Launched on Port: %s ' % (self.port))

		# Run Certbot while HTTP Server process is live.
		try:
			p1 = Popen(["certbot", "--webroot", "--non-interactive", "certonly", "--text", "--rsa-key-size", "4096", "--agree-tos", "--webroot-path", "/var/www/WiFiSuite/", "-m " + self.email, "-d " + self.certname], stdout=PIPE, stderr=PIPE)
		except Exception as e:
			print(' Error: %s' % (e))
		if self.debug:
			print(white('Debug')+'Certbot STDOUT/STDERR below:')
			# Print STDOUT
			for line in iter(p1.stdout.readline, ''):
				sys.stdout.write(line)
			# Print STDERR
			for line in iter(p1.stderr.readline, ''):
				sys.stderr.write(line)

		# Terminate HTTP Server process
		server_process.terminate()
		os.chdir(self.cwd)

	def datafolders_check(self):
		'''Creates Web Server directory folder if missing'''
		self.webserver_directory = '/var/www/WiFiSuite/'
		if not os.path.exists(self.webserver_directory):
			os.makedirs(self.webserver_directory)

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