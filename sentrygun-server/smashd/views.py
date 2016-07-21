'''
' Filename: views.py
' Author: Gabriel 'solstice' Ryan
' Description: I can't be bothered to fill this in right now lololol
'
'''

import json
import redis
import time

import models

from flask import render_template, request, Response, session
from flask_socketio import emit, disconnect
from multiprocessing import Process, Queue

from smashd import smashd, socketio

clients = []

socketio_ns = smashd.config['SOCKETIO_NS']
listener_ns = smashd.config['LISTENER_NS']

# EVENTS ----------------------------------------------------------------------

@smashd.route('/alert/add', methods=['POST'])
def on_alert_add():

    # this is vulnerable to DOM based xss and a whole bunch of other
    # bad stuff if i don't later make sure data is properly
    # encoded before being broadcasted to all web clients. maybe whitelist
    # as well. but definitely separate data from code before sending to
    # webclient.

    alert = request.get_json(force=False)

    add_alert(alert)

    return json.dumps({'success' : True})

@smashd.route('/alert/dismiss', methods=['POST'])
def on_alert_dismiss():

    alerts = request.get_json(force=False)

    print alerts
    dismiss_alerts(alerts)

    return json.dumps({'success' : True})

@smashd.route('/napalm', methods=['POST'])
def on_napalm():

    targets = request.get_json(force=False)

    print 'napalm'

    for t in targets:
    
        t = models.retrieve_alert(t)

        print 'napalming', json.dumps(t, sort_keys=True, indent=4)
        launch_napalm(t)
        print 'launching napalm'

    return json.dumps({'success' : True})

@smashd.route('/deauth', methods=['POST'])
def on_deauth():

    targets = request.get_json(force=False)

    print 'deauth'

    for t in targets:
    
        t = models.retrieve_alert(t)

        print 'deauthing', json.dumps(t, sort_keys=True, indent=4)
        launch_deauth(t)
        print 'launching deauth'

    return json.dumps({'success' : True})

@smashd.route('/webcli/connect', methods=['GET'])
def on_webcli_connect():

    # retrieve all current alerts from redis cache
    current_alerts = models.retrieve_alerts()

    print current_alerts

    data = json.dumps(current_alerts)
    response = Response(data, status=200, mimetype='application/json')

    return response

# on_alert_expire is simply an on_alert_dismiss event triggered from redis cache

# ACTIONS ---------------------------------------------------------------------

def dismiss_alerts(alerts):
    
    models.remove_alerts(alerts)

    print 'dismissing'
    emit('dismiss alerts', alerts, namespace=socketio_ns, broadcast=True)

    # stop all current attacks
    for a in alerts:

        a['dismiss'] = True
        launch_napalm(a)
        launch_deauth(a)

def add_alert(alert):
    
    alert = models.store_alert(alert)

    print json.dumps(alert, sort_keys=True, indent=4)

    emit('add alert', alert, namespace=socketio_ns, broadcast=True)

    #r = redis.Redis()

    #r.set('%s:%s' % (alert['id'], alert['location']), alert['location'])
    ##r.expire(alert['id'], 30)
    ##r.expire('%s:%s' % (alert['id'], alert['location']), 30)
    #r.expire('%s:%s' % (alert['id'], alert['location']), 18)
    ##r.expire(alert['id'], 5)

    ## store alert in time based cache
    #if models.store_alert(alert):

    #    emit('add alert', alert, namespace=socketio_ns, broadcast=True)

def launch_napalm(alerts):

    #emit('aaa_response', namespace=listener_ns, broadcast=True)
    emit('napalm_target', alerts, namespace=listener_ns, broadcast=True)

def launch_deauth(alerts):

    #emit('aaa_response', namespace=listener_ns, broadcast=True)
    emit('deauth_target', alerts, namespace=listener_ns, broadcast=True)

# SOCKETIO EVENTS -------------------------------------------------------------


@socketio.on('connected', namespace=socketio_ns)
def watchdog_connect():

    print '%s connected' % (request.sid)
    clients.append(request.sid)

@socketio.on('disconnect request', namespace=socketio_ns)
def watchdog_disconnect_request():

    print '%s disconnected' % (request.sid)
    clients.remove(request.sid)
    
    disconnect()

# VIEWS -----------------------------------------------------------------------

@smashd.route('/')
def index():

    return render_template('index.html')

@smashd.route('/prev')
def prev():

    return render_template('prev.html')

@smashd.route('/map')
def area_map():

    return render_template('map.html')

@smashd.route('/settings')
def settings():

    return render_template('settings.html')

@smashd.route('/logout')
def logout():

    return 'logout page goes here'

dismiss_queue = Queue()

def redis_monitor():

    
    # this is awful but this needs to be ready in three weeks
    import requests

    r = redis.StrictRedis()
    pubsub = r.pubsub()
    pubsub.psubscribe('*')
    for msg in pubsub.listen():

        if 'expired' in msg['channel']:

            msg = msg['data'].split(':')
        
            alert = [{ 'id' : msg[0], 'location' : msg[1] }]
    
            response = requests.post('http://0.0.0.0:80/alert/dismiss', json=alert)

            print 'Sent to self:', response
    
rmon = Process(target=redis_monitor, args=())
rmon.start()
