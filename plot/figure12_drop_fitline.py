import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

root = '../data/internal resistance/'
files = os.listdir(root)
fig, ax = plt.subplots(figsize=(5, 3), dpi=200)

colors = ['#80A6E2', '#7BDFF2', '#FBDD85']
markers = ['o', 'v', 'D']
legends = ['18650F', '21700F', '26650F']
line_width = 0.7

all_IR_values = set()
temperatures_all_batches = []

# Collect all temperatures first
for f in files:
    for batch in legends:
        if batch in f:
            try:
                path = os.path.join(root, f)
                data = pd.read_csv(path)
                temperatures_all_batches.extend(data['temperature'].values)  # Collect temperatures
            except Exception as e:
                print(f"Error processing {f}: {e}")

all_temperatures = sorted(set(temperatures_all_batches))
temperature_indices = {temp: idx for idx, temp in enumerate(all_temperatures)}

# Now plot each file's data with consistent x-axis
for f in files:
    for i, batch in enumerate(legends):
        if batch in f:
            try:
                path = os.path.join(root, f)
                data = pd.read_csv(path)
                temperature = data['temperature'].values
                IR = data['Drop100'].values
                all_IR_values.update(IR)  # Collect Drop data

                # Perform linear fit
                fit_params = np.polyfit(temperature, IR, 1)
                fit_fn = np.poly1d(fit_params)

                # Prepare a continuous range of temperatures for the fit line
                temp_fit = np.linspace(min(temperature), max(temperature), 500)
                x = [temperature_indices[temp] for temp in temperature]

                # Plotting
                ax.scatter(temperature, IR, color=colors[i], label=f'{batch} data')
                ax.plot(temp_fit, fit_fn(temp_fit), '--', color=colors[i], label=f'{batch} fit (slope: {fit_params[0]:.2f})')

            except Exception as e:
                print(f"Error processing {f}: {e}")

# Customize legend
ax.legend(loc='upper right', frameon=False, fontsize=6)

ax.set_ylabel('Drop Rate (%)')
ax.set_xlabel('Temperature (°C)')

# Setting the y-axis and formatting
ax.set_yticks(np.linspace(min(all_IR_values), max(all_IR_values), 4))
ax.set_xticks(np.linspace(min(all_temperatures), max(all_temperatures), 6))

plt.title('Firotch Drop Rate (100) vs Temperature')
plt.tight_layout()
plt.show()