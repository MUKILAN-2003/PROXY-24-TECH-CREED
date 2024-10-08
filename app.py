import os
import sys
from flask import Flask
from json import load

# from modules.utils import *

STATIC_FOLDER = sys.path[0] + '/static/'
UPLOAD_FOLDER = sys.path[0] + '/static/uploads/'
TEMPLATES_FOLDER = sys.path[0] + '/templates/'

app = Flask(__name__, template_folder=TEMPLATES_FOLDER, static_folder=STATIC_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "SSKEY"
