![Supported Python versions](https://img.shields.io/badge/python-2.7-blue.svg)
# WiFiSuite     
	WiFiSuite is a wireless auditing platform for Pentesters.

## :heavy_exclamation_mark: Requirements
	Kali 2016.1 or Kali 2016.2 rolling. 
	External WiFi card, known working Brands/Models: TP-Link Model TL-WN722N, AWUS036NH, AWUS051NH
    
## Installation
	apt-get install scapy
	git clone https://github.com/NickSanzotta/WiFiSuite.git
	cd WiFiSuite
	python setup.py install --record install.log	
##
	cd wifisuite/
	python wifisuite.py
	Output of Successful Installation:
	       [i] Directory found: data/
 	       [!] Database not found: data/WiFiSuite.db
 	       [i] Created Datebase: data/WiFiSuite.db
 	       [i] Database instantiated

## Uninstall
    cd WiFiSuite
    cat install.log | xargs rm -rf

## Dependencies
    hostapd-wpe
    netifaces
    python-pip 
    python-dev
    psutil
    scapy    
    wpa_supplicant
        
## :book: Cheat Sheet
    SCAN:           python wifisuite.py -iwlan0 scan --location="CoffeeShop"
    EVILTWIN (EAP): python wifisuite.py -iwlan0 -s"New Corp WiFi" -m 66:55:44:AB:40:88 -c4 --certname="WiFISuite" --band b eviltwin
    ENUM:           python wifisuite.py -iwlan0 -d 10:10:10:A9:72:E6 -c4 enum --seconds=30 --packets=5
    SPRAY (EAP):    python wifisuite.py -iwlan0 -s"Corp WiFi" -u data/users.txt -pWelcome1 spray
    SPRAY (WPA):    python wifisuite.py -iwlan0 -s"Corp Hotspot" -p data/passwords.txt spray
    CONNECT (EAP):  python wifisuite.py -iwlan0 -s"Corp WiFi" -ubeamr -pWelcome1 connect
    CONNECT (WPA):  python wifisuite.py -iwlan0 -s"CompanyXYZ Hotspot" -p Password123 connect
    CONNECT (Open): python wifisuite.py -iwlan0 -s"CompanyXYZ Hotspot" connect
    MAC (Randomize):python wifisuite.py -iwlan0 mac
    MAC (Manual):   python wifisuite.py -iwlan0 -m 10:10:10:A9:72:E6 mac
    DATABASE:       python wifisuite.py database
##
* SCAN: Perform a quick survey of the 2.4Ghz Wireless Spectrum
     ![](https://github.com/NickSanzotta/img/blob/master/WiFiSuiteSCAN-C.gif)

##
* SPRAY (EAP): Perform a EAP Password Spray against a list of user accounts using a single password.
	       [*] Tip SSID(s) are case sensitive!
	       
     ![](https://github.com/NickSanzotta/img/blob/master/WiFiSuiteSPRAYEAP-A.gif)
##

* CONNECT (EAP): Connect to an EAP Access Point with username and password authentication, after connection has completed 
		 open a new console tab to interact with the network. Ensure to shutdown the connection gracefully to avoid 		     future connectivity issues.
	         [*] Tip SSID(s) are case sensitive!

     ![]( https://github.com/NickSanzotta/img/blob/master/WiFiSuiteCONNECT-A.gif)

## :octocat: Credits
	Contributor(s):             Bill Harshbarger 'https://github.com/bharshbarger'
	Inspiration (Database):     byt3bl33d3r 'https://github.com/byt3bl33d3r/CrackMapExec'
	Beta Testers:               ac3lives, dissect0r, jstines, sho-luv

## Disclaimer

***WiFiSuite is intended to be used for legal security purposes only, any other use is not the responsibility of the developer(s). ***
