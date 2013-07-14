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

def fetch_weather(
        location, units='imperial', with_forecast=False, provider='owm',
        api_key=None):
    w = _fetch_weather_json(location, units, with_forecast, provider, api_key)
    if 'e' in w:
        raise Exception(w['e'])
    if provider == 'owm':
        r = _parse_owm(w, units, with_forecast)
    elif provider == 'wund':
        r = _parse_wund(w, units, with_forecast)
    else:
        raise Exception('Invalid provider selected')
    return r

def _parse_owm(w, units, with_forecast):
    r = {}
    m = {
        'temp': 'temperature', 'humidity': 'humidity',
        'pressure': 'pressure', 'speed': 'wind_spd', 'gust': 'wind_gst',
        'deg': 'wind_dir', '3h': 'rain_3hr', 'description': 'summary'}
    u = {
        'temp': 'fahrenheit', 'humidity': 'percent', 'pressure': 'millibars',
        'speed': 'mph', 'gust': 'mph', 'deg': 'degrees', '3h': 'inches',
        'description': ''}
    if units == 'metric':
        u['temp'] = 'celsius'
        u['speed'] = 'kph'
        u['gust'] = 'kph'
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

def _parse_wund(w, units, with_forecast):
    r = {}
    if units == 'imperial':
        m = {
            'temp_f': 'temperature', 'relative_humidity': 'humidity',
            'pressure_in': 'pressure', 'wind_mph': 'wind_spd',
            'wind_gust_mph': 'wind_gst', 'wind_degrees': 'wind_dir',
            'weather': 'summary'}
        u = {
            'temp_f': 'fahrenheit', 'relative_humidity': 'percent',
            'pressure_in': 'inHg', 'speed': 'mph', 'gust': 'wind_gust_mph',
            'wind_degrees': 'degrees', 'weather': ''}
    if units == 'metric':
        m = {
            'temp_c': 'temperature', 'relative_humidity': 'humidity',
            'pressure_mb': 'pressure', 'wind_kph': 'wind_spd',
            'wind_gust_kph': 'wind_gst', 'wind_degrees': 'wind_dir',
            'weather': 'summary'}
        u = {
            'temp_c': 'celsius', 'relative_humidity': 'percent',
            'pressure_mb': 'millibars', 'wind_mph': 'kph',
            'wind_gust_kph': 'kph', 'wind_degrees': 'degrees', 'weather': ''}
    c = w['c']['current_observation']
    r['current'] = {}
    for key in c:
        if key not in m or key not in u:
            continue
        if key not in r:
            r['current'][key] = []
        r['current'][key].append(w['c']['current_observation'][key])
        r['current'][key].append(u[key])
    r['current'] = dict(
        (m.get(k, k), v) for (k, v) in r['current'].items())
    return r

def _fetch_weather_json(
        location, units, with_forecast, provider, api_key):
    weather_urls = {
        'owm':  'http://api.openweathermap.org/data/2.5/weather?'
                'q={0}&units={1}',
        'wund': 'http://api.wunderground.com/api/{2}/conditions/'
                'q/{0}.json'}
    forecast_urls = {
        'owm':  'http://api.openweathermap.org/data/2.5/forecast?'
                'q={0}&units={1}',
        'wund': 'http://api.wunderground.com/api/{2}/forecast/'
                'q/{0}.json'}
    if provider == 'owm':
        location = urllib.quote_plus(location)
        units = urllib.quote_plus(units)
        weather_url = weather_urls[provider]
        try:
            r = requests.get(weather_url.format(location, units))
            c = json.loads(r.text)
            if (c['cod'] != 200):
                return {'e': c['message']}

            if (with_forecast):
                forecast_url = forecast_urls[provider]
                r = requests.get(forecast_url.format(location, units))
                f = json.loads(r.text)
                if (f['cod'] != 200):
                    return {'e': f['message']}
            else:
                f = None
        except requests.exceptions.ConnectionError as e:
            return {'e': 'Connection error'}
        return {'c': c, 'f': f}
    elif provider == 'wund':
        if api_key == None:
            return {'e': 'API key required for Weather Underground provider'}
        loc_parsed = _parse_location(location)
        units = urllib.quote_plus(units)
        if loc_parsed:
            weather_url = weather_urls[provider]
            try:
                r = requests.get(
                    weather_url.format(loc_parsed, units, api_key))
                c = json.loads(r.text)
                if ('conditions' not in c['response']['features']):
                    return {'e': 'Unable to load current conditions'}
                if ('error' in c['response']):
                    return {'e': c['response']['error']['description']}

                if (with_forecast):
                    forecast_url = forecast_urls[provider]
                    r = requests.get(
                        forecast_url.format(loc_parsed, units, api_key))
                    f = json.loads(r.text)
                    if ('forecast' not in f['response']['features']):
                        return {'e': 'Unable to load forecast'}
                    if ('error' in f['response']):
                        return {'e': f['response']['error']['description']}
                else:
                    f = None
            except requests.exceptions.ConnectionError as e:
                return {'e': 'Connection error'}
            return {'c': c, 'f': f}
        else:
            return {'e': 'Unable to parse location'}

def _parse_location(loc):
    if loc.isdigit():
        return loc
    else:
        loc_list = loc.replace(',','').split()
        if len(loc_list) == 2:
            return "{1}/{0}".format(
                urllib.quote_plus(loc_list[0]),
                urllib.quote_plus(loc_list[1]))
        else:
            return 0
