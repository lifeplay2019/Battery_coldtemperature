import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

root = '../data/internal resistance/'
files = os.listdir(root)
fig, ax = plt.subplots(figsize=(5, 3), dpi=200)

colors = ['#2878B5', '#F8AC8C', '#FF8884']
markers = ['o', 'v', 'D']
legends = ['18650F', '21700F', '26650F']
line_width = 0.7

all_IR_values = set()
temperatures_all_batches = []

# Collect all temperatures first to establish a consistent x-axis
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
                IR = data['CE'].values
                all_IR_values.update(IR)  # Collect Drop data

                # Perform linear fit and plot
                fit_params = np.polyfit(temperature, IR, 1)  # Linear fit
                fit_function = np.poly1d(fit_params)  # Create fit function


                # Map each temperature to its index for plotting
                x = [temperature_indices[temp] for temp in temperature]
                temp_fit = np.linspace(min(temperature), max(temperature), 500)

                ax.plot(x, IR, color=colors[i], alpha=1,
                        linewidth=line_width, marker=markers[i], markersize=2, markevery=1)

                # Plot the linear fit line as a dashed line
                ax.plot(temp_fit, fit_function(temperature), '--', color=colors[i], label=f'{batch} fit')

            except Exception as e:
                print(f"Error processing {f}: {e}")


# Customize legend
custom_lines = [
    Line2D([0], [0], color=colors[0], marker=markers[0], markersize=1.5, linewidth=line_width),
    Line2D([0], [0], color=colors[1], marker=markers[1], markersize=1.5, linewidth=line_width),
    Line2D([0], [0], color=colors[2], marker=markers[2], markersize=1.5, linewidth=line_width),
]

# Set y-ticks and x-ticks
interval = np.percentile(list(all_IR_values), 75) - np.percentile(list(all_IR_values), 25)
tick_frequency = interval / 0.5
min_ir, max_ir = min(all_IR_values), max(all_IR_values)
ticks = np.arange(min_ir, max_ir + tick_frequency, tick_frequency)
ax.set_yticks(ticks)

ax.set_xticks(range(len(all_temperatures)))
ax.set_xticklabels([str(temp) for temp in all_temperatures])

# set xticks and y ticks
# Rotating tick labels
plt.xticks(fontsize=5)
plt.yticks(rotation = 0, fontsize = 5)  # Rotate labels


ax.set_title('Fitorch Coulombic Efficiency vs Temperature', fontsize=8)
ax.set_xlabel(r'Temperature ($^\circ$C)', fontsize=5)
ax.set_ylabel(r'Coulombic Efficiency', fontsize=5)
ax.legend(custom_lines, legends, loc='lower right', bbox_to_anchor=(1.0, 0), frameon=False, ncol=1, fontsize=6)

plt.tight_layout()
plt.grid(axis='both',linestyle=':', which='major')
plt.show()