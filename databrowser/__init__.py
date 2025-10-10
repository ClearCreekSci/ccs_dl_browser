import os

from flask import Flask

from ccs_dlconfig import config
from ccs_dlconfig import manifest

app = Flask('DataBrowser')

datapath = '/opt/ccs/WeatherDataLogger/data'

cfg = config.Settings()
mnfst = manifest.Manifest()
app.config['SECRET_KEY'] = cfg.secret

from databrowser import routes
