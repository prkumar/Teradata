from request import request
from portland import grab_portland_crime_data
from portland import get_bounds
import matplotlib.pyplot as plt

x_data=[]
y_data=[]

def get_points( filter ):
    global x_data, y_data
    for n in grab_portland_crime_data(size=5000):
        try:
            x = int(n[-2])
            y = int(n[-1])
        except:
            continue
        if n[3] == filter:
            x_data = x_data + [x]
            y_data = y_data + [y]

def plot_by_type( type, color ):
    global x_data, y_data
    x_data=[]
    y_data=[]
    get_points(type)
    plt.plot( x_data, y_data, color)

plot_by_type( "Aggravated Assault", "bo" )
plot_by_type( "Assault, Simple", "co" )
plot_by_type( "Burglary", "ko" )
plot_by_type( "Drugs", "ys" )
plot_by_type( "Forgery", "go" )
plot_by_type( "Fraud", "yo" )
plot_by_type( "Larceny", "mo" )
plot_by_type( "Liquor Laws", "rs" )
plot_by_type( "Motor Vehicle Theft", "ks" )
plot_by_type( "Robbery", "gs" )
plot_by_type( "Trespass", "cs" )
plot_by_type( "Vandalism", "ms" )

plt.axes(get_bounds(grab_portland_crime_data()))
plt.show()

