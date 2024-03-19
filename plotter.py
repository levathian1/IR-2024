from gmplot import gmplot
import pandas as pd 
from geopy.distance import geodesic

import math

# TODO: figure out tolerance for speed difference given sensor precision

def haversine(coord1, coord2):
    if(math.isnan(float(coord2[0]))):
        return -1
    print(coord1, coord2)
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

print(geodesic((48.672945486, 6.153757156), (48.666823756, 6.145844497)).kilometers)

print(df.head())
# Calculate distance and time difference
df['prev_latitude'] = df['latitude(deg)'].shift(-1)
df['prev_longitude'] = df['longitude(deg)'].shift(-1)
if(pd.isna(df['prev_latitude'].shift(-1).any()) == False):
    df['distance'] = df.apply(lambda x: haversine((x['latitude(deg)'], x['longitude(deg)']), (x['prev_latitude'], x['prev_longitude'])), axis=1)
    df['time_diff'] = (df['Time'] - df['Time'].shift()).dt.total_seconds() / 3600  # Convert seconds to hours

# Calculate speed and add a new column to the DataFrame
df['speed'] = df['distance'] / df['time_diff']

# Drop intermediate columns (optional)
df = df.drop(['distance', 'time_diff'], axis=1)

print(df.head())