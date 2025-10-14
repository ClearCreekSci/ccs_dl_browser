from databrowser import app
from databrowser import bcrypt
from databrowser import cfg
from databrowser import defaultpassword

if '__main__' == __name__:
    if len(cfg.passwd) == 0:
        cfg.passwd = bcrypt.generate_password_hash(defaultpassword).decode('utf-8')
        cfg.write()
    app.run(debug=True,host='0.0.0.0')


