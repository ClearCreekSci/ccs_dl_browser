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


