import json

from request import request, wsUser, wsPass


def grab_portland_crime_data(size=100):
    import os
    fn = os.path.join('portland_crime_data', str(size))
    try:
        with open(fn, 'r') as stream:
            resp = json.load(stream)
    except IOError:
        resp = request('select * from crime_data.portland_crime', wsUser, wsPass, rowLimit=size)
        with open(fn, 'w') as out:
            json.dump(resp, out)
    data = []
    length = len(resp['results'][0]['data'])
    for i, point in enumerate(resp['results'][0]['data']):
        coords = get_coords(point[4])
        if coords is not None:
            data.append(CrimeReport(point[1], point[3], coords))
        print str(float(i + 1)/length * 100) + '%'
    return data


def get_bounds(data):
    xs_min = xs_max = data[0].x
    ys_min = ys_max = data[0].y
    for n in data[1:]:
        try:
            x = float(n.x)
            y = float(n.y)
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


class CrimeReport(object):
    def __init__(self, rd, mot, coords):
        # self.record_id = data[0]
        self.report_date = rd
        # self.report_time = data[2]
        self.major_offense_type = mot
        # self.neighborhood = data[5]
        # self.police_precinct = data[6]
        # self.police_district = data[7]
        self.address = coords['full addresses']
        self.longitudes = coords['longitudes']
        self.latitudes = coords['latitudes']
        self.x = min(self.longitudes)
        self.y = min(self.latitudes)

if __name__ == '__main__':
    # grab data
    response = grab_portland_crime_data()
    print response

    # print min and max of x and y for data
    print get_bounds(response)


