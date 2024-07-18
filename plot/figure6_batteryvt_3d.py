import pandas as pd
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 设定图形和Axes
fig = plt.figure(figsize=(10, 6), dpi=200)
ax = fig.add_subplot(111, projection='3d')

colors = ['#80A6E2', '#7BDFF2', '#FBDD85', '#F46F43', '#403990', '#CF3D3E']
markers = ['o', 'v', 'D', 'p', 's', '^']
batches = ['P25', 'N10', 'N15', 'N20', 'N25', 'N30']
line_width = 0.7

roots = ['../data/18650_procress_added/', '../data/26650_procress/']
# roots = ['../data/18650_procress_added/', '../data/26650_procress/']
roots_labels = ['18650', '26650']  # 用于标记X轴的批次类型

for root_idx, root in enumerate(roots):
    files = os.listdir(root)

    for i, batch in enumerate(batches):
        for file in files:
            if batch in file:
                try:
                    path = os.path.join(root, file)
                    data = pd.read_csv(path)
                    time = data['time'].values
                    voltage = data['voltage'].values
                    x = [roots_labels[root_idx]] * len(time)  # X轴均为当前电池种类

                    # 绘制3D曲线
                    ax.plot(x, time, voltage, label=f"{batch} {roots_labels[root_index]}", color=colors[i], marker=markers[i], linewidth=line_width, markersize=2, markevery=50)
                except Exception as e:
                    print(f"Error processing {file}: {e}")

# 设置坐标轴标签和标题
ax.set_xlabel('Battery Type')
ax.set_ylabel('Time (s)')
ax.set_zlabel('Voltage (V)')

# 图例和视图调整
ax.legend(loc='upper left', bbox_to_anchor=(1,1))
plt.show()