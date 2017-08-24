#!/usr/bin/env python2
try:
    import sqlite3
except Exception as e:
    print('\n  [!] Error ' +str(e)+'\n')
    sys.exit(1)

class DB:
    def __init__(self, conn):
        self.conn = conn
        # CHECK is cur can be used once as oppose to in each func.
        # cur = self.conn.cursor()

    def get_ap(self, args):
        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM ap WHERE security LIKE "%"""+args+"""%" """)
        # cur.execute(""" SELECT * FROM ap WHERE """+column3+""" LIKE "%"""+args+"""%" """)
        # cur.execute("""SELECT * FROM ap""")# GROUP BY bssid""")
        results = cur.fetchall()
        cur.close()
        return results
    
    def get_identity(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM identity""")
        results = cur.fetchall()
        cur.close()
        return results

    def get_eapcreds(self, args):
        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM eapcreds WHERE essid LIKE "%"""+args+"""%" """)
        # cur.execute("""SELECT * FROM eapcreds""")
        results = cur.fetchall()
        cur.close()
        return results

    def get_wpakeys(self, args):
        cur = self.conn.cursor()
        cur.execute(""" SELECT * FROM wpakeys WHERE essid LIKE "%"""+args+"""%" """)
        # cur.execute("""SELECT * FROM wpakeys""")
        results = cur.fetchall()
        cur.close()
        return results
    
    ### Commits ###
    def ap_commit(self, location, signal, channel, bssid, essid, client_id):
        cur = self.conn.cursor()
        cur.execute("insert into ap (location, signal, channel, bssid, essid, client_id) values (?,?,?,?,?,?)", \
        (location, signal, channel, bssid, essid, client_id))

    def identity_commit(self, identity, essid):
        cur = self.conn.cursor()
        cur.execute("insert into identity (identity, essid) values (?,?)", \
        (identity, essid))

    def eapspray_commit(self, essid, identity, password):
        cur = self.conn.cursor()
        cur.execute("insert into eapcreds (essid, identity, password) values (?,?,?)", \
        (essid, identity, password))

    def eviltwin_commit(self, essid, identity, password):
        cur = self.conn.cursor()
        cur.execute("insert into eapcreds (essid, identity, password) values (?,?,?)", \
            (essid, identity, password))

    def wpabrute_commit(self, essid, password):
        cur = self.conn.cursor()
        cur.execute("insert into wpakeys (essid, password) values (?,?)", \
        (essid, password))
    ###################################################################################
    # def get_engagement(self):
    #     cur = self.conn.cursor()
    #     cur.execute("""SELECT * FROM engagement""")
    #     results = cur.fetchall()
    #     cur.close()
    #     return results

    # def get_probes(self):
    #     cur = self.conn.cursor()
    #     cur.execute("""SELECT * FROM probes""")
    #     results = cur.fetchall()
    #     cur.close()
    #     return results

    # def get_ap(self):
    #     cur = self.conn.cursor()
    #     cur.execute("""SELECT * FROM ap GROUP BY bssid""")
    #     results = cur.fetchall()
    #     cur.close()
    #     return results

    # def get_creds(self):
    #     cur = self.conn.cursor()
    #     cur.execute("""SELECT * FROM creds""")
    #     results = cur.fetchall()
    #     cur.close()
    #     return results

    # def get_iwificlient(self):
    #     cur = self.conn.cursor()
    #     cur.execute("""SELECT * FROM wificlient""")
    #     results = cur.fetchall()
    #     cur.close()
    #     return results

    # def get_psk(self):
    #     cur = self.conn.cursor()
    #     cur.execute("""SELECT * FROM psk""")
    #     results = cur.fetchall()
    #     cur.close()
    #     return results

    # # Commits
    # def engagement_commit(self, name, contact, location):
    #     cur = self.conn.cursor()
    #     cur.execute("insert into engagement (name, contact, location) values (?,?,?)", \
    #     (name, contact, location))

    # def probes_commit(self, probe_ssid, mac_addr):
    #     cur = self.conn.cursor()
    #     cur.execute("insert into probes (probe_ssid, mac_addr) values (?,?)", \
    #     (probe_ssid, mac_addr))

    # def ap_commit(self, location, signal, channel, bssid, essid, client_id):
    #     cur = self.conn.cursor()
    #     cur.execute("insert into ap (location, signal, channel, bssid, essid, client_id) values (?,?,?,?,?,?)", \
    #     (location, signal, channel, bssid, essid, client_id))
    #     '''ap commit from ssid.py
    #     """INSERT INTO ap 
    #                 (bssid, channel, signal, security, essid ) VALUES (?, ?, ?, ?, ?)""", 
    #                 (b,c,s,si,e))'''

    # def cred_commit(self, probe_ssid, identity, password, location, essid, bssid, client_id):
    #     cur = self.conn.cursor()
    #     cur.execute("insert into creds (probe_ssid, identity, password, location, essid, bssid, client_id) values (?,?,?,?,?,?,?)", \
    #     (probe_ssid, identity, password, location, essid, bssid, client_id))

    # def wificlient_commit(self, security, mac_addr, probe_ssid, identity, password, client_id):
    #     cur = self.conn.cursor()
    #     cur.execute("insert into creds (probe_ssid, identity, password, location, essid, bssid, client_id) values (?,?,?,?,?,?,?)", \
    #     (probe_ssid, identity, password, location, essid, bssid, client_id))

    # def psk_commit(self, security, psk, bssid, ess, client_id):
    #     cur = self.conn.cursor()
    #     cur.execute("insert into creds (security, psk, bssid, ess, client_id) values (?,?,?,?,?)", \
    #     (security, psk, bssid, ess, client_id))
 
