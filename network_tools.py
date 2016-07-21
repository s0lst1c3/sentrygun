import os 

from subprocess import check_output

def traceroute(hostname):

    out = check_output(['traceroute', hostname])
    count = 0
    for line in out.split('\n')[1:]:
        if line:
            count += 1
    return count

def wifi_connect(iface, essid):

    os.system('ifconfig %s down' % iface)
    os.system('iwconfig %s essid %s' % (iface, essid))
    os.system('ifconfig %s up' % iface)

    os.system('dhclient %s' % iface)
