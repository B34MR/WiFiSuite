## The WiFiSuite Project

### Installation for WifiSuite legacy (Python2.7 fix):

    apt install python2-pip-whl
    apt install python2-setuptools-whl
    apt install hostapd-wpe
    cd WiFiSuite
    virtualenv -p /usr/bin/python2.7 venv/
    source venv/bin/activate
    python2.7 -m pip install netifaces
    python2.7 -m pip install psutil
    python2.7 -m pip install twisted
    python2.7 -m pip install txdbus
    python2.7 -m pip install click
    python2.7 -m pip install scapy
    python2.7 setup.py install
    cd wifisuite/
    python2.7 wifisuite.py

### Usage:

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
