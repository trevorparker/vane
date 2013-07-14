vane
====

[![Build Status](https://travis-ci.org/trevorparker/vane.png?branch=devel)](https://travis-ci.org/trevorparker/vane)

Simple weather library in Python.

## Using the library

The library is very much a work in progress. Refer to the `weather-now`
reference utility for a working example. Simply,

```
import vane
w = vane.fetch_weather('New York, NY')
temperature = w['current']['temperature'][0]
temperature_units = w['current']['temperature'][1]
summary = w['current']['summary'][0]
```

## Included utilities

### weather-now

Current weather in a single line.

Example usage:

```
# weather-now New York
# Broken clouds with a temperature of 88°F
#
```

```
# weather-now --units metric London, UK
# Few clouds with a temperature of 22°C
#
```

```
# weather-now --provider wund --api-key beef00d00feed00d 90210
# Haze with a temperature of 76°F
#
```
