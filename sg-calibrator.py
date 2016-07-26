import sniffer
import json
import os
import cPickle
import time

from argparse import ArgumentParser
from multiprocessing import Process
from configs import *

def channel_hopper():

    import sniffer
    while True:

        for channel in xrange(1, 14):

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

    return parser.parse_args().__dict__

if __name__ == '__main__':

    configs = set_configs()
    interface = configs['iface']

    whitelist = {}
    calibration_table = {
            'len' : 0,
            'calibrated_count' : 0,
            'calibrated' : False,
            'ssids' : {},
    }

    hopper = Process(target=channel_hopper, args=())
    hopper.daemon = True
    hopper.start()

    with open('whitelist.txt') as fd:
    
        for line in fd:
    
            line = line.split()
            ssid = line[0]
            bssid = line[1].lower()
    
            if ssid in whitelist:
                whitelist[ssid].add(bssid)
                calibration_table['ssids'][ssid]['bssids'][bssid] = {
                                            'calibrated' : False,
                                            'packets' : [],
                                            'len' : 0,
                                        }
                calibration_table['ssids'][ssid]['len'] += 1
    
            else:
                whitelist[ssid] = set()
                whitelist[ssid].add(bssid)
                calibration_table['ssids'][ssid] = {
                                        'bssids' : {
                                            bssid : {
                                                'calibrated' : False,
                                                'packets' : [],
                                                'len' : 0,
                                            }, 
                                        },
                                        'calibrated_count' : 0,
                                        'calibrated' : False,
                                        'len' : 1,
                }
                calibration_table['len'] += 1
    
    probe_responses = sniffer.response_sniffer(interface)
    
    print json.dumps(calibration_table, indent=4, sort_keys=True)
    
    for response in probe_responses:
    
        ssid = response['essid']
        bssid = response['addr3'].lower()
        tx = response['tx']
    
        print '[probe_response]', ssid, bssid, tx
    
        ''' so ugly '''
        if ssid in calibration_table['ssids']:
    
            if bssid in calibration_table['ssids'][ssid]['bssids']:
    
                if not calibration_table['ssids'][ssid]['calibrated']:
    
                    if not calibration_table['ssids'][ssid]['bssids'][bssid]['calibrated']:
    
                        calibration_table['ssids'][ssid]['bssids'][bssid]['packets'].append(tx)
                        calibration_table['ssids'][ssid]['bssids'][bssid]['len'] += 1
    
                        if calibration_table['ssids'][ssid]['bssids'][bssid]['len'] >= CALIBRATION_TX_COUNT:
    
                            calibration_table['ssids'][ssid]['bssids'][bssid]['calibrated'] = True
    
                            calibration_table['ssids'][ssid]['calibrated_count'] += 1
                            if calibration_table['ssids'][ssid]['calibrated_count'] >= calibration_table['ssids'][ssid]['len']:
    
                                calibration_table['ssids'][ssid]['calibrated'] = True
                                calibration_table['calibrated_count'] += 1
    
                                if calibration_table['calibrated_count'] >= calibration_table['len']:
    
                                    calibration_table['calibrated'] = True
                                    break
    
            print json.dumps(calibration_table, indent=4, sort_keys=True)

    ssids = calibration_table['ssids']
    for s in ssids:
    
        for bssid in ssids[s]['bssids']:
            
            tx_list = ssids[s]['bssids'][bssid]['packets']
            tx_list_len = ssids[s]['bssids'][bssid]['len']
    
            mean =  sum(tx_list) / tx_list_len
            max_dev = max(abs(el - mean) for el in tx_list)

            upper_bound = mean + (max_dev * N_TIMES_MAX_DEV) 
            lower_bound = mean - (max_dev * N_TIMES_MAX_DEV) 
    
            ssids[s]['bssids'][bssid]['mean'] = mean
            ssids[s]['bssids'][bssid]['max_dev'] = max_dev
            ssids[s]['bssids'][bssid]['upper_bound'] = upper_bound
            ssids[s]['bssids'][bssid]['lower_bound'] = lower_bound

    with open(r'calibration_table.pickle', 'wb') as fd:

        cPickle.dump(calibration_table, fd)

    with open(r'whitelist.pickle', 'wb') as fd:

        cPickle.dump(whitelist, fd)
    
    print json.dumps(calibration_table, indent=4, sort_keys=True)

    hopper.terminate()
