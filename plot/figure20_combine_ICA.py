import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.ndimage import gaussian_filter1d
import numpy as np

import scienceplots  # Assuming this is correctly installed and configured
plt.style.use(['science', 'nature'])
from matplotlib.backends.backend_pdf import PdfPages


# Define directories and labels for each battery type
battery_dirs_labels = [
    ('../data/18650_procress_added/', '18650'),
    ('../data/21700_procress/', '21700'),
    ('../data/26650_procress/', '26650')
]

# Define batches and colors for easier plotting
batches = ['P25', 'N10', 'N20']
colors = ['red', 'green', 'blue']
line_width = 1.0
sigma = 5  # Standard deviation for Gaussian filter

for batch in batches:
    fig, ax = plt.subplots(figsize=(6, 4), dpi=200)
    ICA_min, ICA_max = float('inf'), float('-inf')

    # Plot each type of battery in one subplot
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

                    ICA_min = min(ICA_min, np.min(ICA_filtered))
                    ICA_max = max(ICA_max, np.max(ICA_filtered))

                except Exception as e:
                    print(f"Error processing {f}: {e}")

    if np.isfinite(ICA_min) and np.isfinite(ICA_max):
        ax.set_ylim([ICA_min - 0.1, ICA_max + 0.1])

    ax.set_title(f'Combined ICA Measurements for {batch}')
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('dQ/dv (Ah/V)')
    ax.legend(loc='upper right', frameon=False)
    plt.tight_layout()
    plt.show()