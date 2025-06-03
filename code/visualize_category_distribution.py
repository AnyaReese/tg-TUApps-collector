import json
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np # Import numpy for colormap indexing

# 蓝色主题和图表参数
plt.rcParams['figure.figsize'] = [7, 6]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.facecolor'] = '#f8fafd'
plt.rcParams['figure.facecolor'] = '#f8fafd'

# 定义分类文件和对应的图例标签 (使用英文标签)
category_files = {
    'Pornographic Software': '色情_software_urls.json',
    'Gambling Software': '赌博_software_urls.json',
    'Pirated Software': '盗版_software_urls.json',
    'AI': 'AI_urls.json',
    'Blockchain/Web3': 'blockchain_web3_urls.json',
    'Other': '其他_urls.json'
}

result_dir = './result'

# 读取各分类文件的URL数量
category_counts = {}
for category, filename in category_files.items():
    file_path = os.path.join(result_dir, filename)
    urls = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = json.load(f)
            if isinstance(urls, list):
                category_counts[category] = len(urls)
            else:
                print(f"Warning: {filename} does not contain a list.")
                category_counts[category] = 0
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_path}")
            category_counts[category] = 0
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            category_counts[category] = 0
    else:
        print(f"Warning: File not found at {file_path}")
        category_counts[category] = 0

# 过滤掉数量为0的类别，避免饼图出现0%的扇形
valid_categories = {k: v for k, v in category_counts.items() if v > 0}
labels = list(valid_categories.keys())
sizes = list(valid_categories.values())
total_classified_urls = sum(sizes)

if total_classified_urls == 0:
    print("No classified URL data available to generate chart.")
    exit()

# 画图
fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
fig.patch.set_facecolor('#f8fafd')

# 使用蓝色系的颜色映射，并跳过最浅的部分
blues_cmap = plt.colormaps['Blues']
# Sample colors from a range within the colormap (e.g., from 0.3 to 1.0)
start_sampling = 0.3 # Adjust this value (0.0 to 1.0) to control how much of the light end is skipped
colors = [blues_cmap(start_sampling + (1.0 - start_sampling) * i / (len(labels) - 1)) for i in range(len(labels))] # Sample from start_sampling to 1.0
colors = colors[::-1] # Reverse to get darker shades for larger slices

explode = [0.02] * len(labels) # 微小的分离效果

# 绘制饼图
wedges, texts, autotexts = ax.pie(
    sizes, explode=explode, colors=colors,
    autopct='%1.1f%%', startangle=90,
    textprops={'fontsize': 8, 'color': 'white', 'weight': 'bold'},
    wedgeprops={'edgecolor': 'white', 'linewidth': 1, 'antialiased': True}
)

# 尝试调整百分比标签位置，避免重叠 (对于小扇形)
# 你可能需要根据实际数据分布进一步微调这里的逻辑
for i, w in enumerate(wedges):
    ang = (w.theta2 + w.theta1) / 2.
    # 计算文本位置，稍微靠外一些
    x = w.r * 0.8 * np.cos(np.deg2rad(ang)) # Use np.cos and np.deg2rad
    y = w.r * 0.8 * np.sin(np.deg2rad(ang)) # Use np.sin and np.deg2rad
    autotexts[i].set_position((x, y))
    # 如果标签移到外面，将颜色改深
    autotexts[i].set_color('black')

# 主标题 (居中)
fig.text(
    0.14,  # x position (0.5 = center)
    0.75,  # y position
    'URL Category Distribution',
    fontsize=18,
    fontweight='bold',
    color='#223a5e'
)

# 计算每一类的占比 (用于图例)
legend_labels = []
for i, label in enumerate(labels):
    percentage = (sizes[i] / total_classified_urls) * 100 if total_classified_urls > 0 else 0
    legend_labels.append(f"{label} ({percentage:.1f}%)") # Label (Percentage)

# 图例竖直排列在右侧
custom_legend_patches = [Patch(facecolor=colors[i], edgecolor='white') for i in range(len(labels))]
plt.legend(
    custom_legend_patches, legend_labels,
    loc='center left',
    bbox_to_anchor=(1, 0.5),
    ncol=1,
    frameon=False,
    fontsize=10,
    handlelength=1.5,
    handleheight=1.5,
    borderaxespad=0.5,
    labelspacing=0.7
)

# 调整布局 (为右侧图例留出更多空间，如果需要)
plt.tight_layout(rect=[0, 0, 0.75, 1]) # 根据需要调整

# 保存图表
output_plot_path = os.path.join(result_dir, 'url_category_distribution.png')
plt.savefig(
    output_plot_path,
    dpi=300,
    bbox_inches='tight',
    facecolor='#f8fafd',
    edgecolor='none'
)
plt.close()

print(f"Generated category distribution chart: {output_plot_path}")
print("Category Counts:")
for category, count in category_counts.items():
    print(f"{category}: {count}")
print(f"Total Classified URLs: {total_classified_urls}") 