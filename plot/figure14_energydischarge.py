import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.backends.backend_pdf import PdfPages

root = '../data/internal resistance/'
files = os.listdir(root)
fig, ax = plt.subplots(figsize=(5, 3), dpi=200)  # 增加了图表尺寸

# Colors and markers
colors = ['#80A6E2', '#7BDFF2', '#FBDD85']
markers = ['o', 'v', 'D']
legends = ['18650E', '21700E', '26650E']
batches = ['18650E', '21700E', '26650E']
line_width = 0.7

all_IR_values = set()

# Plot data
for i, batch in enumerate(batches):
    for f in files:
        if batch in f:
            try:
                path = os.path.join(root, f)
                data = pd.read_csv(path)
                temperature = data['temperature'].values
                Pr = data['ED'].values
                all_IR_values.update(Pr)  # Collect all Percentage values

                ax.plot(temperature, Pr, color=colors[i], alpha=1,
                        linewidth=line_width, marker=markers[i],
                        markersize=2, markevery=1)
            except Exception as e:
                print(f"Error processing {f}: {e}")

# Customize legend
custom_lines = [
    Line2D([0], [0], color=colors[0], marker=markers[0], markersize=1.5, linewidth=line_width),
    Line2D([0], [0], color=colors[1], marker=markers[1], markersize=1.5, linewidth=line_width),
    Line2D([0], [0], color=colors[2], marker=markers[2], markersize=1.5, linewidth=line_width),
]


# Customizing ticks
# interval = np.percentile(list(all_IR_values), 75) - np.percentile(list(all_IR_values), 25)
# tick_frequency = interval   # Adjust frequency as necessary
# min_ir, max_ir = min(all_IR_values), max(all_IR_values)
# ticks = np.arange(min_ir, max_ir + tick_frequency, tick_frequency)
# ax.set_yticks(ticks)
specific_xticks = [-30, -25, -20, -15, -10, 0, 25]
ax.set_xticks(specific_xticks)
ax.set_xticklabels([str(x) for x in specific_xticks])  # Ensuring the labels are what we expect

# Rotating tick labels
plt.xticks(fontsize=5)
plt.yticks(rotation = 0, fontsize = 5)  # Rotate labels to prevent overlap

ax.set_title('Efest Energy Discharge vs Temperature', fontsize=8)
ax.set_xlabel(r'Temperature ($^\circ$C)', fontsize=5)
ax.set_ylabel(r'Energy Discharge (Wh)', fontsize=5)

plt.xticks(fontsize=5)
plt.yticks(fontsize=5)  # Adjust font size as needed

ax.legend(custom_lines, legends, loc='lower right', bbox_to_anchor=(1, 0), frameon=False, ncol=1, fontsize=6)

plt.tight_layout()
plt.grid(axis='x',linestyle=':', which='major')
plt.show()