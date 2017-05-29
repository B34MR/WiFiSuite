# Module: scanner.py
# Description: Scans the WiFi spectrum and saves output to the WiFiSuite database.
# Author: Bill Harshbarger 
# Contributors: Nick Sanzotta/@Beamr
# Version: v 1.05162017
try:
	from scapy.all import *
	from theme import *
	import threading, sched, time, sqlite3, os, sys, signal, re
	from time import sleep
	from subprocess import Popen, PIPE, STDOUT 
	from eapdb import Navigator
	# DB CHECK
	import createdb
except Exception as e:
	print('\n [!] Error ' +str(e))

class apScan(threading.Thread):
	def __init__(self, location, seconds, supplicantInt, interface):
		threading.Thread.__init__(self)
		self.setDaemon(0) # Thread is not a daemon, resolves issues with terminating reactor.
		self.supplicantInt = supplicantInt
		self.interface = interface
		self.location = location
		self.seconds = seconds
		self.wirelessInt = str(self.interface.get_ifname())
		self.iwApDict={}
		self.aps={}
		# ORIGINAL VARS
		self.eapSuitedb = str(os.path.expanduser('data/WiFiSuite.db'))

	def monitor_start(self):
		os.system('ifconfig ' + self.wirelessInt + ' down')
		os.system('iwconfig ' + self.wirelessInt + ' mode managed')
		os.system('ifconfig ' + self.wirelessInt + ' up')
		os.system('iwconfig ' + self.wirelessInt + ' channel ' + str(self.channel))
		os.system('ifconfig ' + self.wirelessInt + ' down')
		os.system('iwconfig ' + self.wirelessInt + ' mode monitor')
		os.system('ifconfig ' + self.wirelessInt + ' up')
		return

	def monitor_stop(self):
		os.system('ifconfig ' + self.wirelessInt + ' down')
		os.system('iwconfig ' + self.wirelessInt + ' mode monitor')
		os.system('ifconfig ' + self.wirelessInt + ' up')
		os.system('ifconfig ' + self.wirelessInt + ' down')
		os.system('iwconfig ' + self.wirelessInt + ' mode managed')
		os.system('ifconfig ' + self.wirelessInt + ' up')
		return

	def signal_handler(self, signal, frame):
		print('You pressed Ctrl+C! Exiting...')
		self.monitor_stop()
		sys.exit(0)

	def dbcommit(self):
		try:
			self.dbconn = sqlite3.connect(self.eapSuitedb)
		except sqlite3.Error as e:
			print("Error: %s" % e.args[0])
		#conn to db
		self.cursor = self.dbconn.cursor()
		#loop results 
		#loop iwlist output
		for key in self.iwApDict.items()[1:]:
			#print key
			b=key[0]
			b=b.replace(':','').strip()
			vals=key[1]
			c, s, si, e = vals
			# DEBUG
			# print(' [i] Committing %s %s %s %s %s to database' % (b,c,s,si,e))	
			try:	
				self.cursor.execute("""INSERT INTO ap 
					(location, bssid, channel, signal, security, essid ) VALUES (?, ?, ?, ?, ?, ?)""", 
					(self.location,b,c,s,si,e))
				self.dbconn.commit()
			except sqlite3.Error as e:
				print(" [-] Database Error: %s" % e.args[0])
		#loop scapy output
		for key in self.aps.items():	
			#print key
			b=key[0]
			b=b.replace(':','').strip()
			vals=key[1]
			c, s, si, e = vals
			print(' [i] Committing %s %s %s %s %s to database' % (b,c,s,si,e))
			try:
				self.cursor.execute("""INSERT INTO ap 
					(location, bssid, channel, signal, security, essid ) VALUES (?, ?, ?, ?, ?, ?)""", 
					(self.location, b,c,s,si,e))

				self.dbconn.commit()
			except sqlite3.Error as e:
				print(" [-] Database Error: %s" % e.args[0])
		#temp code to return entries
		'''self.cursor.execute('SELECT * FROM ap;')
		print self.cursor.fetchall()'''
		self.dbconn.close()

	def output(self):
		'''Display Output to end User'''
		print('  BSSID               CH   PWR     AUTH    ESSID           ')
		print('  -----------------   --   ---     ----    ----------------')
		#print(self.aps)
		for key in self.aps.items():
			print(' '+key[0]),
			vals=key[1]
			c,t,e = vals
			print(c),
			print(t),
			print(e)
		for key in self.iwApDict.items()[1:]:
			#print key
			mac=key[0]
			vals=key[1]
			ch, pwr, auth, essid = vals
			print(' %-20s %-4s %-6s %-7s  %s'%\
			(mac, ch, pwr.replace(' dBm',''), auth, essid))	
		print('\n')

	def run(self):
		# Create iwlist sub process.
		proc = subprocess.Popen(['/bin/bash', '-c','iwlist %s scan' % \
			(self.wirelessInt)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# Display stdout and decode as utf-8
		iwlistOutput = proc.stdout.read().decode('utf-8')
		# get lines
		lines = iwlistOutput.split('\n')
		self.chan=''
		self.signal=''
		self.security=''
		self.essid=''
		self.bssid=''
		self.encryption = ''

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
		self.monitor_stop()
		self.output()
		self.dbcommit()