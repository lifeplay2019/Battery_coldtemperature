import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scienceplots  # Assuming 'scienceplots' theme is installed
plt.style.use(['science', 'nature'])
from matplotlib.backends.backend_pdf import PdfPages

# Set up subplots layout as two rows by two columns
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 6), dpi=200)
axes = axes.flatten()  # Flatten the 2x2 axes array to make indexing easier
colors = ['#80A6E2', '#7BDFF2', '#FBDD85', '#F46F43', '#403990', '#CF3D3E']
markers = ['o', 'v', 'D', 'p', 's', '^']
legends = ['25 °C', '-10 °C', '-15 °C', '-20 °C', '-25 °C', '-30 °C']
batches = ['P25', 'N10', 'N15', 'N20', 'N25', 'N30']
line_width = 0.7

# Specify data file paths
roots = ['../data/18650_procress_added/',
         '../data/26650_procress/',
         '../data/efset18650_procress',
         '../data/efset26650_procress']
titles = [
    'Fitorch 18650 Voltage vs Time',
    'Fitorch 26650 Voltage vs Time',
    'Efset 18650 Voltage vs Time',
    'Efset 26650 Voltage vs Time'
]
