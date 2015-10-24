#!/usr/bin/python

import json
import urllib2
import base64
import zlib

# Overall WS Access Variables
dbsAlias = 'xTD150'
wsHost = 'dragon.teradata.ws'
wsPort = '1080'
path = '/tdrest/systems/' + dbsAlias + '/queries'
wsUser = 'hack_user11'
wsPass = 'tdhackathon'

def request(query, user, pw, rowLimit=1000):
    url = 'http://' + wsHost + ':' + wsPort + path
   
    headers = dict()
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/vnd.com.teradata.rest-v1.0+json'
    headers['Authorization'] = "Basic %s" % base64.encodestring('%s:%s' % (user, pw)).replace('\n', '');

    # Set query bands
    queryBands = dict()
    queryBands['applicationName'] = 'MyApp'
    queryBands['version'] = '1.0'

    # Set request fields. including SQL
    data = dict()
    data['query'] = query
    data['queryBands'] = queryBands
    data['format'] = 'array'
    data['rowLimit'] = rowLimit

    # Build request.
    req = urllib2.Request(url, json.dumps(data), headers)

    # Submit request
    try:
        response = urllib2.urlopen(req)
        # Check if result have been compressed.
        if response.info().get('Content-Encoding') == 'gzip':
            response = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
        else:
            response = response.read()
    except urllib2.HTTPError, e:
        print 'HTTPError = ' + str(e.code)
        response = e.read()
    except urllib2.URLError, e:
        print 'URLError = ' + str(e.reason)
        response = e.read()

    # Parse response to confirm value JSON.
    results = json.loads(response)

    return results


def grab_portland_crime_data(size=1000, just_data=True):
    import os
    fn = os.path.join('portland_crime_data', str(size))
    try:
        with open(fn, 'r') as stream:
            resp = json.load(stream)
    except IOError:
        resp = request('select * from crime_data.portland_crime', wsUser, wsPass, rowLimit=size)
        with open(fn, 'w') as out:
            json.dump(resp, out)
    if just_data:
        resp = resp['results'][0]['data']
    return resp


def get_bounds(data):
    xs_min = xs_max = data[0][-2]
    ys_min = ys_max = data[0][-1]
    for n in data[1:]:
        try:
            x = float(n[-1])
            y = float(n[-2])
        except:
            continue
        if x < xs_min:
            xs_min = x
        if x > xs_max:
            xs_max = x
        if y < ys_min:
            ys_min = y
        if y > ys_max:
            ys_max = y
    print xs_min, xs_max, ys_min, ys_max


def get_coords(value):
    if ' and ' in value:
        addresses = value.split(' and ')
    elif ' block of ' in value:
        coords = value.split(' ')
        address = ' '.join(coords[3:])
        street_numbers = coords[0].split('-')
        addresses = (street_numbers[0] + ' ' + address, street_numbers[1] + ' ' + address)
    else:
        addresses = (value, value)
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(timeout=None)
    loc1 = geolocator.geocode(addresses[0], timeout=None)
    loc2 = geolocator.geocode(addresses[1], timeout=None)
    if loc1 is None:
        if loc2 is None:
            return None
        else:
            loc1 = loc2
    if loc2 is None:
        loc2 = loc1
    return {'addresses': addresses,
            'full addresses': (loc1.address, loc2.address),
            'longitudes': (loc1.longitude, loc2.longitude),
            'latitudes': (loc1.latitude, loc2.latitude)
            }

if __name__ == '__main__':
    # grab data
    response = grab_portland_crime_data()
    print response

    # print min and max of x and y for data
    get_bounds(response)

    # grabbing long and lat
    for x in response:
        print x[4]
        print get_coords(x[4])



