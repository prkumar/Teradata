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


def request(query, user, pw):
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

if __name__ == '__main__':
    wsUser = 'hack_user11'
    wsPass = 'tdhackathon'

    # printing portland crime
    print json.dumps(request('select * from crime_data.portland_crime', wsUser, wsPass), indent=4, sort_keys=True)

    # looking for min, max x and y
    xs = []
    ys = []
    for data in request('select * from crime_data.portland_crime', wsUser, wsPass)["results"][0]["data"]:
        xs.append(data[-2])
        ys.append(data[-1])

    print len(xs), len(ys)




