# Amperage negatif = recharge (http://physapp.giraud.free.fr/tgel/courant/cours_courant.htm)


import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import csv
import re

csv_data = []
avg_data = [
[],[],[]
]

final_data = [[], [], []]

final_final_data = []

avg_count = 3

with open("Data24_02_1/Fev-12-1er-acqui.txt") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    for row in reader:
        csv_data.append(row)

df = pd.read_csv("Data24_02_1/Fev-12-1er-acqui.txt", sep=';')
df = df.drop(0)
df = df.drop(1)    

df['Courant'] = pd.to_numeric(df['Courant batterie de traction mesuré par LBC'].str.replace(',', '.'))
df["Vitesse du véhicule"] = pd.to_numeric(df['Vitesse du véhicule'].str.replace(',', '.'))
df['Temps'] = pd.to_numeric(df['Temps'].str.replace(',', '.'))
df['Courant batterie de traction mesuré par LBC'] = pd.to_numeric(df['Courant batterie de traction mesuré par LBC'].str.replace(',', '.'))
        
# print(df.head())

#########################################################################
# Plot Intensite du courant en fonction de la vitesse (sur les 98 premieres valeurs)
#########################################################################
plt.figure(figsize=(12, 6))
# try resampling data later
plt.plot(df['Vitesse du véhicule'][2:100], df["Courant"][2:100])
plt.title("Intensite du courant en fonction de la vitesse")
plt.ylabel("Intensite courant")
plt.xlabel('Vitesse du véhicule')

#########################################################################


#########################################################################
# Demo moyenne mobile sur l'intensite du courant
#########################################################################
df['MA_amp'] = df['Courant'].rolling(window=avg_count).mean()
plt.figure(figsize=(12, 6))
plt.plot(df['Temps'][:100], df['MA_amp'][:100])
plt.title("Moyenne mobile intensite du courant en fonction du temps")
plt.ylabel("Intensite")
plt.xlabel('Temps')

#########################################################################

#########################################################################
# Lecture fichier de pos
#########################################################################
df_pos = pd.read_csv("Data24_02_1/Fev-12-1er-sans-RTK.txt", sep='\s+')
df_pos = df_pos.drop(0)

print(df_pos.columns)

#########################################################################

#########################################################################
# Moyennes colonnes pos
#########################################################################


#########################################################################
# Avant Moyenne Mobile

print("Moyennes avant correction")
print("Courant: ", df["Courant"].mean())
print("Vitesse du véhicule: ", df["Vitesse du véhicule"].mean())

print("Latitude: ", df_pos["latitude(deg)"].mean())
print("Longitude: ", df_pos["longitude(deg)"].mean())
print("Hauteur: ", df_pos["height(m)"].mean())
print("Hauteur min et max: ", df_pos["height(m)"].min(), df_pos["height(m)"].max())

#########################################################################
# Apres Moyenne Mobile

df['MA_vit'] = df['Vitesse du véhicule'].rolling(window=avg_count).mean()
df_pos['MA_lon'] = df_pos['latitude(deg)'].rolling(window=avg_count).mean()
df_pos['MA_lat'] = df_pos['longitude(deg)'].rolling(window=avg_count).mean()
df_pos['MA_hau'] = df_pos['height(m)'].rolling(window=avg_count).mean()


print("Moyennes apres correction")
print("Courant: ", df["MA_amp"].mean())
print("Vitesse du véhicule: ", df["MA_vit"].mean())

print("Latitude: ", df_pos["MA_lon"].mean())
print("Longitude: ", df_pos["MA_lat"].mean())
print("Hauteur: ", df_pos["MA_hau"].mean())
print("Hauteur min et max: ", df_pos["height(m)"].min(), df_pos["height(m)"].max())


#########################################################################


# Lier le geodata et l'acquitement

# Pour chaque interval de 200ms - prendre toutes les valeurs de l'inf jusqu'a la derniere valeur possible 
# ie si temps = 09:17:38.200, on prend les valeurs de 0,000 a 0,199 ms de l'acquitement
# on fait une moyenne de ces valeurs et on l'associe a la valeur attachee

#########################################################################
# Demo: liaison des valeurs entre 0 et 100 ms
#########################################################################

# avg = 0
# counter_current_ms = 1
# counter_vals = 1
# counter_outer = 0

# for i in range(4, 7):
#     match = re.search(r',\s*(\d+)', csv_data[i][0])
#     # print(match.group(1)[0])
#     if str(counter_current_ms) == match.group(1)[0]:
#         avg_data[0].append(float(csv_data[i][0].replace(',', '.')))
#         avg_data[1].append(float(csv_data[i][1].replace(',', '.')))
#         avg_data[2].append(float(csv_data[i][2].replace(',', '.')))
#     else:
#         final_data[0].append(str((sum(avg_data[0])) / len(avg_data[0])))
#         final_data[1].append(str((sum(avg_data[1])) / len(avg_data[1])))
#         final_data[2].append(str(sum(avg_data[2]) / len(avg_data[2])))
# print(final_data)

# tmp_df = pd.DataFrame([final_data], columns=['Temps', 'Vitesse du véhicule', 'Courant batterie de traction mesuré par LBC'])

# print(tmp_df)
# print(df_pos.iloc[4:5])

# df_pos2 = df_pos.iloc[4:5].reset_index(drop=True)
# tmp_df = tmp_df.reset_index(drop=True)

# final_final_data = pd.concat([df_pos2, tmp_df], axis=1)

# print(final_final_data.head())

#########################################################################
# Interpolation des donnees toutes les 200ms
# https://stackoverflow.com/questions/73210784/how-do-interpolate-values-between-two-date-columns-in-my-pandas-dataframe
#########################################################################
print(df.Temps)

# Drop all of the average calc added columns to stop spread of nan throughout the table
df_pos = df_pos.drop('MA_lon', axis=1)
df_pos = df_pos.drop('MA_lat', axis=1)
df_pos = df_pos.drop('MA_hau', axis=1)

df = df.drop('MA_amp', axis=1)
df = df.drop('MA_vit', axis=1)

df['Temps'] = pd.to_datetime(df['Temps'], unit='s')
df['Temps'] = df['Temps'] + pd.Timedelta(hours = 9, minutes=17, seconds=38)
new_date = pd.to_datetime('2024/02/12', format='%Y/%m/%d')
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

# plt.show()
