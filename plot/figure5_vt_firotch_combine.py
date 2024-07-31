import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scienceplots  # Assuming 'scienceplots' theme is installed

plt.style.use(['science', 'nature'])
from matplotlib.backends.backend_pdf import PdfPages

# Set up subplots layout as two rows by two columns
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(8, 6), dpi=200)
axes = axes.flatten()  # Flatten the 3x3 axes array to make indexing easier
colors = ['#80A6E2', '#7BDFF2', '#FBDD85', '#F46F43', '#403990', '#CF3D3E']
markers = ['o', 'v', 'D', 'p', 's', '^']
legends = ['25 °C', '-10 °C', '-15 °C', '-20 °C', '-25 °C', '-30 °C']
batches = ['P25', 'N10', 'N15', 'N20', 'N25', 'N30']
line_width = 0.7

# Specify data file paths
roots = ['../data/18650_procress_added/',
         '../data/efset18650_procress',
         '../data/21700_procress',
         '../data/efset21700_procress',
         '../data/26650_procress/',
         '../data/efset26650_procress'
         ]
titles = ['Fitorch 18650 Voltage vs Time',
          'Efest 18650 Voltage vs Time',
          'Fitorch 21700 Voltage vs Time',
          'Efest 21700 Voltage vs Time',
          'Fitorch 26650 Voltage vs Time',
          'Efest 26650 Voltage vs Time'
          ]

for idx, root in enumerate(roots):
    if not os.path.exists(root):
        print(f"Directory not found: {root}")
        continue

    files = os.listdir(root)
    voltage_min, voltage_max = float('inf'), float('-inf')
    for i in range(6):
        for f in files:
            if batches[i] in f:
                try:
                    path = os.path.join(root, f)
                    data = pd.read_csv(path)

                    if data.empty:
                        print(f"Data file is empty: {f}")
                        continue

                    time = data['time'].values
                    voltage = data['voltage'].values
                    axes[idx].plot(time, voltage, color=colors[i], alpha=1, linewidth=line_width,
                                   marker=markers[i], markersize=2, markevery=50)

                    # Update voltage ranges
                    if len(voltage) > 0:
                        voltage_min = min(voltage_min, min(voltage))
                        voltage_max = max(voltage_max, max(voltage))
                except Exception as e:
                    print(f"Error processing {f}: {e}")

    if voltage_min == float('inf') or voltage_max == float('-inf'):
        print("No valid voltage data found, cannot set plot limits.")
        continue

    # Set labels and titles for each subplot
    axes[idx].set_title(titles[idx],fontsize = 8)
    axes[idx].set_xlabel('Time (s)', fontsize=6)
    axes[idx].set_ylabel('Voltage (V)', fontsize=6)
    axes[idx].legend(legends, loc='upper right', bbox_to_anchor=(1, 1), frameon=False, ncol=3, fontsize=6)
    axes[idx].set_ylim([voltage_min - 0.1, voltage_max + 0.4])

plt.subplots_adjust(hspace=0.6, wspace=0.2)  # Adjust the spacing
plt.show()

# # Save as pdf
# with PdfPages("combined_output.pdf") as pdf:
#     pdf.savefig(fig)
#
# # Save as SVG
# plt.savefig('combined_output.svg', format='svg')
