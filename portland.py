import json

from request import request, wsUser, wsPass


def grab_portland_crime_data(size=1000):
    import os
    fn = os.path.join('portland_crime_data', str(size))
    try:
        with open(fn, 'r') as stream:
            resp = json.load(stream)
    except IOError:
        resp = request('select * from crime_data.portland_crime', wsUser, wsPass, rowLimit=size)
        with open(fn, 'w') as out:
            json.dump(resp, out)
    return resp['results'][0]['data']


def get_bounds(data):
    xs_min = xs_max = data[0][-2]
    ys_min = ys_max = data[0][-1]
    for n in data[1:]:
        try:
            x = float(n[-2])
            y = float(n[-1])
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
    return xs_min, xs_max, ys_min, ys_max


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


def find_avg_coords(d, size=100):
    lats = []
    longs = []
    for point in d[:size]:
        coords = get_coords(point[4])
        if coords is not None:
            lats.append(point[-2]/coords['latitudes'][0])
            longs.append(point[-1]/coords['longitudes'][0])
    return sum(lats)/len(lats), sum(longs)/len(longs)

