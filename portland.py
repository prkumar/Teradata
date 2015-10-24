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
    data = []
    for point in resp['results'][0]['data']:
        data.append(CrimeReport(point))
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


class CrimeReport(object):
    def __init__(self, data):
        # self.record_id = data[0]
        self.report_date = data[1]
        # self.report_time = data[2]
        self.major_offense_type = data[3]
        self.address = data[4]
        # self.police_precinct = data[5]
        # self.police_district = data[6]
        self.x = data[7]
        self.y = data[8]
        self.__addresses = None

    @property
    def longitudes(self):
        if self.__addresses is None:
            self.__addresses = get_coords(self.address)
        return self.__addresses['longitudes']

    @property
    def latitudes(self):
        if self.__addresses is None:
            self.__addresses = get_coords(self.address)
        return self.__addresses['latitudes']


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