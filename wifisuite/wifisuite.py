#!/usr/bin/env python2
try:
	import createdb
	import core
	import os, signal
	from theme import *
	from subprocess import check_output, STDOUT, CalledProcessError
except Exception as e:
	print('\n  [!] Error ' +str(e)+'\n')

def killProcess(procName):
	try:
		pid =  int(check_output(['pidof',procName]))
		if procName == 'NetworkManager':
			nmOption = raw_input(' network-manager is running, would you like to stop this process:[YES] ') or 'yes'
			choice = nmOption.lower()
			yes = set(['yes','y', 'ye', ''])
			no = set(['no','n'])
			print(' ENTERED: "%s"' % choice + "\n")
			if choice in yes:
				# Using os.kill and service network-manager produce different results
				# os.kill the network-manager service is still active but the process is killed.
				# serivice network-manager stop, deactives the service.
				# This can be validated with service network-manager status
				# os.kill(pid, signal.SIGKILL)
				os.system('systemctl stop network-manager')
				# os.pkill('NetworkManager')
				print(' network-manager service stoppped.')
				return True
			elif choice in no:
				print(' network-manager service not stopped.')
				print(' Exiting eapSpray.py')
				sys.exit(0)
				return False
			else:
				sys.stdout.write("Please respond with 'yes' or 'no'")
		else:
			# DEBUG Print statement
			# print(' DEBUG: ' + procName + ' is running under PID: '+ str(pid))
			print(blue('i') + 'Preparing to stop: ' + procName +'...\n')
			# os.pkill('wpa_supplicant')
			os.kill(pid, signal.SIGKILL)	
			return pid 
			returncode = 0
	except CalledProcessError as ex:
		o = ex.output
		returncode = ex.returncode
		# Another Error Occured
		if returncode != 1: 
			raise

def sanityCheck():
	'''Runs sanity checks prior to launching core.'''
	createdb.dbcheck() # ADD if db exists, option to overwrite
	killProcess('NetworkManager')
	killProcess('hostapd-wpe') # EvilTwin process sanitization.
	killProcess('wpa_supplicant')
	print(' [i] Sanity checks completed without errors.')

def run():
	sanityCheck()
	core.main()

if __name__ == '__main__':
	run()




