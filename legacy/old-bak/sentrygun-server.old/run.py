import time
import json
import os

from argparse import ArgumentParser
from smashd import smashd, socketio

def set_configs():

    parser = ArgumentParser()

    parser.add_argument('--port',
            required=False,
            type=int,
            default=80,
            help='Run server on this port')

    parser.add_argument('--host',
            required=False,
            type=str,
            default='0.0.0.0',
            help='Run server on this address')

    parser.add_argument('--debug',
            action='store_true',
            default=False,
            help='Run in debug mode.')

    args = parser.parse_args()

    smashd.config.port = args.port
    smashd.config.host = args.host
    smashd.config.debug = args.debug

def display_banner():

    print '''
                      __                                     
  ______ ____   _____/  |________ ___.__. ____  __ __  ____  
 /  ___// __ \\ /    \\   __\\_  __ <   |  |/ ___\\|  |  \\/    \\ 
 \\___ \\\\  ___/|   |  \  |  |  | \\/\\___  / /_/  >  |  /   |  \\
/____  >\\___  >___|  /__|  |__|   / ____\\___  /|____/|___|  /
     \\/     \\/     \\/             \\/   /_____/            \\/ 


                    version 1.0.0
                    Gabriel Ryan <gryan@gdssecurity.com>
                    Gotham Digital Science
    '''

    print 'Starting on %s:%d . . .' % (smashd.config.host, smashd.config.port)
    print 'Debug mode is', 'on' if smashd.config.debug else 'off'

def main():

    set_configs()

    display_banner()

    print '[*] Starting redis-server daemon...'
    ''' i'm sorry '''
    os.system('redis-server 2>&1 1>/dev/null ./redis.conf &')

    time.sleep(2)

    print '[*] Starting SentryGun server...'
    
    try:
    
        print '[*] SentryGun server is running ...'
    
        socketio.run(smashd,
                    host=smashd.config.host,
                    port=smashd.config.port,
                    debug=smashd.config.debug)

    except KeyboardInterrupt:

        print '[*] Gracefully shutting down redis-server'

        # yep, "gracefully"
        os.system('for i in `pgrep redis-server`; do kill $i; done')
        os.system('rm -f dump.rdb')

    print '[*] Goodbye!'

if __name__ == '__main__':
    main()
