import logging
import time

# set scapy loglevel to ERROR before importing scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all  import *

from configs import BURST_COUNT

PROBE_REQUEST  = 0x4
PROBE_RESPONSE = 0x5

def is_valid_probe_response(packet):

    if not packet.haslayer(Dot11):
        return None

    if packet.subtype != PROBE_RESPONSE:
        return None

    #return extract_valid_probe_data(packet)
    return packet

def extract_probe_data(packet):

    return { 
    
        'addr2' : packet.addr2,
        'addr1' : packet.addr1,
        'addr3' : packet.addr3,
        'essid' : packet[Dot11Elt].info,
	'channel' : int(ord(packet[Dot11Elt:3].info)),
        'tx' : -(256-ord(packet.notdecoded[-6:-5])),
        'len' : packet.len,
        'timestamp' : time.time(),
    }

def response_sniffer(interface):

    while True:
        pkt = sniff(lfilter=is_valid_probe_response, iface=interface, count=1, store=1, timeout=10)

        if len(pkt) > 0:
            try:
                yield extract_probe_data(pkt[0])
            except IndexError:
                continue

def ProbeReq(count=BURST_COUNT,ssid='',dst='ff:ff:ff:ff:ff:ff', interface=None):

    param = Dot11ProbeReq()
    essid = Dot11Elt(ID='SSID',info=ssid)
    rates = Dot11Elt(ID='Rates',info='\x03\x12\x96\x18\x24\x30\x48\x60')
    dsset = Dot11Elt(ID='DSset',info='\x01')
    pkt = RadioTap()\
        /Dot11(type=0,subtype=4,addr1=dst,addr2='00:11:22:33:44:55',addr3='00:11:22:33:44:00')\
        /param/essid/rates/dsset

    print '[karma honeypot] sending 802.11 probe request: SSID=[%s], count=%d' % (ssid,count)
    sendp(pkt,iface=interface,count=count,inter=0.1,verbose=0)

def send_probe_requests(interface=None, ssid=None):

    ProbeReq(ssid=ssid, interface=interface)

