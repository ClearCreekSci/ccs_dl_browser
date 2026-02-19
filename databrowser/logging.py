'''
    logging.py
    logging for the Data Server 

    Copyright (C) 2026 Clear Creek Scientific

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
import datetime

LOG_SUFFIX      = '_ccs_data_logger.log'
g_log_path      = None

def initlog(cfg):
    global g_log_path
    ts = datetime.datetime.now(datetime.UTC)
    name = ts.strftime('%Y%m%d%I%M%S') + LOG_SUFFIX
    if hasattr(cfg,'log_dir') and None is not cfg.log_dir:
        g_log_path = os.path.join(cfg.log_dir,name)
    else:
        g_log_path = name

def logmsg(cfg,tag,msg):
    global g_log_path
    if None is not g_log_path:
        with open(g_log_path,'a') as fd:
            ts = datetime.datetime.now(datetime.UTC)
            s = ts.strftime('%Y-%m-%d %I:%M:%S ') + '[' + tag + '] ' + msg + '\n'
            fd.write(s)

