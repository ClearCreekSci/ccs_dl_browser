import os

from flask import Flask

from ccs_dlconfig import config

VERSION = 1

app = Flask('DataBrowser')
app.config['SECRET_KEY'] = '808524e95e823a592019dc45e8101fe3244220eeff2bde0b031fb712fb8e188f'

datapath = '/opt/ccs/WeatherLogger/data'

cfg = config.Settings()

from databrowser import routes
