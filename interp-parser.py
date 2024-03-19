import numpy as np
from scipy.interpolate import interp1d
import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have a DataFrame with timestamps and multiple columns of data
data = {
    'timestamp': pd.to_datetime(['2022-01-01', '2022-01-02', '2022-01-04']),
    'value1': [2, 3, 5],
    'value2': [10, 15, 20]
}

df = pd.DataFrame(data)

# Create interpolation functions for each column
interp_func_value1 = interp1d(df['timestamp'], df['value1'], kind='linear', fill_value='extrapolate')
interp_func_value2 = interp1d(df['timestamp'], df['value2'], kind='linear', fill_value='extrapolate')

# Generate new timestamps for interpolation
new_timestamps = pd.date_range(start='2022-01-01', end='2022-01-04', freq='D')

# Interpolate the corresponding values for each column
new_value1 = interp_func_value1(new_timestamps)
new_value2 = interp_func_value2(new_timestamps)

# Create a new DataFrame with interpolated values
interpolated_data = pd.DataFrame({
    'timestamp': new_timestamps,
    'value1': new_value1,
    'value2': new_value2
})

# Plot the original and interpolated data for each column
plt.plot(df['timestamp'], df['value1'], 'o', label='Original value1')
plt.plot(new_timestamps, new_value1, '-', label='Interpolated value1')
plt.plot(df['timestamp'], df['value2'], 'o', label='Original value2')
plt.plot(new_timestamps, new_value2, '-', label='Interpolated value2')
plt.legend()
plt.show()