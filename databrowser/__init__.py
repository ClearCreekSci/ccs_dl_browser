import os

from flask import Flask

from ccs_dlconfig import config

VERSION = 1

app = Flask('DataBrowser')

datapath = '/opt/ccs/WeatherDataLogger/data'

cfg = config.Settings()
app.config['SECRET_KEY'] = cfg.secret

from databrowser import routes
