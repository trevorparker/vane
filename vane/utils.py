# vane utils
#
# Copyright (c) 2013 Trevor Parker <trevor@trevorparker.com>
# All rights reserved
#
# Distributed under the terms of the modified BSD license (see LICENSE)

import json
import requests
import sys
import urllib

def fetch_weather(location, units='imperial', with_forecast=False):
    w = _fetch_weather_json(location, units, with_forecast)
    if 'e' in w:
        raise Exception(w['e'])
    r = _parse_owm(w, units, with_forecast)
    return r

def _parse_owm(w, units, with_forecast):
    r = {}
    m = {
        'temp':'temperature', 'humidity': 'humidity',
        'pressure':'pressure', 'speed':'wind_spd', 'gust':'wind_gst',
        'deg':'wind_dir', '3h':'rain_3hr', 'description':'summary'}
    if units == 'imperial':
        u = {
            'temp':'fahrenheit', 'humidity':'percent', 'pressure':'millibars',
            'speed':'mph', 'gust':'mph', 'deg':'degrees', '3h':'inches',
            'description':''}
    else:
        u = {
            'temp':'celsius', 'humidity':'percent', 'pressure':'millibars',
            'speed':'kph', 'gust':'kph', 'deg':'degrees', '3h':'inches',
            'description':''}
    c = w['c']['main']
    c.update(w['c']['wind'])
    c.update(w['c']['rain'])
    c.update(w['c']['weather'][0])
    r['current'] = {}
    for key in c:
        if key not in m or key not in u:
            continue
        if key not in r:
            r['current'][key] = []
        r['current'][key].append(w['c']['main'][key])
        r['current'][key].append(u[key])
    r['current'] = dict(
        (m.get(k, k), v) for (k, v) in r['current'].items())
    return r

def _fetch_weather_json(location, units, with_forecast=False):
    try:
        location = urllib.quote_plus(' '.join(location))
        weather_url = (
            "http://api.openweathermap.org/data/2.5/weather?"
            "q={0}&units={1}")
        r = requests.get(weather_url.format(location, units))
        c = json.loads(r.text)
        if (c['cod'] != 200):
            return {'e': c['message']}

        if (with_forecast):
            forecast_url = (
                "http://api.openweathermap.org/data/2.5/forecast?"
                "q={0}&units={1}")
            r = requests.get(forecast_url.format(location, units))
            f = json.loads(r.text)
            if (f['cod'] != 200):
                return {'e': f['message']}
        else:
            f = None
    except requests.exceptions.ConnectionError as e:
        return {'e': 'Connection error'}

    return {'c': c, 'f': f}
