import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# 读取数据
data = pd.read_csv('../data/CCCV/FP25.csv')
time = data['time']
voltage = data['voltage']
current = data['current']

# 创建图表和轴
fig, ax1 = plt.subplots(figsize=(6, 3), dpi=200)

# 第二个y轴
ax2 = ax1.twinx()

# 绘制数据
voltage_line, = ax1.plot(time, voltage, '#5F97D2', label='Voltage (V)')
current_line, = ax2.plot(time, current, '#96C37D', label='Current (A)')

# 设置轴标题
ax1.set_xlabel('Time (s)', fontsize=7)
ax1.set_ylabel('Voltage (V)', color='#5F97D2', fontsize=7)
ax2.set_ylabel('Current (A)', color='#96C37D', fontsize=7)

# 设置轴和刻度颜色
ax1.spines['left'].set_color('#5F97D2')    # 左侧轴颜色
ax1.spines['right'].set_color('#5F97D2')   # 右侧轴颜色，确保无覆盖
ax1.spines['top'].set_color('#5F97D2')     # 顶部轴颜色
ax1.spines['bottom'].set_color('#5F97D2')  # 底部轴颜色
ax1.tick_params(axis='y', colors='#5F97D2', labelsize=7)  # 左侧刻度颜色和字体大小

ax2.spines['right'].set_color('#96C37D')
ax2.spines['left'].set_color('#5F97D2')  # 为一致性也设置右侧轴的左轴颜色（可能不可见）
ax2.tick_params(axis='y', colors='#96C37D', labelsize=7)  # 右侧刻度颜色和字体大小

ax1.tick_params(axis='x', labelsize=7)   # 设置x轴刻度字体大小

# 在主图中绘制内嵌图
axins1 = inset_axes(ax1, "20%", "20%", loc='upper right', borderpad=1)
axins1.plot(time, current, color='#96c37D', label='Current')
axins1.tick_params(axis='y', colors='#96C37D', labelsize=4)
axins1.tick_params(axis='x', labelsize=4)
axins1.set_xlim(6900, 7200)
axins1.set_ylim(-0.1, 0.1)
#
# axins2 = inset_axes(ax2, "30%", "30%", loc='lower left', borderpad=5)
# axins2.plot(time, current, color='#96C37D')
# axins2.set_xlim(4000, 4500)
# axins2.set_ylim(-1, 1)

# 展示图表
plt.show()