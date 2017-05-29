![Supported Python versions](https://img.shields.io/badge/python-2.7-blue.svg)
# WiFiSuite     
    Description: Enterprise WPA Wireless Tool suite.
    
# Installation:
    # git clone https://github.com/NickSanzotta/WiFiSuite.git
    # cd WiFiSuite
    # python setup.py install --record install.log
    # cd wifisuite/
    # python wifisuite.py
    OUTPUT:
	[i] Directory found: data/
 	[!] Database not found: data/WiFiSuite.db
 	[i] Created Datebase: data/WiFiSuite.db
 	[i] Database instantiated

# Uninstall:
    # cd WiFiSuite
    # cat install.log | xargs rm -rf

# Dependencies:
    apt-get install python-pip python-dev
    pip install wpa_supplicant
    pip install psutil
    pip install netifaces
    
# Installation troubleshooting:
    # Error(s) Rasised: 
    # Bad key "patch.force_edgecolor"
    # Rsolution:
    # pip install matplotlib --upgrade

 


    

 
