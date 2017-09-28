# Module: eapenum.py
# Description: Enumerates insecure Extensible Authentication Protocol (EAP) user identities.
# The Eapenum module will perform a deauthentication attack against a single access point/BSSID,
# while client probes attempt to reconnect Eapenum will sniff for insecure EAP user identities.
# Author(s): Nick Sanzotta
# Version: v 1.09282017
try:
	import os, sys, signal, threading
	from datetime import datetime
	from scapy.all import *
	from theme import *
	from dbcommands import DB
	from helpers import monitormode
except Exception as e:
	print('\n [!] EAPENUM - Error: ' % (e))
	sys.exit(1)
# Keep outside of class eapEnum()
identities = set()
bssid = set()

class eapEnum(threading.Thread):
	def __init__(self, db_path, apmac, timeout, interface, channel):
		threading.Thread.__init__(self)
		self.setDaemon(0) # non-daemon
		self.apmac = apmac
		self.timeout = timeout # must be >0, if you choose not to include a timeout the args must me removed.
		self.interface = interface
		self.channel = channel
		self.counter = 0
		self.userDict = {}
		self.wifiDict = {}
		self.future = time.time()+10 
		self.wirelessInt = str(self.interface.get_ifname())
		self.log_timestamp = '{:%Y-%m-%d_%H:%M:%S}'.format(datetime.now())
		self.identities_log = 'data/identities/ch%s_%s.%s' % (self.channel, self.apmac, self.log_timestamp)
		self.db_path = db_path

	def run(self):
		self.database_connect() # Connect to database
		self.datafolders_check() # Check Identities folder exists
		try:
			print(normal('*')+'Packet sniffing on %s for the next %s seconds.' % (self.wirelessInt, self.timeout))
			print(blue('*')+'Identities Log: %s ' % (self.identities_log))
			print(normal('*')+'(Press Ctrl-C to quit)\n')
			sniff(iface=self.wirelessInt, timeout=self.timeout, prn=self.packethandler, count=0)
			print(normal('*')+'Packet Sniffing Stopped, %s seconds has exceeded: ' % (self.timeout))
			monitormode.monitor_stop(self.wirelessInt)
		except Exception as e:
			# monitormode.monitor_stop(self.wirelessInt)
			print('\n'+red('!')+'Packet Sniffing Aborted: %s' % (e))

	def datafolders_check(self):
		# Creates Identities folder if missing
		identities_directory = 'data/identities'
		if not os.path.exists(identities_directory):
			os.makedirs(identities_directory)

	def packethandler(self, pkt):
		essid = ''
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
				# Filter out Request Identity Packets which produce a NULL entry
				if identity not in 'Request':
					print(green('*')+'%s' % (identity))
					# Write to Identity log.
					with open(self.identities_log, 'a') as f1:
						f1.write(identity)
						f1.write('\n')
					# Commit to database
					try:
						self.db.identity_commit(identity, essid)
					except Exception as e:
						print(red('!')+'WARNING - (EAPENUM) Could not save to database: %s' % (e))

	def database_connect(self):
		try:
			self.db = DB(self.db_path)
		except Exception as e:
			print(red('!')+'WARNING - (EAPENUM) Could not connect to database: %s' % (e))
			pass
