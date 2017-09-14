#!/usr/bin/env python2
# __future__ must be imported at start of script.
from __future__ import print_function
try:
	import sys, time
	import threading
	# CLI Arguments  #CHECK might integrate theme
	import arguments
	from Queue import Queue
	# WPA Supplicant required libs
	from wpa_supplicant.core import WpaSupplicantDriver
	from twisted.internet.selectreactor import SelectReactor
	from twisted.internet import task
	# Tab Complete lib
	import readline
	readline.parse_and_bind("tab: complete")
	from theme import *
	# Import Modules
	from modules import eapenum
	from modules import eapspray
	from modules import eapconnect
	from modules import wpabrute
	from modules import wpaconnect
	from modules import scanner
	from modules import openconnect
	from modules import macchange
	from modules import database
	from modules import eviltwin
	from modules import pubc
	from helpers import deauthentication
	from helpers import monitormode

except Exception as e:
	print(' [!] Error: ' + str(e))
	sys.exit(1)

def main():
	# Create Arguments
	args = arguments.parse_args()
	# Set Queue to infinite
	Queue_user = Queue(maxsize=0) #CHECK queue may remove this feature.
	Queue_password = Queue(maxsize=0) #CHECK queue may remove this feature.

    # Argpparse Vars 
	mode = args.mode
	ssid = args.ssid
	user = args.user
	password = args.password
	channel = args.channel
	apmac = args.deauth
	packets = args.packets
	seconds = args.seconds
	location = args.location
	macaddress = args.mac
	# EAP Cert Vars
	# ca_cert = '/opt/my_scripts/ProjectEAP/eapSpray/RadiusServer.pem' 
	# server_cert = args.server_cert # Not a requirement, if defined it must point to correct ca_cert else connection will fail.
	server_cert_path = ''
	client_cert = ''
	#EvilTwin Vars
	certname = args.certname
	public = args.public
	server_cert = args.server_cert
	private_key = args.private_key
	country = args.country
	band = args.band
	state = args.state
	city = args.city
	company = args.company
	ou = args.ou
	email = args.email
	debug = args.debug



	# Launch DATABASE module if called from CLI.
	if mode in 'database':
		database.main()
		reactor.callFromThread(reactor.stop)
	# If DATABASE was not called, Launch Twisted Reactor and creates supplicant interface.
	else:
		# Starts Twisted Reactor in the background via reactorThread
		reactor = SelectReactor()
		reactorThread = threading.Thread(target=reactor.run, \
			kwargs={'installSignalHandlers': 0}, name='Reactor thread').start()
		# let reactor start
		time.sleep(0.1)
		# Start Driver
		driver = WpaSupplicantDriver(reactor)
		# Connect to the supplicant, which returns the "root" D-Bus object for wpa_supplicant
		supplicant = driver.connect()

		# Create interface in wpa supplicant
		try:
			interface0 = supplicant.create_interface(args.interface)
		except Exception as e:
			print(' [!] Error: ' + str(e))
			reactor.callFromThread(reactor.stop)
			sys.exit(1)

		# Assigns interface 0 Supplicant Interface 0
		supplicantInt0 = supplicant.get_interfaces()[0]
		
		# User(s) value from CLI Args
		try:
			# Read users from a file.
			userList = args.user
			with open(userList, 'r') as f1:
				x = f1.read()
			userList = x.split()
			# Create user queue
			Queue_user.put(userList)
		except IOError:
			# Read user(s) given as a value on the CLI seperated by commas
			userList=userList.split(',')
			Queue_user.put(userList)
		except TypeError:
			# If arg does not have user option, pass.
			pass

		# Password(s) value from CLI Args
		try:
			# Read passwords from a file.
			passwordList = args.password
			with open(passwordList, 'r') as f1:
				x = f1.read()
				z = ' '.join([w for w in x.split() if len(w)>7])
				print(' Passwords less than 8 Characters have been excluded. ')
				passwordList = z.split()
				# Create password queue
				Queue_password.put(passwordList)
		except IOError:
			# Read password(s) given as a value on the CLI seperated by commas
			passwordList = passwordList.split(',')
			# Verify password(s) is at least 8 chars.
			for password in passwordList:
				# print(len(x))
				if len(password) < 7:
					print(' Password(s) must be atleast 8 Characters. ')
					print(' Invalid: '+'('+password+')')
					reactor.callFromThread(reactor.stop)
					sys.exit(1)
			# Create password queue
			Queue_password.put(passwordList)
		except TypeError:
			# If arg does not have password option, pass.
			pass

	# MODULE Menu
	if mode in 'scan':
		# I may remove threading for scanner, as there not much need.
		seconds = 5
		apscanT1 = scanner.apScan(location, seconds, supplicantInt0, interface0).start()
		reactor.callFromThread(reactor.stop)
	elif mode in 'eviltwin':
		# Consider placing macchange inside the evilTwin class.
		if macaddress:
			macchange.macManual(interface0, macaddress)
		elif not macaddress:
			macchange.macRandom(interface0)
		# Time not needed, but provides smoother exit.
		time.sleep(.5)
		eviltwinT1 = eviltwin.evilTwin(interface0, ssid, channel, macaddress, certname, public, band, server_cert, \
			private_key, country, state, city, company, ou, email, debug).start()
		# Time not needed, but provides smoother exit.
		time.sleep(.5) 
		reactor.callFromThread(reactor.stop)
	elif mode in 'enum':
		# Place interface in Monitor mode, prior to DeAuth and Enum
		wirelessInt = str(interface0.get_ifname())
		monitormode.monitor_start(wirelessInt, channel)

		try:
			# Create Enum-Sniffing Thread (non-daemon)
			enum_Thread = eapenum.eapEnum(apmac, seconds, interface0, channel)
			enum_Thread.start()
			time.sleep(2.5)
			# Create a deAuth Thread (non-daemon)
			deAuth_Thread = deauthentication.deAuth(apmac, packets, interface0)
			deAuth_Thread.start()
		except KeyboardInterrupt:
			print('\n'+red('!')+'Ctrl-C detected: ')
			monitormode.monitor_stop(wirelessInt)
		# Stop reator Thread / Terminate script
		reactor.callFromThread(reactor.stop)

	elif mode in 'spray':
		print(blue('i')+ 'Using Interface(s): '+str(interface0.get_ifname()))
		'''Determines if Brute-force attack will be EAP or WPA by checking if the USER parameter is present'''
		if user:
			# initiates eapSpray worker thread
			eapSprayT1 = eapspray.eapSpray(ssid, Queue_user, userList, password, server_cert,\
			server_cert_path, client_cert, supplicantInt0, interface0).start()
			# Starts Queue
			Queue_user.join()
			# Stops Twisted Reactor after the Queue is empty.
			def check_stop_flag():
				if Queue_user.empty() == True:
					reactor.callFromThread(reactor.stop)
			lc = task.LoopingCall(check_stop_flag)
			lc.start(10)
		else:
			# initiates wpaBrute worker thread
			wpaBruteT1 = wpabrute.wpaBrute(ssid, Queue_password, passwordList, supplicantInt0,\
			interface0).start()
			# Starts Queue
			Queue_password.join()
			def check_stop_flag():
				if Queue_password.empty() == True:
					reactor.callFromThread(reactor.stop)
			lc = task.LoopingCall(check_stop_flag)
			lc.start(10)

	elif mode in 'connect':
		'''Determines if Connection will be EAP or WPA by checking if the USER parameter is present'''
		if user:
			# initiates eapConnect worker thread
			eapConnectT1 = eapconnect.eapConnect(ssid, Queue_user, password, server_cert,\
			server_cert_path, client_cert, supplicantInt0, interface0).start()
			# Starts Queue
			Queue_user.join()
			# Stops Twisted Reactor after the Queue is empty.
			def check_stop_flag():
				if Queue_user.empty() == True:
					reactor.callFromThread(reactor.stop)
			lc = task.LoopingCall(check_stop_flag)
			lc.start(10)
		elif password:
			# initiates wpaConnect worker thread
			wpaConnectT1 = wpaconnect.wpaConnect(ssid, Queue_password, supplicantInt0, interface0).start()
			# Waits until Queue is Empty and all Threads are done working.
			Queue_password.join()
			# Stops Twisted Reactor after the Queue is empty.
			def check_stop_flag():
				if Queue_password.empty() == True:
					reactor.callFromThread(reactor.stop)
			lc = task.LoopingCall(check_stop_flag)
			lc.start(10)
		else:
			openconnect.openConnect(ssid, supplicantInt0, interface0).run()
			reactor.callFromThread(reactor.stop)
	elif mode in 'mac':
		if macaddress:
			macchange.macManual(interface0, macaddress)
		elif not macaddress:
			macchange.macRandom(interface0)
		# Time not needed, but provides smoother exit.
		time.sleep(.5) 
		reactor.callFromThread(reactor.stop)