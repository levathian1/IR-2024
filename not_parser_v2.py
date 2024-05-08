from hmac import new
from re import I
import pandas as pd 
import warnings
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import math

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

    # for i in range(0, 10):
    #     timestamp, res, df, min_ind = func.ajust_curve(df, val = df.iloc[i]["Vitesse du véhicule"])
    #     # https://stackoverflow.com/questions/22276066/how-to-plot-multiple-functions-on-the-same-figure
    #     plt.plot(res, 'r')
    #     plt.plot(df.iloc[min_ind]["Vitesse du véhicule"])
    #     plt.title(f"Vitesse, index premier timestamp = {timestamp}")
    #     plt.show()
    res = func.calc_speed(df_pos)
    res = func.calc_pente(res)
    df2 = df.copy()
    new_df = func.interp_system(df2, df_pos2)
    res = res.iloc[9:]
    res['intensity'] = new_df.iloc[:len(res)]['Courant'].to_numpy()
    print(res)
    res.to_csv("df_pos_with_speed_heightdiff.csv", sep='\t')
    new_df.to_csv("dump_interp_speed.csv", sep='\t')
    print("aa:", res["speed"].index)
    res.to_csv("dump_speed.csv", sep='\t')
    min = math.inf
# TODO: move the plots along :) to ajust, calc ajustement from that
    for i in range(0, 15):
        # print("pos: ", df_pos.head())     
        # print("new: ", len(new_df), len(res[i]["speed"]))
        plt.figure()
        # https://stackoverflow.com/questions/22276066/how-to-plot-multiple-functions-on-the-same-figure
        # if new_df.iloc[i:].index < len(res[i]["speed"]): len = len(df_pos[i:]["speed"]) 
        # else: new_df.iloc[i:].index
        # print(new_df["Time"], res[i]["Time"])
        print("len: ", len(res) - len(new_df[i:]))
        plt.plot(res["speed"][0:1000].index, res["speed"][i:i+1000], 'r', label="vitesse GPS")
        # for j in range (0, len(res) - len(new_df[i:])):
        #     new_df2 = pd.concat([new_df2, pd.DataFrame([[np.nan] * new_df2.shape[1]], columns=new_df2.columns)], ignore_index=True)
        plt.plot(res["speed"][0:1000].index, new_df["Vitesse du véhicule"][0:1000], 'b', label="vitesse interpolee")
        speed = new_df["Vitesse du véhicule"].iloc[0] - res["speed"].iloc[i]
        if speed < min: min = speed
        plt.legend()
        plt.title(f"Vitesse, index = {i}, speed diff at first index {speed}")

    plt.show()

    
    res = res.iloc[min:]
    res['intensity'] = new_df.iloc[:len(res)]['Courant'].to_numpy()
    print(res)
    res.to_csv("df_pos_with_speed_heightdiff.csv", sep='\t')

    # print("res: ", len(res[0]["speed"]))

    replace_header(df, df1_head)
    replace_header(df_pos, gps_head)