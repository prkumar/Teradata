from portland import grab_portland_crime_data
import matplotlib.pyplot as plt

x_data=[]
y_data=[]

LATCOEF = 168680.5064887113
LONGCOEF = -5640.630632788689

def color_by_type(type):
    if (type=="Drugs"):
        return "ro"
    if (type=="Liquor Laws"):
        return "rs"
    if (type=="Forgery"):
        return "mo"
    if (type=="Fraud"):
        return "ms"
    if (type=="Trespass"):
        return "cs"
    if (type=="Vandalism"):
        return"co"
    if (type=="Larceny"):
        return "go"
    if (type=="Robbery"):
        return "gs"
    if (type=="Motor Vehicle Theft"):
        return "bo"
    if (type=="Burglary"):
        return "bs"
    if (type=="Aggravated Assault"):
        return "ks"
    if (type=="Assault, Simple"):
        return "ko"
    return "k."

image = plt.imread('portland.png')
plt.imshow(image, zorder=0, extent=[7600000, 7720000 , 620000 , 740000])

for n in grab_portland_crime_data(size=10000):
    try:
        x = int(n[-2])
        y = int(n[-1])
        crime = n[3]
    except:
        continue
    x_data = [x]
    y_data = [y]
    plt.plot(x_data, y_data, color_by_type(crime))



#plt.axis(get_bounds(grab_portland_crime_data()))
plt.axis([7600000, 7720000, 620000 , 740000])
plt.show()