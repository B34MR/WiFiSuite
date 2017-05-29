![Supported Python versions](https://img.shields.io/badge/python-2.7-blue.svg)
# WiFiSuite     
	WiFiSuite was originally developed to perform Brute-force attacks against Access Points (AP) configured with Extensible Authentication Protocol (EAP) using an Active Directory backend database.
	I recognized if clients/probes were configured to check server side certificates the traditional EvilTwin attack vector would no longer be feasible and a second avenue would need to exists.

	Often us Pentesters perform Password Sprays on internal engagements against hosts running the Server Message Block (SMB) service. Considering EAP is typically configured with only a username and password for authentication backed by Active Directory. I asked myself “why not perform a Password Spray against those same high quality user passwords as SMB?”  
	Tbh probably because I couldn’t find a tool out there that already did this, hence why I began development. 
	
	Admittedly, I discovered performing a Password Spray over WiFi is MUCH slower than on the wire, but it’s a first step and hopefully this process can become more efficient with some clever ideas and engineering. 


## :heavy_exclamation_mark: Requirements
	Kali 2016.1 or Kali 2016.2 rolling. 
	WiFi card is recommended.
	Known working Brands/Models: TP-Link Model TL-WN722N, AWUS036NH, AWUS051NH
    
# Installation:
``` git clone https://github.com/NickSanzotta/WiFiSuite.git
    cd WiFiSuite
    python setup.py install --record install.log ```
    
   ``` # cd wifisuite/
    # python wifisuite.py ```
   ``` OUTPUT:
	[i] Directory found: data/
 	[!] Database not found: data/WiFiSuite.db
 	[i] Created Datebase: data/WiFiSuite.db
 	[i] Database instantiated```

# Uninstall:
    # cd WiFiSuite
    # cat install.log | xargs rm -rf

# Dependencies:
    netifaces
    python-pip 
    python-dev
    psutil
    scapy    
    wpa_supplicant
    
# Installation troubleshooting:
    # Error(s) Rasised: 
   	 Bad key "patch.force_edgecolor"
    # Resolution:
    	 pip install matplotlib --upgrade

 
## :octocat: Credits
	Contributor:  Bill Harshbarger 'https://github.com/bharshbarger'
        Inspiration:  byt3bl33d3r 'https://github.com/byt3bl33d3r/CrackMapExec'
	QA Testers:   jstines, sho-luv, dissect0r

## Disclaimer

***WiFiSuite is intended to be used for legal security purposes only, any other use is not the responsibility of the developer(s). ***
