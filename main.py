from portland import grab_portland_crime_data
import matplotlib.pyplot as plt

x_data=[]
y_data=[]

LATCOEF = 168680.5064887113
LONGCOEF = -5640.630632788689

def get_points(filter):
    global x_data, y_data
    for n in grab_portland_crime_data(size=200000):

        try:
            x = int(n[-2])
            y = int(n[-1])
        except:
            continue
        if n[3] == filter:
            x_data = x_data + [x/LATCOEF]
            y_data = y_data + [y/LONGCOEF]

def plot_by_type( type, color ):
    global x_data, y_data
    x_data=[]
    y_data=[]
    get_points(type)
    plt.plot(x_data, y_data, color)

plot_by_type( "Aggravated Assault", "ks" )
plot_by_type( "Assault, Simple", "ko" )
plot_by_type( "Burglary", "bs" )
plot_by_type( "Drugs", "ro" )
plot_by_type( "Forgery", "mo" )
plot_by_type( "Fraud", "ms" )
plot_by_type( "Larceny", "go" )
plot_by_type( "Liquor Laws", "rs" )
plot_by_type( "Motor Vehicle Theft", "bo" )
plot_by_type( "Robbery", "gs" )
plot_by_type( "Trespass", "cs" )
plot_by_type( "Vandalism", "co" )

#plt.axis(get_bounds(grab_portland_crime_data()))
plt.axis([7600000, 7720000, 620000, 740000])
plt.show()