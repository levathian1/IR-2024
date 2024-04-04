import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from geopy.distance import geodesic
import math

# TODO: linking to functions
# TODO: Linking to physics 
# TODO: produce model from this
# TODO: verify function on other files

#########################################################################
# Plot Intensite du courant en fonction de la vitesse (sur les 98 premieres valeurs)
#########################################################################
def amp_over_speed(df):
    """
        Plot Intensite du courant en fonction de la vitesse

        :param df: le dataframe ou extraire les donnees
        :return: returns nothing
    """
    plt.figure(figsize=(12, 6))
    # try resampling data later
    plt.plot(df['Vitesse du véhicule'][2:100], df["Courant"][2:100])
    plt.title("Intensite du courant en fonction de la vitesse")
    plt.ylabel("Intensite courant")
    plt.xlabel('Vitesse du véhicule')

#########################################################################
# Demo moyenne mobile sur l'intensite du courant
#########################################################################
def rolling_avg(df, df_pos, avg_count=3):
    """
        Demo moyenne mobile sur l'intensite du courant

        :param df: le dataframe ou extraire les donnees
        :param df_pos: le dataframe avec donnees gps ou extraire les donnees
        :param avg_count: le nombre d'entrees du df a prendre en compte dans le lissage (default = 3)
        :return: returns nothing
    """
    df['MA_amp'] = df['Courant'].rolling(window=avg_count).mean()

    df['MA_vit'] = df['Vitesse du véhicule'].rolling(window=avg_count).mean()
    df_pos['MA_lon'] = df_pos['latitude(deg)'].rolling(window=avg_count).mean()
    df_pos['MA_lat'] = df_pos['longitude(deg)'].rolling(window=avg_count).mean()
    df_pos['MA_hau'] = df_pos['height(m)'].rolling(window=avg_count).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(df['Temps'][:100], df['MA_amp'][:100])
    plt.title("Moyenne mobile intensite du courant en fonction du temps")
    plt.ylabel("Intensite")
    plt.xlabel('Temps')

#########################################################################
# Interpolation des donnees toutes les 200ms
# https://stackoverflow.com/questions/73210784/how-do-interpolate-values-between-two-date-columns-in-my-pandas-dataframe
#########################################################################
def interp_system(df, df_pos, datestamp, timestamp):
    """
        Interpolation des donnees toutes les 200ms

        :param df: le dataframe ou extraire les donnees
        :param df_pos: le dataframe avec donnees gps ou extraire les donnees
        :param datestamp: la premiere date des donnees gps
        :param timestamp: premier horaire des donnees gps
        :return: returns nothing
    """
    print(df.Temps)

    # Drop all of the average calc added columns to stop spread of nan throughout the table
    df_pos = df_pos.drop('MA_lon', axis=1)
    df_pos = df_pos.drop('MA_lat', axis=1)
    df_pos = df_pos.drop('MA_hau', axis=1)

    df = df.drop('MA_amp', axis=1)
    df = df.drop('MA_vit', axis=1)

    df['Temps'] = pd.to_datetime(df['Temps'], unit='s')
    df['Temps'] = df['Temps'] + pd.Timedelta(hours = timestamp[0], minutes=timestamp[1], seconds=timestamp[2])
    new_date = pd.to_datetime(datestamp, format='%Y/%m/%d')
    df['Temps'] = df['Temps'] + (new_date - df['Temps'].dt.floor('D'))
    # new range
    new_range = pd.date_range(df.Temps.iloc[0], df.Temps.iloc[-1], freq='200L')

    df_pos['time'] = pd.to_datetime(df_pos['GPST'] + ' ' + df_pos['Time'], format='%Y/%m/%d %H:%M:%S.%f')

    print(new_range)
    df.set_index('Temps', inplace=True)
    df_pos.set_index("time", inplace=True)

    print(df_pos)

    df = df.reindex(df.index.union(new_range))

    interp_df = df.interpolate('time')

    print(interp_df)

    merge_df = pd.merge(interp_df, df_pos, left_index=True, right_index=True, how='left')

    print(merge_df)
    print(merge_df.iloc[9])

    merge_df.to_csv("test.csv", sep='\t')

    merge_df_no_nan = merge_df.dropna()

    print(merge_df_no_nan)

#########################################################################
# https://en.wikipedia.org/wiki/Haversine_formula
#########################################################################
def haversine(coord1, coord2):
    """
        Haversine distance calculation 

        :param coord1: la premiere coordonnee gps
        :param coord2: la deuxieme coordonnee gps
        :return: returns distance
    """
    if(math.isnan(float(coord2[0]))):
        return -1
    # print(coord1, coord2)
    return geodesic(coord1, coord2).kilometers

#########################################################################
# Calcul d'un timestamp ideal selon les donnees GPS et vitesse capteur voiture si besoin
#########################################################################
def ajust_curve(df, val = 43.8, err_range=3):
    """
        Calcul d'un timestamp ideal selon les donnees GPS et vitesse capteur voiture si besoin

        :param df: le dataframe
        :param val: la premiere valeur de vitesse de la dataframe contre lequel s'ajsuter
        :param err_range: tolerance de difference de vitesse (en km/h)
        :return: returns datetime stamp
    """
    # val = 43.8
    # err_range = 3 # nb of km different between both authorised
    df['prev_latitude'] = df['latitude(deg)'].shift(-1)
    df['prev_longitude'] = df['longitude(deg)'].shift(-1)
    if(pd.isna(df['prev_latitude'].shift(-1).any()) == False):
        df['distance'] = df.apply(lambda x: haversine((x['latitude(deg)'], x['longitude(deg)']), (x['prev_latitude'], x['prev_longitude'])), axis=1)
        df['time_diff'] = (df['Time'] - df['Time'].shift()).dt.total_seconds() / 3600  # Convert seconds to hours

    df['speed'] = df['distance'] / df['time_diff']

    df = df.drop(['distance', 'time_diff'], axis=1)

    df = df.dropna()

    new_timestamp = None

    df["speed"] = pd.to_numeric(df['speed'])

    df2 = df.iloc[:10]

    min_val = abs(df2['speed'] - val).min()
    min_index = abs(df2['speed'] - val).idxmin()

    print(min_index)
    print(min_val)

    if min_val > err_range:
        new_timestamp = df2.iloc[min_index]["GPST"] + df2.iloc[min_index]["Time"]

    return new_timestamp or -1