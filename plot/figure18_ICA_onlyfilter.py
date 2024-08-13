import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.ndimage import gaussian_filter1d
import numpy as np

import scienceplots  # Assuming this is correctly installed and configured
plt.style.use(['science', 'nature'])
from matplotlib.backends.backend_pdf import PdfPages

root = '../data/18650_procress_added/'
files = os.listdir(root)
fig, ax = plt.subplots(figsize=(4, 3), dpi=200)
color_filtered = '#FFA07A'  # Use a distinctive color for the filtered data
batch = 'N15'
line_width = 0.7

ICA_min, ICA_max = float('inf'), float('-inf')
sigma = 5  # Standard deviation for Gaussian filter

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
            ax.plot(voltage, ICA_filtered, color=color_filtered, alpha=1, linewidth=line_width)

            ICA_min = min(ICA_min, np.min(ICA_filtered))
            ICA_max = max(ICA_max, np.max(ICA_filtered))
        except Exception as e:
            print(f"Error processing {f}: {e}")

if np.isfinite(ICA_min) and np.isfinite(ICA_max):
    ax.set_ylim([ICA_min - 0.1, ICA_max + 0.4])
else:
    print("Invalid ICA_min or ICA_max, skipping ylim setting.")

ax.set_title('Fitorch 18650 ICA at -15 °C')
ax.set_xlabel('Voltage (V)')
ax.set_ylabel('dQ/dv (Ah/V)')

legend_elements = [Line2D([0], [0], color=color_filtered, lw=line_width, label='Filtered Data')]
ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.3, 1.0), frameon=False, fontsize=6)

plt.tight_layout()
plt.show()