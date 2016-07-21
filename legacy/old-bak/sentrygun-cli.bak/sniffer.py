import logging
import time

from multiprocessing import Process, Queue
from configs import BURST_COUNT

def response_sniffer(interface):

    valid = [
        { 
        
            'addr3' : 'ff:ff:ff:aa:aa:aa',
            'essid' : 'starbucks',
            'tx' : 23,
            'timestamp' : time.time(),
            'channel' : 6,
        },
        { 
        
            'addr3' : 'ff:ff:aa:aa:aa:aa',
            'tx' : 23,
            'essid' : 'starbucks',
            'timestamp' : time.time(),
            'channel' : 6,
        },
    ]
    invalid = [
        { 
        
            'addr3' : 'aa:aa:aa:aa:aa:aa',
            'essid' : 'starbucks',
            'tx' : 23,
            'timestamp' : time.time(),
            'channel' : 6,
        },
        { 
        
            'addr3' : 'aa:aa:ff:aa:aa:aa',
            'essid' : 'starbucks',
            'tx' : 23,
            'timestamp' : time.time(),
            'channel' : 6,
        },
        { 
        
            'addr3' : 'aa:aa:ff:aa:aa:aa',
            'essid' : 'starbucks',
            'tx' : 23,
            'timestamp' : time.time(),
            'channel' : 6,
        },
        { 
        
            'addr3' : 'ff:aa:aa:aa:aa:aa',
            'essid' : 'starbucks',
            'timestamp' : time.time(),
            'tx' : 23,
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
            'tx' : 87,
            'channel' : 6,
            'timestamp' : time.time(),
        },
        {
            'addr3' : '11:22:33:11:22:33',
            'essid' : '908jsdf9asj3oj09asfjas9832jh',
            'tx' : 64,
            'channel' : 6,
            'timestamp' : time.time(),
        },
        {
            'addr3' : '11:22:33:11:22:33',
            'essid' : '9djkrjsdfgs9dfuas98jl02asdfa',
            'channel' : 6,
            'tx' : 68,
            'timestamp' : time.time(),
        },
        {
            'addr3' : '22:22:33:11:22:33',
            'essid' : 'oisdf098qwjfas9d83k298adsf2s',
            'tx' : 37,
            'channel' : 6,
            'timestamp' : time.time(),
        },
    ]
