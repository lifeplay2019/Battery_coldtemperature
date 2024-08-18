import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import numpy as np

import scienceplots
plt.style.use(['science','nature'])
from matplotlib.backends.backend_pdf import PdfPages

sigma = 5  # Standard deviation for Gaussian filter
line_width = 1.0
colors = ['#80A6E2', '#7BDFF2', '#F46F43']  # Plot colors for each battery type

# Directories and labels for each battery type
battery_dirs_labels = [
    ('../data/18650_procress_added/', '18650'),
    ('../data/21700_procress/', '21700'),
    ('../data/26650_procress/', '26650')
]

batches = ['P25', 'N10', 'N20']  # Batches to plot

# Custom titles for each subplot
titles = ['Fitorch Battery at 25°C',
          'Fitorch Battery at -10°C',
          'Fitorch Battery at -20°C']

# Initialize figure with 3 subplots side-by-side
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(8, 3), dpi=200, sharey=True)

for ax, batch, title in zip(axs, batches, titles):
    ICA_min, ICA_max = float('inf'), float('-inf')  # Initialize min/max for ICA

    for (dir_path, label), color in zip(battery_dirs_labels, colors):
        files = os.listdir(dir_path)
        for f in files:
            if batch in f:
                try:
                    path = os.path.join(dir_path, f)
                    data = pd.read_csv(path)

                    if data.empty or 'voltage' not in data.columns or 'ICA' not in data.columns:
                        print(f"Warning: {f} is missing required data.")
                        continue

                    data.dropna(subset=['voltage', 'ICA'], inplace=True)

                    voltage = data['voltage'].values
                    ICA = data['ICA'].values

                    if len(voltage) != len(ICA):
                        print(f"Warning: Mismatch in lengths of voltage and ICA in {f}.")
                        continue

                    ICA_filtered = gaussian_filter1d(ICA, sigma=sigma)
                    ax.plot(voltage, ICA_filtered, color=color, alpha=1, linewidth=line_width, label=label)

                    # Update ICA min/max for setting y-axis limits
                    ICA_min = min(ICA_min, np.min(ICA_filtered))
                    ICA_max = max(ICA_max, np.max(ICA_filtered))

                except Exception as e:
                    print(f"Error processing {f}: {e}")

    if np.isfinite(ICA_min) and np.isfinite(ICA_max):
        ax.set_ylim([ICA_min - 0.1, ICA_max + 0.1])

    ax.set_title(title, fontsize=8)
    ax.set_xlabel('Voltage (V)', fontsize=6)

    # Now the grid and legend are set per subplot
    ax.grid(axis='both', linestyle=':', which='major')
    ax.legend(loc='best', fontsize=6)

axs[0].set_ylabel('dQ/dv (Ah/V)', fontsize=6)  # Only set ylabel for the first subplot

plt.tight_layout()
plt.subplots_adjust(top=0.85)  # Adjust spacing to avoid overlap
plt.show()