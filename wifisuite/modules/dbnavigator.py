#!/usr/bin/env python2
# Module: dbnavigator.py
# Description: Interactive CLI (Navigator) for Database queries
# Author(s): Nick Sanzotta
# Version: v 1.09282017
try:
	import os, sys, cmd, sqlite3
	from theme import *
	from dbcommands import DB
	from createdb import dbcheck # This needs to be removed
except Exception as e:
	print('\n [!] DATABASE NAVIGATOR  - Error: ' % (e))
	sys.exit(1)

class Navigator(cmd.Cmd):
	def __init__(self, db_path):
		cmd.Cmd.__init__(self)
		self.prompt = 'WiFiSuite > '
		self.db_path = db_path
		try:
			from dbcommands import DB
			self.db = DB(self.db_path)
		except Exception as e:
			print(red('!')+'DATABASE NAVIGATOR - Could not connect to database: %s' % (e))
			sys.exit(1)

	def do_ap(self, args):
		# Displays all Access Points captured from SCAN. \n Filter Auth Type: ap <AUTH> \n Example: ap 802.1x
		print(' %-3s %-12s %-5s %-3s %-8s %-13s %-32s %s' % \
			 ('ID', 'Location', 'PWR', 'Ch', 'Auth', 'BSSID', 'ESSID', 'Last Seen'))
		print(' %-3s %-12s %-5s %-3s %-8s %-13s %-32s %s' % \
		     ('--','--------','---', '--', '-----', '------------','----------------', '--------------------'))
		try:
			table = self.db.get_ap(args)
			for row in table:
				print(' %-3s %-12s %-5s %-3s %-8s %-13s %-32s %s ' % \
				(row[0], row[1], row[2].replace(' dBm',''), row[4], row[6], row[3], row[5].replace('"',''), row[8]))
		except Exception as e:
			print(red('!')+'DATABASE NAVIGATOR - Could not connect to database: %s' % (e))
			sys.exit(1)
	
	def do_identities(self, args):
		# Displays all Identities captured from ENUM.
		print(' %-3s %-13s %-30s %-8s' % \
			 ('ID', 'ESSID', 'Identity', 'Last Seen'))
		print(' %-3s %-13s %-30s %-8s' % \
			 ('--',  '--------', '---------', '--------------------'))
		try:
			table = self.db.get_identity()
			for row in table:
				print(' %-3s %-13s %-30s %-8s ' %\
				(row[0], row[2], row[1], row[3]))
		except Exception as e:
			print(red('!')+'DATABASE NAVIGATOR - Could not connect to database: %s' % (e))
			sys.exit(1)

	def do_eapcreds(self, args):
		# Displays all EAP Credentials.\n Filter ESSID Type: eapcreds <ESSID> \n Example: eapcreds CompanyWiFi
		print(' %-3s %-13s %-17s %-80s %s' % \
			 ('ID', 'ESSID', 'Identity', 'Password', 'Last Seen'))
		print(' %-3s %-13s %-17s %-80s %s' % \
		     ('--', '--------', '---------', '--------', '--------------------'))
		try:
			table = self.db.get_eapcreds(args)
			for row in table:
				print(' %-3s %-13s %-17s %-80s %s' %\
				(row[0], row[3], row[1], row[2], row[4]))
		except Exception as e:
			print(red('!')+'DATABASE NAVIGATOR - Could not connect to database: %s' % (e))
			sys.exit(1)
	
	def do_eaphashes(self, args):
		# Displays all EAP Hashes.\n Filter ESSID Type: eaphashes <ESSID> \n Example: eaphashes CompanyWiFi
		print(' %-3s %-15s %-17s %-80s %s' % \
			 ('ID', 'ESSID', 'Identity', 'Hash', 'Last Seen'))
		print(' %-3s %-15s %-17s %-80s %s' % \
		     ('--', '--------', '---------', '--------', '--------------------'))
		try:
			table = self.db.get_eaphashes(args)
			for row in table:
				print(' %-3s %-15s %-17s %-80s %s' %\
				(row[0], row[3], row[1], row[2], row[4]))
		except Exception as e:
			print(red('!')+'DATABASE NAVIGATOR - Could not connect to database: %s' % (e))
			sys.exit(1)

	def do_wpakeys(self, args):
		# Displays all WPA Pre-Shared Keys.\n Filter ESSID Type: wpakeys <ESSID> \n Example: wpakeys CoffeeShop
		print(' %-3s %-20s %-22s %-13s' % \
			 (' ID', 'ESSID', 'Password', 'Last Seen'))
		print('%-3s %-20s %-22s %-13s' % \
			 (' --', '------------------', '---------', '--------------------'))
		try:
			table = self.db.get_wpakeys(args)
			for row in table:
				print(' %-3s %-20s %-22s %-13s' %\
				(row[0], row[2], row[1], row[3]))
		except Exception as e:
			print(red('!')+'DATABASE NAVIGATOR - Could not connect to database: %s' % (e))
			sys.exit(1)

	def do_exit(self,args):
		# Terminates Script.
		print('Exiting ...')
		sys.exit(1)

	def do_quit(self,args):
		# Terminates Script.
		print('Exiting ...')
		sys.exit(1)