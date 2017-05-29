#!/usr/bin/env python2
# Module: database.py
# Description:
# Author(s): Nick Sanzotta / Bill Harshbarger
# Version: v 1.05162017

try:
	import os, sys, cmd, sqlite3
	from theme import *
	from dbcommands import DB
	from createdb import dbcheck
except Exception as e:
	print('\n [!] Error: ' +str(e))
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
            print(red('!') + 'Could not connect to database: ' + str(e))
            sys.exit(1)

	def print_header(self):
		print(' ID  ESSID         Identity      Password  ')
		print(' --  --------      ---------     --------  ')

	def do_ap(self, args):
		"""Displays all Access Points captured from SCAN.
Filter Auth Type: ap <AUTH> 
Example: ap 802.1x
		"""
		table = self.db.get_ap(args)
		print(' ID  Location     PWR   Ch   AUTH    BSSID         ESSID                            Last Seen')
		print(' --  --------     ---   --   -----   ------------  ----------------                 -------------------- ')
		for row in table:
			print(' %-3s %-12s %-5s %-3s %-8s %-13s %-30s   %s ' %\
			(row[0], row[1], row[2].replace(' dBm',''), row[4], row[6], row[3], row[5].replace('"',''), row[8]))
	
	def do_identities(self, args):
		"""Displays all Identities captured from ENUM.
		"""
		print(' ID  ESSID         Identity      Last Seen ')
		print(' --  --------      ---------     -------------------- ')
		table = self.db.get_identity()
		for row in table:
			print(' %-3s %-13s %-13s %-8s ' %\
			(row[0], row[2], row[1], row[3]))

	def do_eapcreds(self, args):
		"""Displays all EAP Credentials.
Filter ESSID Type: eapcreds <ESSID> 
Example: eapcreds CompanyWiFi
		"""
		print(' ID  ESSID         Identity      Password      Last Seen ')
		print(' --  --------      ---------     --------      -------------------- ')
		table = self.db.get_eapcreds(args)
		for row in table:
			print(' %-3s %-13s %-13s %-13s %s' %\
			(row[0], row[3], row[1], row[2], row[4]))

	def do_wpakeys(self, args):
		"""Displays all WPA Pre-Shared Keys.
Filter ESSID Type: wpakeys <ESSID> 
Example: wpakeys CoffeeShop
		"""
		print(' ID  ESSID                Password               Last Seen')
		print(' --  ------------------   ---------              -------------------- ')
		table = self.db.get_wpakeys(args)
		for row in table:
			print(' %-3s %-20s %-22s %-13s' %\
			(row[0], row[2], row[1], row[3]))

	def do_exit(self,args):
		"""Terminates Script."""
		print('Exiting ...')
		sys.exit(1)

	def do_quit(self,args):
		"""Terminates Script."""
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
