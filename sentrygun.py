#!/usr/bin/env python
# sentrygun
# Gabriel 'solstice' Ryan
# gabriel@solstice.me
# v0.0.1

import random
import string
import time
import json
import smtplib

from email.mime.text import MIMEText
from email.utils import make_msgid
from multiprocessing import Queue, Process
from collections import deque
from configs import *
from argparse import ArgumentParser

ESSID_LEN  = 24

shitlist = Queue()

def rand_essid():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in xrange(ESSID_LEN))

def send_alert(body, subject=DEFAULT_SUBJECT, debug_level=True):
    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) #port 465 or 587
    server.set_debuglevel(debug_level)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SMTP_USER, SMTP_PASS)
    
    for to_addr in ALERT_RECIPIENTS:
    
        msg = MIMEText(body, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = SMTP_USER
        msg['To'] = to_addr
        msg['Message-ID'] = make_msgid()
        server.sendmail(SMTP_USER,[to_addr],msg.as_string())
    
    server.close()

def deauth(bssid, client='ff:ff:ff:ff:ff:ff'):

    pckt = Dot11(addr1=client, addr2=bssid, addr3=bssid) / Dot11Deauth()
    while True:

        for i in range(64):
            if i == 0:
                print '[Sentrygun] Deauthing ', bssid
            send(pckt)

def mitigator():
    
    try:

        deauth_treatments = []
        
        deauthed_bssids = set([])
        while True:

            response = shitlist.get()
            bssid = response['addr3']

            if bssid in deauthed_bssids:
                continue

            print '[banhammer] Recieved new target:', bssid

            if THREAT_MITIGATION_ENABLED:

                print '[banhammer] Launching persistent deauth on:', bssid
                deauthed_bssids.add(bssid)

                p = Process(target=deauth, args=(bssid,))
                p.daemon = True
                p.start()
                deauth_treatments.append(p)

            if ALERTS_ENABLED:

                body = 'Karma attack detected from %s' % bssid
                send_alert(body, 'New IDS Alert')

    except KeyboardInterrupt:
        pass

    for d in deauth_treatments:
    
        d.terminate()
        d.join()

def get_responding_aps(probe_responses):

    unique_stations = set([])
    for response in probe_responses:
        
        station = response['addr3']
        if station not in unique_stations:
            unique_stations.add(station)
            yield response

def detect_evil_twins():

    import sniffer

    try:
        whitelist = {}
        with open('whitelist.txt') as fd:

            for line in fd:

                line = line.split()
                ssid = line[0]
                bssid = line[1]

                if ssid in whitelist:
                    whitelist[ssid].add(bssid)
                else:
                    whitelist[ssid] = set()
                    whitelist[ssid].add(bssid)

        probe_responses = sniffer.response_sniffer(interface)

        recent_tx_values = deque([], 10)

        for response in probe_responses:
        
            ssid = response['essid']
            bssid = response['addr3']

            if ssid in whitelist:

                if bssid not in whitelist[ssid]:
                    print '[Evil Twin Sentry] %s has ssid: %s but not in whitelist' % (bssid, ssid)
                    shitlist.put(response)
                else:
                    pass

                    #baseline_tx = numpy.mean(recent_tx_values)
                    #
                    #range_a = baseline_tx - THRESHOLD
                    #range_b = baseline_tx + THRESHOLD

                    #if range_a > range_b:

                    #    high_lim = range_a
                    #    low_lim = range_b
            
                    #else:

                    #    high_lim = range_b
                    #    low_lim = range_a

                    #tx = response['tx']

                    #if tx > high_lim or tx < low_lim:

                    #    print '[Evil Twin Sentry] Illegal tx varation: %s ' % bssid
                    #    shitlist.put(bssid)

                    #else:

                    #    baseline_tx.appendleft(tx)

    except KeyboardInterrupt:
        pass


def detect_karma_attacks():

    import sniffer

    try:
        while True:

            # use set for fast lookup times, dicts for storing counts and details
            responding_aps = {
                'members' :  set([]),
                'counts' : {},
                'details' : {},
            }

            for i in xrange(THRESHOLD):

                next_essid = rand_essid()
                print '[Karma Sentry] Sending Probe Request %d for: %s' % (i, next_essid)
            
                # call progress bar here based on scapy.sniff's timeout
                probe_responses = sniffer.send_probe_requests(interface=interface, ssid=next_essid)

                for response in get_responding_aps(probe_responses):

                    bssid = response['addr3']

                    if bssid not in responding_aps['members']:
                        responding_aps['members'].add(bssid)
                        responding_aps['counts'][bssid] = 1
                        responding_aps['details'][bssid] = response
                    else:
                        responding_aps['counts'][bssid] += 1


            for bssid in responding_aps['members']:

                if responding_aps['counts'][bssid] >= THRESHOLD:

                    print '[Karma Sentry] Karma attack detected from %s' % bssid
                    print '[Karma Sentry] Adding %s to shitlist' % bssid
                    shitlist.put(responding_aps['details'][bssid])

            time.sleep(3)

    except KeyboardInterrupt:
        pass

def set_configs():

    parser = ArgumentParser()

    parser.add_argument('-i',
                    dest='iface',
                    required=True,
                    type=str,
                    help='Specify network interface to use')

    parser.add_argument('--evil-twin',
                    dest='evil_twin',
                    action='store_true',
                    help='detect evil twin attacks')

    parser.add_argument('--karma',
                    dest='karma',
                    action='store_true',
                    help='detect karma attacks')

    return parser.parse_args().__dict__

if __name__ == '__main__':

    print '''

 _______  _______  _       _________ _______           _______           _       
(  ____ \(  ____ \( (    /|\__   __/(  ____ )|\     /|(  ____ \|\     /|( (    /|
| (    \/| (    \/|  \  ( |   ) (   | (    )|( \   / )| (    \/| )   ( ||  \  ( |
| (_____ | (__    |   \ | |   | |   | (____)| \ (_) / | |      | |   | ||   \ | |
(_____  )|  __)   | (\ \) |   | |   |     __)  \   /  | | ____ | |   | || (\ \) |
      ) || (      | | \   |   | |   | (\ (      ) (   | | \_  )| |   | || | \   |
/\____) || (____/\| )  \  |   | |   | ) \ \__   | |   | (___) || (___) || )  \  |
\_______)(_______/|/    )_)   )_(   |/   \__/   \_/   (_______)(_______)|/    )_)


                            Written by Gabriel "solstice" Ryan

                            gabriel@solstice.me
                                                                                 
    '''

    configs = set_configs()
    interface = configs['iface']

    daemons = []
    try:
    
        if configs['karma']:
            daemons.append(Process(target=detect_karma_attacks, args=()))
        if configs['evil_twin']:
            daemons.append(Process(target=detect_evil_twins, args=()))

        daemons.append(Process(target=mitigator, args=()))

        for d in daemons:

            d.start()

    except KeyboardInterrupt:

        for d in running_daemons:

            d.terminate()
            d.join()
