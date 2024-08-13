import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scienceplots  # Ensure this is installed
plt.style.use(['science', 'nature'])

root = '../data/Simulation/'
files = os.listdir(root)

# Create a figure and axis with specific size and resolution
fig, ax = plt.subplots(figsize=(5, 3), dpi=200)

# Updated colors list: First color for '25 °C', second for '25_s °C' as light red
colors = ['#80A6E2', 'lightcoral']  # lightcoral for light red

# New list for line styles: solid for '25 °C', dashed for '25_s °C'
linestyles = ['-', '--']  # Solid and dashed

markers = ['o', 'v']
legends = ['25 °C', '25_s °C']
batches = ['P25', '25F_s']

line_width = 0.5

for i in range(len(batches)):
    for f in files:
        if batches[i] in f:
            try:
                path = os.path.join(root, f)
                data = pd.read_csv(path)
                time = data['time'].values
                voltage = data['voltage'].values
                mask = (time >= 0) & (time <= 4000) & (voltage >= 2.5) & (voltage <=4.2)
                time_filtered = time[mask]
                voltage_filtered = voltage[mask]

                ax.plot(time_filtered[1:], voltage_filtered[1:],
                        color=colors[i], linestyle=linestyles[i],
                        alpha=1, linewidth=line_width,
                        marker=markers[i], markersize=2, markevery=50)

            except Exception as e:
                print(f"Error processing {f}: {e}")

custom_lines = [
    Line2D([0], [0], color=colors[0], linestyle='-', marker='o', markersize=1.5, linewidth=0.7),
    Line2D([0], [0], color=colors[1], linestyle='--', marker='v', markersize=1.5, linewidth=0.7)
]

ax.set_title('18650F Experiment vs Simulation')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (V)')
ax.legend(custom_lines, legends, loc='upper right', bbox_to_anchor=(1.0, 1), frameon=False, ncol=3, fontsize=6)

plt.tight_layout()
plt.show()