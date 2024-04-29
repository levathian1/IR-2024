import math
import pandas as pd

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
    df = pd.read_csv("df_pos_with_speed_heightdiff.csv", sep='\s+')
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html#pandas-dataframe-iterrows
    for ind, row in df.iterrows():
        k_m = 114 / mass
        f_m = ( k_m / 0.2032 ) * row['intensity'] # 18 inch tire
        f_f = 0 # calc on speed > 0
        f_a = ( air_density / 2 ) * cx * frontal_area * row['speed'] ** 2
        f_r = cr * mass *  g * math.cos(row['angle'])
        f_p = mass * g * math.sin(row['angle'])
        a = (f_m - f_f - f_a - f_r - f_p) / mass

        res.append(a)
    # -ma = k * v**2 + f_rl * m * g + m * g * sin theta - F
    return res

# https://stackoverflow.com/questions/4440516/in-python-is-there-an-elegant-way-to-print-a-list-in-a-custom-format-without-ex
print('\n'.join('{}: {}'.format(*k) for k in enumerate(calc_accel())))