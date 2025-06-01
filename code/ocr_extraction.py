
import os
import re
import json
from pathlib import Path
from paddleocr import PaddleOCR
from tqdm import tqdm

# 配置路径
IMG_DIR = "./data/img"
URL_FILE = "./data/msg_history_urls.json"
OUTPUT_JSON = "./data/ocr_results.json"

# 初始化 OCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# 加载 URL 列表
with open(URL_FILE, 'r', encoding='utf-8') as f:
    urls = json.load(f)

# 遍历图片文件夹
results = []

for image_path in tqdm(sorted(Path(IMG_DIR).glob("*.png"))):
    match = re.search(r"\[(\d{5})\]", image_path.name)
    if not match:
        continue
    index = int(match.group(1))
    if index >= len(urls):
        continue
    url = urls[index]
    ocr_output = ocr.ocr(str(image_path), cls=True)
    texts = [line[1][0] for line in ocr_output[0]] if ocr_output and ocr_output[0] else []
    full_text = "\n".join(texts).lower()

    keyword_map = [
        ("download", "download"), ("下载", "download"), ("安装", "download"),
        ("ios", "iOS"), ("苹果", "iOS"),
        ("apk", "apk"),
        ("android", "android"), ("安卓", "android"),
    ]
    matched_keywords = list({v for k, v in keyword_map if k in full_text})

    results.append({
        "id": index,
        "url": url,
        "keywords": matched_keywords,
        "ocr_text": full_text
    })

# 保存为 JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"OCR 提取完成，共处理 {len(results)} 张图片，输出保存至 {OUTPUT_JSON}")
