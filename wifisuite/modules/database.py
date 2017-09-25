#!/usr/bin/env python2
# Module: database.py
# Description: Interactive CLI (Navigator) for Database queries
# Author(s): Nick Sanzotta / Bill Harshbarger
# Version: v 1.09232017
try:
	import os, sys, cmd, sqlite3
	from theme import *
	from dbcommands import DB
	from createdb import dbcheck
except Exception as e:
	print('\n [!] Error: ' % (e))
	sys.exit(1)

class Navigator(cmd.Cmd):
	def __init__(self, db_path):
		cmd.Cmd.__init__(self)
		self.prompt = 'WiFiSuite > '
        try:
            # Connect to Database 
            # ISSUE/TEMP hardcoded db_path
            conn = sqlite3.connect(str(os.path.expanduser('data/WiFiSuite.db')), check_same_thread=False) # KEEP Thread Support
            conn.text_factory = str # KEEP Interpret 8-bit bytestrings 
            conn.isolation_level = None # KEEP Autocommit Mode
            db = DB(conn)
        except Exception as e:
            print(red('!') + 'Could not connect to database: ' % (e))
            sys.exit(1)

	def do_ap(self, args):
		""" Displays all Access Points captured from SCAN. \n Filter Auth Type: ap <AUTH> \n Example: ap 802.1x """
		print(' %-3s %-12s %-5s %-3s %-8s %-13s %-32s %s' % \
			 ('ID', 'Location', 'PWR', 'Ch', 'Auth', 'BSSID', 'ESSID', 'Last Seen'))
		print(' %-3s %-12s %-5s %-3s %-8s %-13s %-32s %s' % \
		     ('--','--------','---', '--', '-----', '------------','----------------', '--------------------'))
		table = self.db.get_ap(args)
		for row in table:
			print(' %-3s %-12s %-5s %-3s %-8s %-13s %-32s %s ' % \
			(row[0], row[1], row[2].replace(' dBm',''), row[4], row[6], row[3], row[5].replace('"',''), row[8]))
	
	def do_identities(self, args):
		""" Displays all Identities captured from ENUM. """
		print(' %-3s %-13s %-30s %-8s' % \
			 ('ID', 'ESSID', 'Identity', 'Last Seen'))
		print(' %-3s %-13s %-30s %-8s' % \
			 ('--',  '--------', '---------', '--------------------'))
		table = self.db.get_identity()
		for row in table:
			print(' %-3s %-13s %-30s %-8s ' %\
			(row[0], row[2], row[1], row[3]))

	def do_eapcreds(self, args):
		""" Displays all EAP Credentials.\n Filter ESSID Type: eapcreds <ESSID> \n Example: eapcreds CompanyWiFi """
		print(' %-3s %-13s %-17s %-80s %s' % \
			 ('ID', 'ESSID', 'Identity', 'Password', 'Last Seen'))
		print(' %-3s %-13s %-17s %-80s %s' % \
		     ('--', '--------', '---------', '--------', '--------------------'))
		table = self.db.get_eapcreds(args)
		for row in table:
			print(' %-3s %-13s %-17s %-80s %s' %\
			(row[0], row[3], row[1], row[2], row[4]))
	
	def do_eaphashes(self, args):
		""" Displays all EAP Hashes.\n Filter ESSID Type: eaphashes <ESSID> \n Example: eaphashes CompanyWiFi """
		print(' %-3s %-13s %-17s %-80s %s' % \
			 ('ID', 'ESSID', 'Identity', 'Hash', 'Last Seen'))
		print(' %-3s %-13s %-17s %-80s %s' % \
		     ('--', '--------', '---------', '--------', '--------------------'))
		table = self.db.get_eaphashes(args)
		for row in table:
			print(' %-3s %-13s %-17s %-80s %s' %\
			(row[0], row[3], row[1], row[2], row[4]))

	def do_wpakeys(self, args):
		""" Displays all WPA Pre-Shared Keys.\n Filter ESSID Type: wpakeys <ESSID> \n Example: wpakeys CoffeeShop """
		print(' %-3s %-20s %-22s %-13s' % \
			 (' ID', 'ESSID', 'Password', 'Last Seen'))
		print('%-3s %-20s %-22s %-13s' % \
			 (' --', '------------------', '---------', '--------------------'))
		table = self.db.get_wpakeys(args)
		for row in table:
			print(' %-3s %-20s %-22s %-13s' %\
			(row[0], row[2], row[1], row[3]))

	def do_exit(self,args):
		""" Terminates Script."""
		print('Exiting ...')
		sys.exit(1)

	def do_quit(self,args):
		""" Terminates Script."""
		print('Exiting ...')
		sys.exit(1)

def main():
	# ISSUE / FEATURE add define database variables
	# ISSUE db_path does not carry over into class
	db_name = 'WiFiSuite.db'
	db_dir = str(os.path.expanduser('data/'))
	db_path = os.path.join(db_dir, db_name)
	# Database Check
	dbcheck()
	# Begin Interactive ClI prompt
	prompt = Navigator(db_path).cmdloop()

if __name__ == '__main__':
	main()
