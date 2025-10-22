```
    forms.py
    OpenSCAD model for the CCS Data Logger enclosure

    Copyright (C) 2025 Clear Creek Scientific

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms import SubmitField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import PasswordField

from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms.validators import NumberRange
from wtforms.validators import ValidationError

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
    password = PasswordField('New Password',validators=[])
    confirm_password = PasswordField('Confirm New Password',validators=[])
    submit = SubmitField('Save')
    errors = list()

    def validate_password(self,units):
        if self.password.data != self.confirm_password.data:
            self.errors.append('Passwords must match')
            raise ValidationError('Passwords must match!')


class LoginForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

