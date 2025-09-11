from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms import SubmitField
from wtforms import IntegerField
from wtforms import SelectField

from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms.validators import NumberRange

METRIC_VALUE = 'metric'
IMPERIAL_VALUE = 'imperial'

PKG_15_MIN = 0
PKG_30_MIN = 1
PKG_HOURLY = 2
PKG_DAILY =  3
PKG_WEEKLY =  4

class SettingsForm(FlaskForm):
    units = RadioField('Units',choices=[(METRIC_VALUE,'Metric'),(IMPERIAL_VALUE,'Imperial')],default=METRIC_VALUE,validators=[DataRequired()])
    frequency = IntegerField('Sample Frequency (minutes)',default=30,validators=[InputRequired(),NumberRange(min=1,message="No negatives!")])
    package_rate = SelectField('Rotate files',choices=[(PKG_15_MIN,'Every 15 Minutes'),(PKG_30_MIN,'Every 30 Minutes'),(PKG_HOURLY,'Hourly'),(PKG_DAILY,'Daily'),(PKG_WEEKLY,'Weekly')],validators=[DataRequired()])
    submit = SubmitField('Save')
    errors = None

    def validate_units(self,units):
        pass
