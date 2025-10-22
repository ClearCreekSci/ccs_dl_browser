'''
    models.py
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
'''

from flask_login import UserMixin

from databrowser import login_manager
from databrowser import cfg

@login_manager.user_loader
def load_user(user_id):
    return Admin()

class Admin(UserMixin):
    id = 1 
    username = 'admin'
    password = cfg.passwd

    def __repr__(self):
        s = 'name: ' + self.username
        s += ', phash: ' + self.password


