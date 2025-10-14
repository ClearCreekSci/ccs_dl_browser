import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from ccs_dlconfig import config
from ccs_dlconfig import manifest

app = Flask('DataBrowser')

datapath = '/opt/ccs/WeatherDataLogger/data'
configpath = '/opt/ccs/WeatherDataLogger/settings.cfg'

defaultpassword = 'MeasureYourWorld'

cfg = config.Settings(configpath)
mnfst = manifest.Manifest()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['SECRET_KEY'] = cfg.secret

from databrowser import routes
