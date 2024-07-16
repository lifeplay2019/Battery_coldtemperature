import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scienceplots  # 假设安装了scienceplots 主题
plt.style.use(['science', 'nature'])
from matplotlib.backends.backend_pdf import PdfPages

# 设定子图布局为两行一列
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(4, 4), dpi=200)
colors = ['#80A6E2', '#7BDFF2', '#FBDD85', '#F46F43', '#403990', '#CF3D3E']
markers = ['o', 'v', 'D', 'p', 's', '^']
legends = ['25 °C', '-10 °C', '-15 °C', '-20 °C', '-25 °C', '-30 °C']
batches = ['P25', 'N10', 'N15', 'N20', 'N25', 'N30']
line_width = 0.7

# 指定数据文件路径
roots = ['../data/18650_procress_added/', '../data/26650_procress/']
titles = ['Fitorch 18650 Voltage vs Time', 'Fitorch 26650 Voltage vs Time']


for idx, root in enumerate(roots):
    files = os.listdir(root)
    voltage_min, voltage_max = float('inf'), float('-inf')

    for i in range(6):
        for f in files:
            if batches[i] in f:
                try:
                    path = os.path.join(root, f)
                    data = pd.read_csv(path)
                    time = data['time'].values
                    voltage = data['voltage'].values
                    axes[idx].plot(time, voltage, color=colors[i], alpha=1, linewidth=line_width,
                                   marker=markers[i], markersize=2, markevery=50)

                    # 更新电压范围
                    voltage_min = min(voltage_min, min(voltage[1:]))
                    voltage_max = max(voltage_max, max(voltage[1:]))
                except Exception as e:
                    print(f"Error processing {f}: {e}")

    # 设置子图的标签和标题
    axes[idx].set_title(titles[idx])
    axes[idx].set_xlabel('Time (s)',fontsize=6)
    axes[idx].set_ylabel('Voltage (V)',fontsize=6)
    axes[idx].legend(legends, loc='upper right', bbox_to_anchor=(1, 1), frameon=False, ncol=3, fontsize=6)
    axes[idx].set_ylim([voltage_min - 0.1, voltage_max + 0.6])

plt.subplots_adjust(hspace=0.4)
plt.show()

# Save as pdf
# with PdfPages("combined_output.pdf") as pdf:
#     pdf.savefig(fig)
#
#  save as SVG
# plt.savefig('combined_output.svg', format='svg')