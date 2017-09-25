#!/usr/bin/env python2
# Module: database.py
# Description: Creates Database and Tables
# Author(s): Nick Sanzotta / Bill Harshbarger
# Version: v 1.09232017
try:
	import os, sqlite3
	from theme import *
except Exception as e:
	print('\n  [!] Error ' % (e))

def createdatabase(db_path):
		try:
			conn = sqlite3.connect(db_path, check_same_thread=False) # KEEP Thread Support
			# Define Cursor
			cur = conn.cursor()

			cur.execute('''CREATE TABLE IF NOT EXISTS ap(
				ID INTEGER PRIMARY KEY,
				location text,
				signal text, 
				bssid text, 
				channel text,
				essid text,
				security text, 
				client_id integer,
				Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
				FOREIGN KEY(client_id) REFERENCES engagement(ID)
				)''')

			cur.execute('''CREATE TABLE IF NOT EXISTS identity(
				ID INTEGER PRIMARY KEY, 
				identity text,
				essid text,
				Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
				)''')

			cur.execute('''CREATE TABLE IF NOT EXISTS eapcreds(
				ID INTEGER PRIMARY KEY, 
				identity text,
				password text,
				essid text,
				Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
				)''')

			cur.execute('''CREATE TABLE IF NOT EXISTS eaphashes(
				ID INTEGER PRIMARY KEY, 
				identity text,
				hash text,
				essid text,
				Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
				)''')
			
			cur.execute('''CREATE TABLE IF NOT EXISTS wpakeys(
				ID INTEGER PRIMARY KEY, 
				password text,
				essid text,
				Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
				)''')

			#####################################
			# cur.execute('''CREATE TABLE engagement(
			# 	ID INTEGER PRIMARY KEY,
			# 	name text, 
			# 	contact text,
			# 	location text,
			# 	Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
			# 	UNIQUE(name)
			# 	)''')
			# #https://documentation.meraki.com/MR/WiFi_Basics_and_Best_Practices/802.11_Association_process_explained
			# cur.execute('''CREATE TABLE probes(
			# 	ID INTEGER PRIMARY KEY,
			# 	probe_ssid text,
			# 	mac_addr text,
			# 	FOREIGN KEY(mac_addr) REFERENCES wificlient(mac_addr)
			# 	)''')
			# #store ap details. location, signal strength, channel, bssid, essid, associate w/client id
			# #how to associate ap to users. 1 ap > many users, yes?
			# cur.execute('''CREATE TABLE ap(
			# 	ID INTEGER PRIMARY KEY,
			# 	location text,
			# 	signal text, 
			# 	bssid text, 
			# 	channel text,
			# 	essid text,
			# 	security text, 
			# 	client_id integer,
			# 	Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
			# 	FOREIGN KEY(client_id) REFERENCES engagement(ID)
			# 	)''')
			# #store captured user creds (not psk). logs client probe, captured eap ID, pass, location, and associates w/client id
			# cur.execute('''CREATE TABLE creds(
			# 	ID INTEGER PRIMARY KEY, 
			# 	probe text, 
			# 	identity text, 
			# 	password text,
			# 	location text,
			# 	essid text,
			# 	bssid text, 
			# 	client_id integer,
			# 	Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
			# 	FOREIGN KEY(probe) REFERENCES wificlient(probe),
			# 	FOREIGN KEY(client_id) REFERENCES engagement(ID),
			# 	FOREIGN KEY(essid) REFERENCES ap(essid), 
			# 	FOREIGN KEY(bssid) REFERENCES ap(bssid)
			# 	)''')
	
			# #store client data. probe info, identiity from creds table, password from creds table and client id
			# cur.execute('''CREATE TABLE wificlient(
			# 	ID INTEGER PRIMARY KEY, 
			# 	security text,
			# 	mac_addr text,
			# 	probe text, 
			# 	identity text,
			# 	password text, 
			# 	client_id integer,
			# 	Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
			# 	FOREIGN KEY(client_id) REFERENCES engagement(ID),
			# 	FOREIGN KEY(identity) REFERENCES creds(identity),
			# 	FOREIGN KEY(password) REFERENCES creds(password),
			# 	FOREIGN KEY(security) REFERENCES security(type),
			# 	FOREIGN KEY(probe) REFERENCES probes(probe_ssid) 
			# 	)''')
			# #store PSK details for non enterprise wifi nets, link to bssid, essid, client and sec type
			# cur.execute('''CREATE TABLE psk(
			# 	ID INTEGER PRIMARY KEY,
			# 	security text, 
			# 	psk text, 
			# 	bssid text,
			# 	essid text,
			# 	client_id integer,
			# 	Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
			# 	FOREIGN KEY(essid) REFERENCES ap(essid), 
			# 	FOREIGN KEY(bssid) REFERENCES ap(bssid),
			# 	FOREIGN KEY(client_id) REFERENCES engagement(ID),
			# 	FOREIGN KEY(security) REFERENCES security(type)
			# 	)''')
			# #store encountered types: wpa, wpa2-psk, wpa2-enterperise, etc
			# cur.execute('''CREATE TABLE security(
			# 	ID INTEGER PRIMARY KEY,
			# 	type text)
			# 	''')
			# Commit and Close
			conn.commit()
			conn.close()
			print(blue('*')+'Database instantiated')
		except sqlite3.Error as e:
			print(red('!')+'Cound not create database: %s' % e)

def dbcheck():
	db_name = 'WiFiSuite.db'
	db_dir = str(os.path.expanduser('data/'))
	db_path = os.path.join(db_dir, db_name)
	# If directory ~/.eapSuite/' does not exists
	# Create ~/.eapSuite/' and 'eap.db'
	createdatabase(db_path)
	if not os.path.exists(db_dir):
		print(red('!') + 'Directory not found: ' + db_dir) 
		os.makedirs(db_dir)
		print(blue('i') + 'Created Directory: ' + db_dir)
		createdatabase(db_path)	
		print(blue('i') +'Created Database: ' + db_path)
	elif not os.path.exists(db_path):
		print(blue('i') + 'Directory found: ' + db_dir)
		print(red('!') + 'Database not found: ' + db_path)
		print(blue('i') + 'Created Datebase: ' + db_path)
		createdatabase(db_path)
	else:
		print(blue('i') + 'Using Existing Database: ' + db_path)
		pass
dbcheck()