#!/usr/bin/env python2
"""WiFiSuite Entry Point."""
try:
    import createdb
    import core
    import os
    import sys
    import signal
    import commands
    from subprocess import check_output, CalledProcessError
except Exception as e:
    print('\n  [!] Error ' + str(e) + '\n')


def kill_process(proc_name):
    """Kill specified process."""
    try:
        pid = int(check_output(['pidof', proc_name]))
        if proc_name == 'NetworkManager':
            nm_option = raw_input(' network-manager is running, would you like to stop this process:[YES] ') or 'yes'
            choice = nm_option.lower()
            yes = set(['yes', 'y', 'ye', ''])
            no = set(['no', 'n'])
            print(' ENTERED: "%s"' % choice + "\n")
            if choice in yes:
                os.system('systemctl stop network-manager')
                print(' network-manager service stoppped.')
                return True
            elif choice in no:
                print(' network-manager service not stopped.')
                print(' Exiting ...')
                sys.exit(0)
                return False
            else:
                sys.stdout.write("Please respond with 'yes' or 'no'")
        else:
            # DEBUG Print statement
            # print(' DEBUG: ' + procName + ' is running under PID: '+ str(pid))
            print(' [i] Preparing to stop: ' + proc_name + '...\n')
            # os.pkill('wpa_supplicant')
            os.kill(pid, signal.SIGKILL)
            return pid
            returncode = 0
    except CalledProcessError as ex:
        o = ex.output
        print(o)
        returncode = ex.returncode
        # Another Error Occured
        if returncode != 1:
            raise


def run():
    """Run sanity checks, then launch core."""
    createdb.dbcheck()
    # Kill network manager service, if running.
    kill_process('NetworkManager')
    # Kill hostapd-wpe processes, if running.
    kill_process('hostapd-wpe')
    # Detect existing WiFiSuite processes.
    script_name = os.path.basename(__file__)
    wifisuite_pid = commands.getstatusoutput("ps aux | grep -e '%s' | grep -v grep | awk '{print $2}'" % script_name)
    num_process = len(wifisuite_pid[1]) / 4
    print(' [i] Wifisuite processes detected: %s' % (num_process))
    # If another WiFiSuite instance is running other than this instance, do not kill wpa_supplicant.
    if num_process == 1:
        kill_process('wpa_supplicant')
        print(' [i] wpa_supplicant service stopped.')
    print(' [i] Sanity checks completed.')

    core.main()

if __name__ == '__main__':
    run()
