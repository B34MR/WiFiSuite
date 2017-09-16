![Supported Python versions](https://img.shields.io/badge/python-2.7-blue.svg)
# WiFiSuite     
WiFiSuite is designed to help Pentesters streamline the process of auditing wireless networks,
this is done by consolidating the most common tools and techniques in a unified platform backed with a SQLite database.


## :book: WiFiSuite Wiki
   [Main](https://github.com/NickSanzotta/WiFiSuite/wiki)<br>
   [EvilTwin](https://github.com/NickSanzotta/WiFiSuite/wiki/EvilTwin) _In Progress_ <br>
   [Enum](https://github.com/NickSanzotta/WiFiSuite/wiki/Enum)<br>
   [Scan](https://github.com/NickSanzotta/WiFiSuite/wiki/Scan) _In Progress_ <br>
   [EAP Spray](https://github.com/NickSanzotta/WiFiSuite/wiki/EAP-Spray) _In Progress_ <br>
   [WPA Brute-force] _In Progress_ <br>
   [WPA Spray] _In Progress_ <br>
   [Quick Connect](https://github.com/NickSanzotta/WiFiSuite/wiki/Quick-Connect) _In Progress_ <br>
   [MAC Changer] _In Progress_ <br>
   [Database] _In Progress_ <br>
   [Average Brute force time](https://github.com/NickSanzotta/WiFiSuite/wiki/Average-Brute-force-time)<br>
   [Troubleshooting](https://github.com/NickSanzotta/WiFiSuite/wiki/Troubleshooting)<br>


## :white_check_mark: Installation
    OS Requirements: 
	Kali Rolling
###
    Dependencies:
        hostapd-wpe
        netifaces
        python-pip 
        python-dev
        psutil
        scapy    
        wpa_supplicant
###	
     Install:
        apt-get install scapy
        git clone https://github.com/NickSanzotta/WiFiSuite.git
        cd WiFiSuite
        python setup.py install --record install.log	
###
     Run:
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

## :pencil: Cheat Sheet
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


## :beers: Credits
	Contributor(s):             Bill Harshbarger 'https://github.com/bharshbarger'
	Inspiration (Database):     byt3bl33d3r 'https://github.com/byt3bl33d3r/CrackMapExec'
	Beta Testers:               ac3lives, dissect0r, jstines, sho-luv

## Disclaimer

***WiFiSuite is intended to be used for legal security purposes only, any other use is not the responsibility of the developer(s). ***
