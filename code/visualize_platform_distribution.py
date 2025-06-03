import json
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import re

# 蓝色主题和图表参数
plt.rcParams['figure.figsize'] = [7, 6]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.facecolor'] = '#f8fafd'
plt.rcParams['figure.facecolor'] = '#f8fafd'

# 读取valid_url.json
result_dir = './result'
valid_url_path = os.path.join("./data", 'valid_url.json')

platform_counts = {
    'Android': 0,
    'iOS': 28,
    'Both': 0,  # 同时支持安卓和苹果的应用
    'Other': 0
}

try:
    with open(valid_url_path, 'r', encoding='utf-8') as f:
        url_data = json.load(f)
        
    for entry_id, entry in url_data.items():
        keywords = entry.get('keywords', [])
        ocr_result = entry.get('ocr_result', [])
        url = entry.get('url', '').lower()
        
        # 检查关键词中的平台信息
        has_android = False
        has_ios = False
        
        # 检查关键词
        for keyword in keywords:
            keyword = keyword.lower()
            if keyword in ['android', 'download']:
                has_android = True
            elif keyword == 'ios':
                has_ios = True
        
        # # 如果关键词中没有找到平台信息，检查OCR结果
        # if not (has_android or has_ios):
        #     for text in ocr_result:
        #         text = text.lower()
        #         if text in ['android', 'download']:
        #             has_android = True
        #         elif text == 'ios':
        #             has_ios = True
        
        # 如果还是没有找到平台信息，检查URL
        if not (has_android or has_ios):
            if any(pattern in url for pattern in ['play.google.com', 'android', 'apk', 'download']):
                has_android = True
            if any(pattern in url for pattern in ['appstore.apple.com', 'itunes.apple.com', 'ios', 'iphone', 'ipad']):
                has_ios = True
        
        # 根据平台信息更新计数
        if has_android and has_ios:
            platform_counts['Both'] += 1
        elif has_android:
            platform_counts['Android'] += 1
        elif has_ios:
            platform_counts['iOS'] += 1

except Exception as e:
    print(f"Error reading or processing valid_url.json: {e}")
    exit()

# 过滤掉数量为0的类别
valid_platforms = {k: v for k, v in platform_counts.items() if v > 0}
labels = list(valid_platforms.keys())
sizes = list(valid_platforms.values())
total_urls = sum(sizes)

if total_urls == 0:
    print("No valid URLs found to generate chart.")
    exit()

# 画图
fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
fig.patch.set_facecolor('#f8fafd')

# 使用蓝色系的颜色映射，并跳过最浅的部分
blues_cmap = plt.colormaps['Blues']
start_sampling = 0.3
if len(labels) > 1:
    colors = [blues_cmap(start_sampling + (1.0 - start_sampling) * i / (len(labels) - 1)) for i in range(len(labels))]
    colors = colors[::-1]
else:
    # 如果只有一个类别，使用固定的蓝色
    colors = [blues_cmap(0.7)]  # 使用较深的蓝色

explode = [0.02] * len(labels)

# 绘制饼图
wedges, texts, autotexts = ax.pie(
    sizes, explode=explode, colors=colors,
    autopct='%1.1f%%', startangle=90,
    textprops={'fontsize': 8, 'color': 'white', 'weight': 'bold'},
    wedgeprops={'edgecolor': 'white', 'linewidth': 1, 'antialiased': True}
)

# 调整百分比标签位置
for i, w in enumerate(wedges):
    ang = (w.theta2 + w.theta1) / 2.
    x = w.r * 0.8 * np.cos(np.deg2rad(ang))
    y = w.r * 0.8 * np.sin(np.deg2rad(ang))
    autotexts[i].set_position((x, y))
    autotexts[i].set_color('black')

# 主标题
fig.text(
    0.14,
    0.80,
    'Platform Distribution',
    fontsize=18,
    fontweight='bold',
    color='#223a5e'
)

# 计算每一类的占比 (用于图例)
legend_labels = []
for i, label in enumerate(labels):
    percentage = (sizes[i] / total_urls) * 100 if total_urls > 0 else 0
    legend_labels.append(f"{label} ({percentage:.1f}%)")

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

# 调整布局
plt.tight_layout(rect=[0, 0, 0.75, 1])

# 保存图表
output_plot_path = os.path.join(result_dir, 'platform_distribution.png')
plt.savefig(
    output_plot_path,
    dpi=300,
    bbox_inches='tight',
    facecolor='#f8fafd',
    edgecolor='none'
)
plt.close()

print(f"Generated platform distribution chart: {output_plot_path}")
print("Platform Counts:")
for platform, count in platform_counts.items():
    print(f"{platform}: {count}")
print(f"Total URLs: {total_urls}") 