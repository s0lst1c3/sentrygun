import json

from argparse import ArgumentParser
from smashd import smashd, socketio

HOST = 'localhost'
PORT = 80

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

        banner text here

    '''

    print 'Starting on %s:%d . . .' % (smashd.config.host, smashd.config.port)
    print 'Debug mode is', 'on' if smashd.config.debug else 'off'

def main():

    set_configs()

    display_banner()
    
    socketio.run(smashd,
                host=smashd.config.host,
                port=smashd.config.port,
                debug=smashd.config.debug)

if __name__ == '__main__':
    main()
