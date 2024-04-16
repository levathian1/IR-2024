import math

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
air_density = 1,204
cx = 0.35
frontal_area = 2.54478
cr = 0.0085
aero_res_const = 1.3 # val ref from pdf
theta = deg_to_rad(1) # use average elevation to min to get slopping over data