import math
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn import preprocessing
import numpy as np

# https://numpy.org/doc/stable/reference/generated/numpy.set_printoptions.html
np.set_printoptions(suppress=True)

# aero_res = ( air_density / 2 ) * cx * frontal_area * speed ** 2
# rolling_res = cr * mass * 9.81
# grade_res = mass * 9.81 * sin theta, theta = angle with road

# air_density = m / V
# https://fr.wikipedia.org/wiki/Masse_volumique_de_l%27air

# thing to estimate: power
# accel: https://www.ncl.ac.uk/webtemplate/ask-assets/external/maths-resources/mechanics/kinematics/speed-time-and-distance-time-graphs.html
# (vf - vi )/delta_time
# power = F * v = (mass * accel + aero_res_const * speed**2 + cr * mass * 9.81 + mass * 9.81 * sin theta) * v

# use simulations to get accel & speed values to plug into formula to get ranges

def deg_to_rad(deg):
    return deg * (math.pi/180)

mass = 1875
air_density = 1.204
cx = 0.35
frontal_area = 2.54478
cr = 0.0085
g = 9.81
aero_res_const = 1.3 # val ref from pdf
theta = deg_to_rad(1) # use average elevation to min to get slopping over data
df = pd.read_csv("df_pos_with_speed_heightdiff.csv", sep='\s+')
max_int = df['intensity'].max() * (5/100)

def calc_aero_res(speed):
    return ( air_density / 2 ) * cx * frontal_area * speed ** 2

def calc_rolling_res():
    return cr * mass * 9.81

def calc_grade_res():
    return mass * 9.81 * math.sin(theta)

def calc_power(accel, speed):
    return (mass * accel + aero_res_const * speed**2 + cr * mass * 9.81 + mass * 9.81 * math.sin(theta)) * speed

def calc_accel():
    # add in accel calc with speed / time to check against
    res = list()
    fin_arr = list()
    accel_moy = (df["speed"].iloc[0] - df["speed"].iloc[:1]) / 430
    print("avg accel", accel_moy)
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html#pandas-dataframe-iterrows
    accel = list()
    angle = list()
    speed = list()
    for i in range(0, df.shape[0]-1):
        accel.append((df["speed"].iloc[i] - df["speed"].iloc[i+1]) / 0.2)
        # print('accel[i]')

    # print(accel)
    km = list()
    for i in range(len(accel)):
        if(df['intensity'].iloc[i] > max_int):
            # print(df['intensity'].iloc[i])
            f_a = ( air_density / 2 ) * cx * frontal_area * df['intensity'].iloc[i] ** 2
            f_r = cr * mass *  g * math.sin(deg_to_rad(df['angle'].iloc[i]))
            f_p = mass * g * math.sin(deg_to_rad(df['angle'].iloc[i]))
            # print((0.2 / (df['intensity'].iloc[i] ) * (mass * accel[i]) - f_a - f_r - f_p))
            km.append((0.5  * (mass * accel[i]) - f_a - f_r - f_p)/ (df['intensity'].iloc[i]  ))

    # print(df.shape[0]-1)
    std_dev = np.std(np.array(km))
    km_nb = np.mean(np.array(km))
    print('dev: ', std_dev)
    print("km: ", km_nb)
    for ind, row in df.iterrows():
        if(row['intensity'] > max_int):
            # k_m = 114 / mass
            # https://www.renault.fr/achat-vehicules-neufs/vehicules.html?productId=VEH_VF1RFK00870363236
            # kangoo engine traction
            angle.append(float(row['angle']))
            speed.append(float(row['speed']))
            k_m = 245 / row['intensity']
            f_m = ( km_nb / 0.5 ) * row['intensity'] # 18 inch tire
            f_f = 0 # calc on speed > 0
            f_a = ( air_density / 2 ) * cx * frontal_area * row['speed'] ** 2
            f_r = cr * mass *  g * math.sin(deg_to_rad(row['angle']))
            f_p = mass * g * math.sin(deg_to_rad(row['angle']))
            a = (f_m - f_f - f_a - f_r - f_p) / mass
            res.append(a)
            fin_arr.append([km_nb, f_m, f_f, f_a, f_r, f_p])
            # print(k_m)


            
    # -ma = k * v**2 + f_rl * m * g + m * g * sin theta - F
    return res, fin_arr, accel, angle, speed

# https://stackoverflow.com/questions/4440516/in-python-is-there-an-elegant-way-to-print-a-list-in-a-custom-format-without-ex
val, arr, acc, ang, sp = calc_accel()
# print('\n'.join('{}: {}'.format(*k) for k in enumerate(val)))
plt.figure()
plt.plot(df['Time'][0:15], val[0:15])
# plt.legend()
plt.title(f"Acceleration au cours du temps")

print(sp)

plt.figure()
plt.plot(sp, ang)
plt.title(f"Variation de la pente en fonction de la vitesse")

plt.figure()
plt.plot(df['Time'][:335], ang)
plt.title(f"Variation de la pente au cours du temps")


# print(len(arr)/2)

arr_t = arr[:int(len(arr)/2)]
arr_p = arr[int(len(arr)/2)+1:]

lab_enc = preprocessing.LabelEncoder()
encoded = lab_enc.fit_transform(val)

clf = svm.SVR()

clf.fit(arr_t, val[:int(len(arr)/2)])

res2 = clf.predict(arr_p)

print("len: ", len(res2), len(val[int(len(arr)/2)+1:]))

# print(res2)
# print(val[int(len(arr)/2)+1:])
# # print(val)

for i in range(0, int(len(arr)/2)):
    print("gap", res2[i] - val[i + int(len(arr)/2)+1])
    print("gap 2", val[i] - acc[i])

plt.show()