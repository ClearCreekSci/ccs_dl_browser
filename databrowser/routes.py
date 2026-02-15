'''
    routes.py
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

import os
import pathlib
import zipfile

from io import BytesIO

from datetime import datetime

from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import send_file
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required


from databrowser import app
from databrowser import cfg
from databrowser import mnfst
from databrowser import bcrypt
from databrowser.models import Admin

from databrowser import ccs_base

from databrowser import forms

DOWNLOAD_SUFFIX                      = '_ccs_logger.zip'

def get_most_recent_file_path(dirpath):
    rv = None
    most_recent = 0
    files = os.listdir(dirpath)
    for f in files:
        parts = f.split('_')
        ts = int(parts[0])
        if ts > most_recent:
            most_recent = ts
            rv = os.path.join(dirpath,f)
    return rv

def parse_most_recent():
    #global cfg
    rv = list()
    header = None
    data = None
    datafile = get_most_recent_file_path(cfg.data_dir)
    if None is not datafile:
        with open(datafile,'r') as fd:
            for line in fd:
                if None is header:
                    header = line
                data = line
        if None is not header and None is not data:
            header_parts = header.split(',')
            data_parts = data.split(',')
            if len(header_parts) == len(data_parts):
                idx = 0
                for hp in header_parts:
                    # Skip the date and time 
                    if 0 == idx:
                        idx += 1
                        continue
                    hp = hp.strip()
                    label = ccs_base.getName(hp)
                    value = ccs_base.getValue(hp,data_parts[idx],cfg.use_metric)
                    value += ' ' + ccs_base.getUnits(hp,cfg.use_metric)
                    rv.append((label,value))
                    idx += 1
    return rv

def parse_data():
    #global cfg
    rv = list()
    data = None
    files = os.listdir(cfg.data_dir)
    files.sort()
    fidx = 0

    for f in files:
        header = None
        datafile = os.path.join(cfg.data_dir,f)
        with open(datafile,'r') as fd:
            for line in fd:
                if None is header:
                    header = list()
                    cooked_header = list()
                    parts = line.split(',')
                    for part in parts:
                        part = part.strip()
                        header.append(part)
                        name = ccs_base.getName(part)
                        if ccs_base.UNKNOWN == name:
                            cooked_header.append(part)
                        else:
                            s = name + ' ' + ccs_base.getUnits(part,cfg.use_metric)
                            cooked_header.append(s)
                    if fidx == 0:
                        rv.append(cooked_header)
                else:
                    parts = line.split(',')
                    data = list()
                    didx = 0
                    for part in parts:
                        part = part.strip()
                        name = ccs_base.getName(header[didx])
                        if name == ccs_base.UNKNOWN: 
                            data.append(part)
                        else:
                            v = ccs_base.getValue(header[didx],part,cfg.use_metric)
                            data.append(str(v))
                        didx += 1
                    rv.append(data)
        fidx += 1
    return rv

def download_files(entries):
    #global cfg

    if 0 == len(entries):
        return render_template('download.html',title='Download',files=os.listdir(cfg.data_dir))
    ts = datetime.now()
    dst = ts.strftime('%Y%m%d%I%M%S') + DOWNLOAD_SUFFIX
    with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as zippy: 
        for entry in entries:
            path = os.path.join(cfg.data_dir,entry)
            with open(path,'rt') as fd:
                data = ''
                header = list()
                for line in fd:
                    parts = line.split(',')
                    if len(data) == 0:
                        idx = 0
                        for part in parts:
                            part = part.strip()
                            s = ''
                            header.append(part)   
                            name = ccs_base.getName(part)
                            if ccs_base.UNKNOWN == name:
                                if 0 == idx:
                                    s = part
                                else:
                                    s = ',' + part
                            else:
                                units = ccs_base.getUnits(part,cfg.use_metric)
                                if 0 == idx:
                                    s = name + ' ' + units
                                else:
                                    s = ',' + name + ' ' + units
                            data += s
                            idx += 1
                        data += '\n'
                    else:
                        idx = 0
                        for part in parts:
                            s = ''
                            part = part.strip()
                            name = ccs_base.getName(header[idx])
                            if 0 == idx:
                                if ccs_base.UNKNOWN == name:
                                    s = part
                                else:
                                    s = ccs_base.getValue(header[idx],part,cfg.use_metric)
                            else:
                                if ccs_base.UNKNOWN == name:
                                    s = ',' + part
                                else:
                                    s = ',' +  ccs_base.getValue(header[idx],part,cfg.use_metric)
                            data += s
                            idx += 1
                        data += '\n'
            if None is not data:
                zippy.writestr(os.path.basename(path),data,compress_type=zipfile.ZIP_DEFLATED)
    return send_file(dst,mimetype='zip',download_name=dst,as_attachment=True) 

def delete_files(entries):
    for entry in entries:
        path = os.path.join(cfg.data_dir,entry)
        if os.path.exists(path):
            pathlib.Path.unlink(path)

def remove_leftovers():
    # When we create the zip files for downloads, they are created in the home directory
    # and never cleaned up. Look for them here and try to delete them...
    files = os.listdir('.')
    for file in files:
        if file.endswith('.zip'):
            pathlib.Path.unlink(file)

def calculate_package_rate(index,frequency):
    rv = 0
    if forms.PKG_15_MIN == index:
        rv = int(15/frequency)
    elif forms.PKG_30_MIN == index:
        rv = int(30/frequency)
    elif forms.PKG_HOURLY == index:
        rv = int(60/frequency)
    elif forms.PKG_DAILY == index:
        rv = int(1440/frequency)
    elif forms.PKG_WEEKLY == index:
        rv = int(10080/frequency)
    else:
        print('[calculate_package_rate] Unrecognized index: ' + str(index))
    return rv

def calculate_package_index(package_rate,frequency):
    rv = 0
    x = frequency * package_rate

    if x <= 15:
        rv = forms.PKG_15_MIN
    elif x <= 30:
        rv = forms.PKG_30_MIN 
    elif x <= 60:
        rv = forms.PKG_HOURLY 
    elif x <= 1440:
        rv = forms.PKG_DAILY 
    else:
        rv = forms.PKG_WEEKLY 
    return rv

@app.route('/')
@app.route('/home')
def home():
    d = parse_most_recent()
    if len(d) > 0:
        return render_template('home.html',title='Home',data=d)
    else:
        return render_template('home.html',title='Home',data=None)

@app.route('/history')
def history():
    d = parse_data()
    if len(d) > 0:
        return render_template('history.html',title='History',data=d)
    else:
        return render_template('home.html',title='Home',data=None)

def get_photos():
    global cfg
    rv = list()
    # FIXME:
    files = os.listdir('/opt/ccs/DataLogger/photos')
    for f in files:
       target = os.path.join('/opt/ccs/DataLogger/photos',f)
       link = os.path.join('/home/winslow/base/ccs/dev/software/linux/ccs_dl_browser/static/photos',f)
       if False == os.path.islink(link) or False == os.path.exists(link):
           os.symlink(target,link)
       rv.append((f,'photos/' + f,target))
    return rv

@app.route('/photos')
def photos():
    v = get_photos()
    return render_template('photos.html',title='Photos',data=v)

@app.route('/graphs')
def graphs():
    return render_template('graphs.html',title='Graphs')

@app.route('/download',methods=['GET','POST'])
@login_required
def download():
    remove_leftovers()
    if 'POST' == request.method:
        entries = request.form.getlist('entry') 
        if 'download' == request.form['action']:
            return download_files(entries)
        elif 'delete' == request.form['action']:
            delete_files(entries)
    return render_template('download.html',title='Download',files=os.listdir(cfg.data_dir))

@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    #global cfg
    form = forms.SettingsForm()
    #form.errors = list()
    if form.validate_on_submit():
        print("Settings form validated!");
        if form.units.data == forms.METRIC_VALUE:
            cfg.use_metric = True
        else:
            cfg.use_metric = False
        cfg.frequency = int(form.frequency.data)
        cfg.package_rate = calculate_package_rate(int(form.package_rate.data),int(form.frequency.data))
        if len(form.password.data) > 0:
            cfg.passwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            logout_user()
        cfg.write()
        return redirect(url_for('home'))
    else:
        if cfg.use_metric:
            form.units.default = forms.METRIC_VALUE
        else:
            form.units.default = forms.IMPERIAL_VALUE
        form.frequency.default = str(cfg.frequency)
        form.package_rate.default = str(calculate_package_index(cfg.package_rate,cfg.frequency))
        form.process()
    return render_template('settings.html',title='Settings',form=form)

@app.route('/about')
def about():
    return render_template('about.html',version=mnfst.version,commit=mnfst.commit,title='About')

#FIXME: error checking needs to be done...
@app.route('/downloadfile/<name>')
@login_required
def downloadfile(name):
    data = None
    path = os.path.join(cfg.data_dir,name)
    with open(path,'rb') as fd:
        data = fd.read()
    return send_file(BytesIO(data),download_name=name,as_attachment=True) 

@app.route('/login',methods=['GET','POST'])
def login():
    #global cfg
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        user = Admin()
        if bcrypt.check_password_hash(cfg.passwd,password):
            login_user(user,True)
            next_page = request.args.get('next')
            if None is not next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html',title='Login',form=form)


