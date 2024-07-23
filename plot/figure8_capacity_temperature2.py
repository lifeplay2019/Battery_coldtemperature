import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Assuming the structure of directories and files from your previous context:
roots = ['../data/18650_procress_added/',
         '../data/21700_procress',
         '../data/26650_procress/']
batches = ['P25', 'N10', 'N15', 'N20', 'N25', 'N30']  # Temperature batches as per your previous context
titles = ['18650', '21700', '26650']  # Simplified titles representing battery types
colors = ['#80A6E2', '#7BDFF2', '#FBDD85', '#F46F43', '#403990', '#CF3D3E']

# Initialize dictionary to hold data
data_dict = {title: {batch: [] for batch in batches} for title in titles}

# Data aggregation
for root, title in zip(roots, titles):
    if not os.path.exists(root):
        print(f"Directory not found: {root}")
        continue

    files = os.listdir(root)
    for batch in batches:
        batch_files = [file for file in files if batch in file]
        all_capacity = []

        for file in batch_files:
            try:
                path = os.path.join(root, file)
                data = pd.read_csv(path)
                all_capacity.extend(data['SoC'].dropna().values )  # Collect all capacity readings
            except Exception as e:
                print(f"Error processing {file}: {e}")

        if all_capacity:
            # Calculate the average voltage per batch and battery type
            max_capacity = np.max(all_capacity)
            data_dict[title][batch] = max_capacity

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
width = 0.15  # width of the bars
n = len(batches)  # to calculate x positions of bars

for i, (batch, color) in enumerate(zip(batches, colors)):
    x = np.arange(len(titles)) + i * width  # nudge each batch over by the width of a bar
    heights = [data_dict[title][batch] for title in titles]
    ax.bar(x, heights, width, label=f"{batch} °C", color=color)

# Set labels and formatting
ax.set_xlabel('Battery Type')
ax.set_ylabel('Capacity Percentage')
ax.set_title('Average Voltage by Battery Type and Temperature')
ax.set_xticks(np.arange(len(titles)) + width * (n/2 - 0.5))
ax.set_xticklabels(titles)
ax.legend(title='Temperature')

plt.show()