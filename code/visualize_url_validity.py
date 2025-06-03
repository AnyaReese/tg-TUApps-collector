import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# 蓝色主题参数
plt.rcParams['figure.figsize'] = [10, 8]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 13
plt.rcParams['axes.facecolor'] = '#f8fafd'
plt.rcParams['figure.facecolor'] = '#f8fafd'

# 读取数据
with open('./data/msg_history_urls.json', 'r') as f:
    original_urls = json.load(f)
filtered_urls = pd.read_csv('./data/result.csv', sep='\t')

total_urls = len(original_urls)
valid_urls = len(filtered_urls)
invalid_urls = total_urls - valid_urls
validity_rate = (valid_urls / total_urls) * 100

# 画图
fig, ax = plt.subplots(figsize=(6, 5.5), dpi=300)  # 更小尺寸
fig.patch.set_facecolor('#f8fafd')

labels = ['Valid URLs', 'Invalid URLs']
sizes = [valid_urls, invalid_urls]
colors = ['#2986cc', '#b3c6e7']  # 深浅蓝
explode = (0.08, 0)

# 只显示百分比，标签不显示类别
wedges, _, autotexts = ax.pie(
    sizes, explode=explode, colors=colors,
    autopct='%1.1f%%', startangle=90,
    textprops={'fontsize': 12, 'color': 'black'},
    wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'antialiased': True})

# 主标题（用 suptitle 保证居中，调整y值靠近图形）
fig.suptitle(
    'URL Validity Analysis',
    fontsize=18,
    fontweight='bold',
    color='#223a5e',
    y=0.83 # 将y值从0.96调整为0.92，让标题下移
)

# 计算每一类的占比
percent_valid = f"{(valid_urls / total_urls * 100):.1f}%"
percent_invalid = f"{(invalid_urls / total_urls * 100):.1f}%"
legend_labels = [
    f"{labels[0]} ({percent_valid})",
    f"{labels[1]} ({percent_invalid})"
]
custom_legend = [
    Patch(facecolor=colors[0], edgecolor='white', label=legend_labels[0]),
    Patch(facecolor=colors[1], edgecolor='white', label=legend_labels[1])
]

# 图例竖直排列在右侧，贴近饼图
plt.legend(
    custom_legend, legend_labels,
    loc='center left',
    bbox_to_anchor=(1, 0.5),  # 更贴近
    ncol=1,
    frameon=False,
    fontsize=10,
    handlelength=1.2,
    handleheight=1.2,
    borderaxespad=0.3,
    columnspacing=1.0,
    labelspacing=0.5
)

plt.tight_layout(rect=[0, 0, 0.93, 1])  # 右侧留更少空间
plt.savefig('./result/url_validity_rate.png', dpi=300, bbox_inches='tight', facecolor='#f8fafd')
plt.close()

print(f"Total URLs: {total_urls}")
print(f"Valid URLs: {valid_urls}")
print(f"Invalid URLs: {invalid_urls}")
print(f"Validity Rate: {validity_rate:.2f}%") 