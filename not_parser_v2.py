from re import I
import pandas as pd 
import warnings
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

import functions as func

gps_head = "GPST Time latitude(deg) longitude(deg) height(m) Q ns sdn(m) sde(m) sdu(m) sdne(m) sdeu(m) sdun(m) age(s) ratio"
df1_head = "Temps;Vitesse du véhicule;Courant batterie de traction mesuré par LBC"
merge_head = "Time Vitesse du véhicule	Courant batterie de traction mesuré par LBC	Courant"

def replace_header(df, header):
    df.iloc[0] = header

if len(sys.argv) < 3:
    print("""
    Usage:
        - Param 1: donnees d'acquisition
        - Param 2: donnees GPS
    """)


# TODO: Header redefine for used formatting (add Time column to GPS dataframe for easier manip in future)
else:
    df = pd.read_csv(sys.argv[1], sep=';') # premier dataframe, donnee d'acquisition

    df = df.drop(0)
    df = df.drop(1)    

    df['Courant'] = pd.to_numeric(df['Courant batterie de traction mesuré par LBC'].str.replace(',', '.'))
    df["Vitesse du véhicule"] = pd.to_numeric(df['Vitesse du véhicule'].str.replace(',', '.'))
    df['Temps'] = pd.to_numeric(df['Temps'].str.replace(',', '.'))
    df['Courant batterie de traction mesuré par LBC'] = pd.to_numeric(df['Courant batterie de traction mesuré par LBC'].str.replace(',', '.'))
    
    df_pos = pd.read_csv(sys.argv[2], sep='\s+')
    # df_pos = df_pos.drop(0)
    df_pos2 = df_pos.copy()
    df_pos['Time'] = pd.to_datetime(df_pos['Time'])

    # print("here: ", df_pos['Time'].dt.time.iloc[0])

    # donne la difference sur les 10 premiers timestamps possibles en prenant la plus petites sur une fenetre de 10, repete sur les x premiers timestamps (probablement redondant cf 2nd solution en dessous)
    # for i in range(0, 10):
    #     timestamp, res, df, min_ind = func.ajust_curve(df, val = df.iloc[i]["Vitesse du véhicule"])
    #     # https://stackoverflow.com/questions/22276066/how-to-plot-multiple-functions-on-the-same-figure
    #     plt.plot(res, 'r')
    #     plt.plot(df.iloc[min_ind]["Vitesse du véhicule"])
    #     plt.title(f"Vitesse, index premier timestamp = {timestamp}")
    #     plt.show()

    res = [0] * 10
    for i in range(0, 1):
        df2 = df.copy()
        # print(df_pos.head())
        res[i] = func.calc_speed(df_pos)
        new_df = func.interp_system(df2, df_pos2)
        print("new: ", new_df)
        plt.figure()
        print("len: ", len(new_df))
        # https://stackoverflow.com/questions/22276066/how-to-plot-multiple-functions-on-the-same-figure
        plt.plot(new_df.iloc[i:len(new_df)-abs(len(new_df)-len(res[i]["speed"]))].index, res[i]["speed"], 'r')
        plt.plot(new_df.iloc[i:].index, new_df.iloc[i:]["Vitesse du véhicule"], 'b')
        plt.title(f"Vitesse, index = {i}")

    plt.show()

    # print("res: ", len(res[0]["speed"]))

    replace_header(df, df1_head)
    replace_header(df_pos, gps_head)