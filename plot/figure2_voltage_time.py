import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scienceplots
plt.style.use(['science','nature'])
from matplotlib.backends.backend_pdf import PdfPages


root = '../data/efset18650_procress/'

files = os.listdir(root)
fig, ax = plt.subplots(figsize=(4, 2), dpi=200)
colors = ['#80A6E2',
          '#7BDFF2',
          '#FBDD85',
          '#F46F43',
          '#403990',
          '#CF3D3E']
markers = ['o', 'v', 'D', 'p', 's', '^']
legends = ['25 °C', '-10 °C', '-15 °C', '-20 °C', '-25 °C', '-30 °C']
batches = ['P25', 'N10', 'N15', 'N20', 'N25', 'N30']
line_width = 0.7

voltage_min, voltage_max = float('inf'), float('-inf')

for i in range(6):
    for f in files:
        if batches[i] in f:
            try:
                path = os.path.join(root, f)
                data = pd.read_csv(path)
                time = data['time'].values
                voltage = data['voltage'].values
                ax.plot(time[0:],
                        voltage[0:],
                        color=colors[i], alpha=1, linewidth=line_width,
                        marker=markers[i], markersize=2, markevery=50)

                # renew voltage range
                voltage_min = min(voltage_min, min(voltage[1:]))
                voltage_max = max(voltage_max, max(voltage[1:]))
            except Exception as e:
                print(f"Error processing {f}: {e}")

custom_lines = [
    Line2D([0], [0], color='#80A6E2', marker='o', markersize=1.5, linewidth=0.7),
    Line2D([0], [0], color='#7BDFF2', marker='v', markersize=1.5, linewidth=0.7),
    Line2D([0], [0], color='#FBDD85', marker='D', markersize=1.5, linewidth=0.7),
    Line2D([0], [0], color='#F46F43', marker='p', markersize=1.5, linewidth=0.7),
    Line2D([0], [0], color='#403990', marker='s', markersize=1.5, linewidth=0.7),
    Line2D([0], [0], color='#CF3D3E', marker='^', markersize=1.5, linewidth=0.7)
]


ax.set_title('Efset 18650 Voltage vs Time')
# ax.set_title('Fitorch 18650 Voltage vs Time')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (V)')
ax.legend(custom_lines, legends, loc='upper right', bbox_to_anchor=(1.0, 1), frameon=False, ncol=3, fontsize=6)

# Adjust the voltage range to the appropriate min-max range
ax.set_ylim([voltage_min - 0.1, voltage_max + 0.4])
plt.tight_layout()
plt.show()

# Save the picture
# with PdfPages("output.pdf") as pdf:
#     pdf.savefig(fig)
# plt.savefig('what ever you name.svg', format='svg')