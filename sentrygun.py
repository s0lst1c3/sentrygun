#!/usr/bin/env python
# sentrygun
# Gabriel 'solstice' Ryan
# gabriel@solstice.me
# v0.0.1

import random
import requests
import string
import time
import json
import mmh3
import os

from multiprocessing import Queue, Process
from collections import deque
from configs import *
from argparse import ArgumentParser
from socketIO_client import SocketIO, BaseNamespace
from network_tools import traceroute, wifi_connect

shitlist = Queue()
deauth_list = Queue()
napalm_list = Queue()

def alert_factory(location=None,
                bssid=None,
                channel=None,
                essid=None,
                tx=None,
                intent=None):

    # all arguments are required
    assert not any([
                location is None,
                bssid is None,
                channel is None,
                essid is None,
                tx is None,
                intent is None,
            ])

    # return dict from arguments
    _id = str(mmh3.hash(''.join([ bssid, str(channel), intent])))

    return {
        
        'id' : _id,
        'location' : location,
        'bssid' : bssid,
        'channel' : channel,
	'tx' : tx,
        'essid' : essid,
        'intent' : intent,
        'timestamp' : time.time(),
    }

def run_canary(iface, essid):

    wifi_connect(iface, essid)

    last_hops = traceroute('google.com')
    try:
        while True:

            time.sleep(5)
            hops = traceroute('google.com')
            if hops != last_hops:
                alert = alert_factory(location=DEVICE_NAME,
                                            bssid='not applicable',
                                            channel=0,
                                            intent='canary tripped!',
                                            essid=essid)
                shitlist.put(alert)

    except KeyboardInterrupt:

        os.system('ifconfig %s down' % iface)

def rand_essid():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in xrange(ESSID_LEN))

def deauth(bssid, client='ff:ff:ff:ff:ff:ff'):


    while True:
        print '[deauth worker] running deauth attack against', bssid
        time.sleep(1)

    #pckt = Dot11(addr1=client, addr2=bssid, addr3=bssid) / Dot11Deauth()
    #while True:

    #    for i in range(64):
    #        if i == 0:
    #            print '[Sentrygun] Deauthing ', bssid
    #        send(pckt)

def napalm(bssid, client='ff:ff:ff:ff:ff:ff'):


    while True:
        print '[deauth] running napalm attack against', bssid
        time.sleep(1)

    # code to connect 100k clients goes here

class PunisherNamespace(BaseNamespace):

    def on_napalm_target(self, *args):
        
        alert = args[0]
        
        napalm_list.put(alert)

        if 'dismiss' in alert:

            print '[punisher] ceasing any existing napalm attacks against', json.dumps(alert, indent=4, sort_keys=True)
    
        else:

            print '[punisher] initiating napalm attack against', json.dumps(alert, indent=4, sort_keys=True)

    def on_deauth_target(self, *args):

        alert = args[0]
        
        deauth_list.put(alert)

        if 'dismiss' in alert:

            print '[punisher] ceasing any existing deauth attack against', json.dumps(alert, indent=4, sort_keys=True)
    
        else:

            print '[punisher] initiating deauth attack against', json.dumps(alert, indent=4, sort_keys=True)

def deauth_scheduler():

    try:


        deauth_treatments = {}
        while True:

            alert = deauth_list.get()
            _id = alert['id']

            if 'dismiss' in alert:

                if _id not in deauth_treatments:
                    continue
                deauth_treatments[_id].terminate()
                del deauth_treatments[_id]

            elif _id in deauth_treatments:
                continue

            else:
                bssid = alert['bssid']

                print '[deauth_scheduler] received new target:', bssid

                deauth_treatments[_id] = Process(target=deauth, args=(bssid,))
                deauth_treatments[_id].daemon = True
                deauth_treatments[_id].start()

    except KeyboardInterrupt:
        pass

def napalm_scheduler():

    try:


        napalm_treatments = {}
        while True:

            alert = napalm_list.get()
            _id = alert['id']

            if 'dismiss' in alert:

                if _id not in napalm_treatments:
                    continue
                napalm_treatments[_id].terminate()
                del napalm_treatments[_id]

            elif _id in napalm_treatments:
                continue

            else:
                bssid = alert['bssid']

                print '[napalm_scheduler] received new target:', bssid

                napalm_treatments[_id] = Process(target=napalm, args=(bssid,))
                napalm_treatments[_id].daemon = True
                napalm_treatments[_id].start()

    except KeyboardInterrupt:
        pass


def punisher(configs):

    socket = SocketIO(configs['server_addr'], configs['server_port'])
    punisher_ns = socket.define(PunisherNamespace, '/punisher')

    try:
        socket.wait()

    except KeyboardInterrupt:

        pass

def listener(configs):

    server_uri = 'http://%s:%d/%s' %\
        (configs['server_addr'], configs['server_port'], SERVER_ENDPOINT)

    try:

        while True:

            alert = shitlist.get()

            print '[alert] %s attack: notifying server at %s' %\
                                       (alert['intent'], server_uri)
            response = requests.post(server_uri, json=alert)
            print '[alert] server at %s acknowledged notification with status code %d' % (server_uri, response.status_code)

    except KeyboardInterrupt:
        pass


def get_responding_aps(probe_responses):

    unique_stations = set([])
    for response in probe_responses:
        
        station = response['addr3']
        if station not in unique_stations:
            unique_stations.add(station)
            yield response

def detect_rogue_ap_attacks():

    import sniffer

    responding_aps = {}
    try:
        if configs['evil_twin']:
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
            channel = response['channel']
            print '[probe Response]', ssid, bssid, response['tx'], channel

            if configs['evil_twin'] and ssid in whitelist:

                if bssid not in whitelist[ssid]:
                    print '[anomaly] %s has ssid: %s but not in whitelist' % (bssid, ssid)

                    alert = alert_factory(location=DEVICE_NAME,
                                        bssid=bssid,
                                        channel=response['channel'],
                                        intent='evil twin - whitelist',
					tx=response['tx'],
                                        essid=ssid)
                    shitlist.put(alert)

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
                    #    alert = alert_factory(location=DEVICE_NAME,
                    #                        bssid=bssid,
                    #                        channel=channel,
                    #                        intent='evil twin - tx',
                    #                        essid=ssid)
                    #    shitlist.put(alert)

                    #else:

                    #    baseline_tx.appendleft(tx)

            elif configs['karma']:

                if bssid in responding_aps:
                     
                    responding_aps[bssid].add(ssid)

                else:
                
                    responding_aps[bssid] = set([])
                    responding_aps[bssid].add(ssid)
                if len(responding_aps[bssid]) > 1:

                    print '[anomaly] %s has sent probe responses for %d SSIDs' % (bssid, len(responding_aps[bssid]))

                    alert = alert_factory(location=DEVICE_NAME,
                                        bssid=bssid,
                                        channel=response['channel'],
                                        intent='karma',
					tx=response['tx'],
                                        essid=ssid)
                    shitlist.put(alert)

    except KeyboardInterrupt:
        pass

def channel_hopper():

    import sniffer
    while True:

        # channel hop from main process
        for channel in xrange(1, 14):

            if configs['karma']:

            	for i in xrange(THRESHOLD):
            	    next_essid = rand_essid()
            	    sniffer.send_probe_requests(interface=interface, ssid=next_essid)

            print '[channel hopper] Switching to channel', channel
            os.system('iwconfig %s channel %d' % (configs['iface'], channel))
            time.sleep(6)

def set_configs():

    parser = ArgumentParser()

    parser.add_argument('-i',
                    dest='iface',
                    required=True,
                    type=str,
                    help='Specify network interface to use')

    parser.add_argument('-a',
                    dest='server_addr',
                    required=True,
                    type=str,
                    help='Send data to server at this address')

    parser.add_argument('-p',
                    dest='server_port',
                    required=False,
                    default=80,
                    type=int,
                    help='Send data to server listening on this port')

    parser.add_argument('--evil-twin',
                    dest='evil_twin',
                    action='store_true',
                    help='detect evil twin attacks')

    parser.add_argument('--karma',
                    dest='karma',
                    action='store_true',
                    help='detect karma attacks')

    parser.add_argument('--canary',
                    dest='canary',
                    type=str,
                    default='',
                    required=False,
                    help='Use canary to detect network drops (must specify essid and dedicated interface in the form essid:interface )')


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


                            Gabriel Ryan <gryan@gdssecurity.com>
                                                                                 
    '''

    configs = set_configs()
    interface = configs['iface']

    daemons = []
    try:
    
        daemons.append(Process(target=detect_rogue_ap_attacks, args=()))

        if configs['canary']:
            canary_configs = configs['canary'].split(':')
            canary_essid = canary_configs[0]
            canary_iface = canary_configs[1]
            daemons.append(Process(target=run_canary, args=(canary_iface, canary_essid,)))

        daemons.append(Process(target=listener, args=(configs,)))
        daemons.append(Process(target=punisher, args=(configs,)))
        daemons.append(Process(target=deauth_scheduler, args=()))
        daemons.append(Process(target=napalm_scheduler, args=()))
        daemons.append(Process(target=channel_hopper, args=()))

        for d in daemons:
            d.start()

    except KeyboardInterrupt:

        for d in running_daemons:

            d.terminate()
            d.join()
