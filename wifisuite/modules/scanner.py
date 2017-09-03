# Module: scanner.py
# Description: Scans the WiFi spectrum and saves output to the WiFiSuite database.
# Author: Bill Harshbarger 
# Contributors: Nick Sanzotta/@Beamr
# Version: v 1.09252017
try:
	from scapy.all import *
	from theme import *
	import threading, sched, time, sqlite3, os, sys, signal, re
	from time import sleep
	from subprocess import Popen, PIPE, STDOUT 
except Exception as e:
	print('\n [!] SCANNER - Error %s' % (e))
	sys.exit(1)

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

class apScan(threading.Thread):
	def __init__(self, location, seconds, supplicantInt, interface):
		threading.Thread.__init__(self)
		self.setDaemon(0) # non-daemon
		self.supplicantInt = supplicantInt
		self.interface = interface
		self.location = location
		self.seconds = seconds
		self.wirelessInt = str(self.interface.get_ifname())
		self.iwApDict={}
		self.chan=''
		self.signal=''
		self.security=''
		self.essid=''
		self.bssid=''
		self.encryption = ''
	
	def run(self):
		# Create iwlist sub process.
		p1 = subprocess.Popen(['/bin/bash', '-c','iwlist %s scan' % \
			(self.wirelessInt)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# Display stdout and decode as utf-8
		iwlistOutput = p1.stdout.read().decode('utf-8')
		lines = iwlistOutput.split('\n')

		# Iterate lines
		for line in lines:
			# Strip weirdness
			line = line.strip()
			if 'Address:' in line: 
				self.bssid = str(':'.join(line.split(':')[1:7]))
			if 'Channel:' in line: 
				self.chan= str(line.split(':')[1])
			if 'Signal level' in line: 
				self.signal=str(line.split('=')[2])
			if 'ESSID:' in line:
				self.essid = str(line.split(':')[1])
			# Determines if Encryption is enable, if not sets the AUTH value to OPEN.
			if 'Encryption key:' in line:
				self.encryption = str(line.split(':')[1])
			if self.encryption == "on":
				if 'Authentication' in line: 
					self.security= str(line.split(':')[1])
			else:
				self.security= ' OPEN'
			# Populate dictionary
			self.iwApDict[self.bssid]=(self.chan, self.signal, self.security, str(self.essid.replace("\x00",' ')))
		self.output()
		self.dbcommit()

		def signal_handler(self, signal, frame):
			print('You pressed Ctrl+C! Exiting...')
			self.monitor_stop()
			sys.exit(0)

	def dbcommit(self):
		#loop results / loop iwlist output
		for key in self.iwApDict.items()[1:]:
			b=key[0]
			b=b.replace(':','').strip()
			vals=key[1]
			c, s, si, e = vals
			try:
				db.ap_commit(self.location, b, c, s, si, e)
			except sqlite3.Error as e:
				print(red('!')+'Database Error: %s' % e.args[0])


	def output(self):
		'''Display Output to end User'''
		print(' %-20s %-4s %-6s %-7s %s' %\
			 ('BSSID', 'CH', 'PWR', 'AUTH', 'ESSID'))
		print(' %-20s %-4s %-6s %-7s %s' % \
		     ('-----------------', '--', '---', '----', '----------------'))
		for key in self.iwApDict.items()[1:]:
			mac=key[0].replace(' ','') # Clean up leading whitespace with replace
			vals=key[1]
			ch, pwr, auth, essid = vals
			print(' %-20s %-4s %-6s %-7s %s'%\
			(mac, ch, pwr.replace(' dBm',''), auth, essid))
		print('\n')