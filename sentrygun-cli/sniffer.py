import logging
import time

from multiprocessing import Process, Queue
from configs import BURST_COUNT

def response_sniffer(interface):

    valid = [
        { 
        
            'addr3' : 'ff:ff:ff:aa:aa:aa',
            'essid' : 'starbucks',
            'tx' : 24,
            'timestamp' : time.time(),
            'channel' : 6,
        },
        { 
        
            'addr3' : 'ff:ff:aa:aa:aa:aa',
            'essid' : 'starbucks',
            'tx' : 24,
            'timestamp' : time.time(),
            'channel' : 6,
        },
    ]
    invalid = [
        { 
        
            'addr3' : 'aa:aa:aa:aa:aa:aa',
            'essid' : 'starbucks',
            'tx' : 24,
            'timestamp' : time.time(),
            'channel' : 6,
        },
        { 
        
            'addr3' : 'aa:aa:ff:aa:aa:aa',
            'essid' : 'starbucks',
            'tx' : 24,
            'timestamp' : time.time(),
            'channel' : 6,
        },
        { 
        
            'addr3' : 'aa:aa:ff:aa:aa:aa',
            'tx' : 24,
            'essid' : 'starbucks',
            'timestamp' : time.time(),
            'channel' : 6,
        },
        { 
        
            'addr3' : 'ff:aa:aa:aa:aa:aa',
            'tx' : 24,
            'essid' : 'starbucks',
            'timestamp' : time.time(),
            'channel' : 6,
        },


    ]

    packets = valid + invalid
    for a in packets:
        yield a

def send_probe_requests(interface=None, ssid=None):

    print 'sending probe requests'
    return [

        {
            'addr3' : '11:22:33:11:22:33',
            'essid' : '0234jksflkasd9f89asdfj23lk09',
            'channel' : 6,
            'timestamp' : time.time(),
            'tx' : 24,
        },
        {
            'addr3' : '11:22:33:11:22:33',
            'essid' : '908jsdf9asj3oj09asfjas9832jh',
            'tx' : 24,
            'channel' : 6,
            'timestamp' : time.time(),
        },
        {
            'addr3' : '11:22:33:11:22:33',
            'tx' : 24,
            'essid' : '9djkrjsdfgs9dfuas98jl02asdfa',
            'channel' : 6,
            'timestamp' : time.time(),
        },
        {
            'addr3' : '22:22:33:11:22:33',
            'essid' : 'oisdf098qwjfas9d83k298adsf2s',
            'tx' : 24,
            'channel' : 6,
            'timestamp' : time.time(),
        },
    ]
