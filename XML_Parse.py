import xml.etree.ElementTree
import pandas as pd
import datetime,time
import numpy as np

alt = []
lat = []
lon = []
t = []
gt = []
gpst = []
e = xml.etree.ElementTree.parse('GpsResults.xml').getroot()


startdate = input("What is the start date and time in the following format (YYYY,MM,DD,HH,MM,SS,ssssss)")
startdate=startdate.split(',')
print(startdate)
a = list(map(int,startdate))
sd = datetime.datetime(a[0],a[1],a[2],a[3],a[4],a[5],a[6])
sd = (time.mktime(sd.timetuple()))
sd = float(sd) + (a[6]/1000000)


for atype in e.findall('Row'):
    alt.append(atype.get('Wgs84Altitude'))
    lat.append(atype.get('Wgs84Latitude'))
    lon.append(atype.get('Wgs84Longitude'))
    t.append(atype.get('DataSrvTime'))

for i in range(len(t)):
    a=(t[i][0:4],t[i][5:7],t[i][8:10],t[i][20:26],t[i][17:19],t[i][14:16],t[i][11:13])
    a = list(map(int, a))
    tt = datetime.datetime(a[0],a[1],a[2],a[6],a[5],a[4],a[3])

    
    gpstime = float(time.mktime(tt.timetuple())) + (a[3]/1000000)
    gpst.append(gpstime)
    gpstimediff = gpstime - sd
    gt.append(gpstimediff)


df = pd.DataFrame({'Altitude':alt,'Latitude':lat,'Longitude':lon,'Time':gt},columns=['Altitude','Latitude','Longitude','Time'])
df['Time'] = round(df['Time'],3)
df = df.set_index('Time')

gpsdf = pd.read_csv('GPS_FLT_KCAR_interp.txt', sep='\s+', header=None, names=['Time','GPSLat','GPSLon','GPSAlt'])
gpsdf = gpsdf.set_index('Time')


alldf=pd.concat([df,gpsdf], axis=1)

alldf = alldf.dropna(subset=['Latitude'])
print(alldf)



