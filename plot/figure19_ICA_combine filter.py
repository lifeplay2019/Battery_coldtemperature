import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.ndimage import gaussian_filter1d
import numpy as np

import scienceplots
plt.style.use(['science','nature'])
from matplotlib.backends.backend_pdf import PdfPages

# Define the root directory where the files are stored
root = '../data/21700_procress/'
files = os.listdir(root)
fig, ax = plt.subplots(figsize=(4, 3), dpi=200)
color_original = '#80A6E2'
color_filtered = '#FFA07A'
color_moving_avg = '#B1CE46'
markers = ['o']
batch = 'P25'
line_width = 0.7

ICA_min, ICA_max = float('inf'), float('-inf')
sigma = 5  # Standard deviation for Gaussian filter
window_size = 20  # Size of the moving average window

def moving_average(x, w):
    """ Calculate the moving average of the input array x using a window size w. """
    return np.convolve(x, np.ones(w), 'valid') / w

for f in files:
    if batch in f:
        try:
            path = os.path.join(root, f)
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
            ICA_moving_avg = moving_average(ICA, window_size)

            # Plot original, Gaussian filtered, and moving average data
            ax.plot(voltage, ICA, color=color_original, alpha=0.5, linewidth=line_width, marker=markers[0],
                    markersize=2, markevery=100,  linestyle='--', label='Original Data')
            ax.plot(voltage, ICA_filtered, color=color_filtered, alpha=0.7, linewidth=line_width * 1.5,
                    label='Gaussian Filtered')
            ax.plot(voltage[:len(ICA_moving_avg)], ICA_moving_avg, color=color_moving_avg, alpha=0.8, linewidth=line_width,
                    label='Moving Avg')

            # Update the min and max for the axis limits
            ICA_min = min(ICA_min, np.min(ICA_filtered), np.min(ICA_moving_avg))
            ICA_max = max(ICA_max, np.max(ICA_filtered), np.max(ICA_moving_avg))

        except Exception as e:
            print(f"Error processing {f}: {e}")

# Set appropriate axis limits
if np.isfinite(ICA_min) and np.isfinite(ICA_max):
    ax.set_ylim([ICA_min - 0.1, ICA_max + 0.1])

# Set labels and title
ax.set_title('21700 Firotch Battery ICA at 25 °C')
ax.set_xlabel('Voltage (V)')
ax.set_ylabel('dQ/dv (Ah/V)')

# Define legend elements for all line types
legend_elements = [
    Line2D([0], [0], color=color_original, lw=1, linestyle='--', label='Original Data'),
    Line2D([0], [0], color=color_filtered, lw=1, label='Gaussian Filter'),
    Line2D([0], [0], color=color_moving_avg, lw=1, label='Moving Average')
]
ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.3, 1.0), frameon=False, fontsize=6)
plt.tight_layout()
plt.show()