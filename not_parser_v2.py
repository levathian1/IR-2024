import pandas as pd 
import warnings
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

if len(sys.argv) < 3:
    print("""
    Usage:
        - Param 1: donnees d'acquisition
        - Param 2: donnees GPS
    """)

# TODO: Header redefine for used formatting (add Time column to GPS dataframe for easier manip in future)
else:
    df = pd.read_csv(sys.argv[1]) # premier dataframe, donnee d'acquisition

    df = df.drop(0)
    df = df.drop(1)    

    df['Courant'] = pd.to_numeric(df['Courant batterie de traction mesuré par LBC'].str.replace(',', '.'))
    df["Vitesse du véhicule"] = pd.to_numeric(df['Vitesse du véhicule'].str.replace(',', '.'))
    df['Temps'] = pd.to_numeric(df['Temps'].str.replace(',', '.'))
    df['Courant batterie de traction mesuré par LBC'] = pd.to_numeric(df['Courant batterie de traction mesuré par LBC'].str.replace(',', '.'))


    df_pos = pd.read_csv(sys.argv[2], sep='\s+')
    df_pos = df_pos.drop(0)