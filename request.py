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
        with open('fn', 'w') as out:
            json.dump(resp, out)
    if just_data:
        resp = resp['results'][0]['data']
    return resp


def get_bounds(data):
    xs_min = xs_max = int(data[0][-2])
    ys_min = ys_max = int(data[0][-1])
    for n in data[1:]:
        try:
            x = float(n[-1])
            y = float(n[-2])
        except:
            continue
        if x < xs_min:
            xs_min = int(x)
        if x > xs_max:
            xs_max = int(x)
        if y < ys_min:
            ys_min = int(y)
        if y > ys_max:
            ys_max = int(y)
    return [xs_min, xs_max, ys_min, ys_max]
