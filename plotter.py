from gmplot import gmplot
import pandas as pd 
from geopy.distance import geodesic

import math

# TODO: figure out tolerance for speed difference given sensor precision

def haversine(coord1, coord2):
    if(math.isnan(float(coord2[0]))):
        return -1
    # print(coord1, coord2)
    return geodesic(coord1, coord2).kilometers

df = pd.read_csv("Data24_02_1/Fev-12-1er-sans-RTK.txt", sep='\s+')
df = df.drop(0)
df['Time'] = pd.to_datetime(df['Time'])
# df['Time'] = df['Time'].astype(int) / 10**9

# Initialize the map at a given point
gmap = gmplot.GoogleMapPlotter(48.664068070, 6.155966458, 13)

# Add a marker
gmap.marker(48.664068052, 6.155966525, 'cornflowerblue')

gmap.plot(df["latitude(deg)"], df["longitude(deg)"])

# Draw map into HTML file
gmap.draw("my_map.html")

# print(geodesic((48.672945486, 6.153757156), (48.666823756, 6.145844497)).kilometers)

# TODO: find stackoverflow where this was found to credit it

# https://stackoverflow.com/questions/72823034/pandas-calculating-the-speed-between-two-rows-based-on-timestamp-and-coordinates
# lambda function 

print(df.head())
# Calculate distance and time difference
df['prev_latitude'] = df['latitude(deg)'].shift(-1)
df['prev_longitude'] = df['longitude(deg)'].shift(-1)
if(pd.isna(df['prev_latitude'].shift(-1).any()) == False):
    df['distance'] = df.apply(lambda x: haversine((x['latitude(deg)'], x['longitude(deg)']), (x['prev_latitude'], x['prev_longitude'])), axis=1)
    df['time_diff'] = (df['Time'] - df['Time'].shift()).dt.total_seconds() / 3600  # Convert seconds to hours

df['speed'] = df['distance'] / df['time_diff']

df = df.drop(['distance', 'time_diff'], axis=1)

df = df.dropna()

print(df)


#######################################################################################################
# Ajusting based on speed
# check first 10 vals
#       if within given margin of error: keep as is
#       else get closest line with speed val within margin of error and set that as starting speed
# get closest timestamp 

val = 43.8
err_range = 3 # nb of km different between both authorised
new_timestamp = None

df["speed"] = pd.to_numeric(df['speed'])

df2 = df.iloc[:10]

min_val = abs(df2['speed'] - val).min()
min_index = abs(df2['speed'] - val).idxmin()

print(min_index)
print(min_val)

if min_val > err_range:
    new_timestamp = df2.iloc[min_index]["GPST"] + df2.iloc[min_index]["Time"]