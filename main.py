from request import request
from request import grab_portland_crime_data
from request import get_bounds
import matplotlib.pyplot as plt

x_data = []
y_data = []

for n in grab_portland_crime_data():
    try:
        x = int(n[-2])
        y = int(n[-1])
    except:
        continue
    x_data = x_data + [x]
    y_data = y_data + [y]

plt.plot( x_data, y_data, 'ro' )
plt.axes(get_bounds(grab_portland_crime_data()))
plt.show()