'''
' Filename: models.py
' Author: Gabriel 'solstice' Ryan
' Description: I can't be bothered to fill this in right now lololol
'
'
'''

import os

from flask import Flask
from flask_socketio import SocketIO

#from models import ___
#from flask_login import ___

smashd = Flask(__name__)
smashd.config.from_pyfile('./config.py')

socketio = SocketIO(smashd)

# db = ___

from smashd import models, views
