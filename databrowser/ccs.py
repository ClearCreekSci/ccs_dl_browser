```
    ccs.py
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

CCS_AIR_TEMPERATURE_UUID    = 'a0ce0210-3bbf-11ee-89eb-00e04c400cc5'
CCS_HUMIDITY_UUID           = 'a0ce0211-3bbf-11ee-89eb-00e04c400cc5'
CCS_AIR_PRESSURE_UUID       = 'a0ce0212-3bbf-11ee-89eb-00e04c400cc5'

C_TO_F_CONVERSION = 1.8   # Add 32 after multiplying
MM_HG_CONVERSION = 0.75006
IN_HG_CONVERSION = 0.0295
UNKNOWN = 'Unknown'

def getName(ID):
    rv = UNKNOWN 
    if ID == CCS_AIR_TEMPERATURE_UUID:
        rv = 'Temperature'
    elif ID == CCS_HUMIDITY_UUID:
        rv = 'Humidity'
    elif ID == CCS_AIR_PRESSURE_UUID:
        rv = 'Air Pressure'
    return rv

def getValue(ID,v,metric):
    rv = '' 
    n = float(v)
    if ID == CCS_AIR_TEMPERATURE_UUID:
        if False == metric:
            n *= C_TO_F_CONVERSION
            n += 32
        rv = '{:.{}f}'.format(n,2)
    elif ID == CCS_HUMIDITY_UUID:
        rv = '{:.{}f}'.format(n,2)
    elif ID == CCS_AIR_PRESSURE_UUID:
        if metric:
            n *= MM_HG_CONVERSION 
        else:
            n *= IN_HG_CONVERSION 
        rv = '{:.{}f}'.format(n,2)
    return rv

def getUnits(ID,metric):
    rv = '' 
    if ID == CCS_AIR_TEMPERATURE_UUID:
        if metric:
            rv = '°C'
        else:
            rv = '°F'
    elif ID == CCS_HUMIDITY_UUID:
        rv = '%'
    elif ID == CCS_AIR_PRESSURE_UUID:
        if metric:
            rv = 'mmHg'
        else:
            rv = 'inHg'
    return rv

