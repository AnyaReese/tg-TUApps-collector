import json
from paddleocr import PaddleOCR
import time
import os
import re
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from pathlib import Path


download_dir = "./data/others"
os.makedirs(download_dir, exist_ok=True)
output_file = "./data/ocr_results1931.json"


# 初始化OCR模型
ocr = PaddleOCR(
    use_textline_orientation=True,
    lang="en"
)


def read_urls_from_json(file_path):
    # 从JSON文件中读取URL
    with open(file_path, "r", encoding="utf-8") as file:
        urls = json.load(file)
    return urls


def ocr_recognize_text(image_path):
    # 使用OCR识别文本
    result = ocr.predict(image_path)
    for res in result:
        text = res["rec_texts"]
        return text


def extract_keywords_links(ocr_result, num):
    # 提取下载链接
    keywords = []
    # 将OCR结果转换为小写以便不区分大小写进行匹配
    ocr_lower = ocr_result.lower() if isinstance(ocr_result, str) else str(ocr_result).lower()
    
    # 定义关键词及其对应的匹配词列表
    keyword_matches = {
        "download": ["download", "下载"],
        "ios": ["ios", "苹果", "iphone", "ipad"],
        "apk": ["apk"],
        "android": ["android", "安卓"],
        "web": ["web", "网页", "网站"],
        "vpn": ["vpn"],
        "app": ["app", "应用"],
        "game": ["game", "游戏"],
        "free": ["free", "免费"],
        "porn": ["porn", "色情"],
        "女优": ["女优", "真人"],
        "adult": ["adult", "成人"],
        "casino": ["casino", "赌场", "博彩", "棋牌", "麻将", "扑克", "澳门"],
        "sports": ["sports", "体育"],
        "money": ["money", "钱", "$", "￥", ]
        # 添加更多关键词及其匹配词列表
    }
    
    # 对每个关键词进行部分匹配检查
    for keyword, match_terms in keyword_matches.items():
        for term in match_terms:
            if term in ocr_lower:
                keywords.append(keyword)
                break  # 一旦找到匹配项，就跳出内层循环
    
    return keywords

def save_results_to_json(results, output_file):
    # 将结果保存为JSON格式
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    print(f"结果已保存到 {output_file}")

def append_result_to_json(file_path, new_data):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    data.update(new_data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def extract_number(file):
    match = re.search(r"\[([0-9]+)\]", file.name)
    if match:
        return int(match.group(1))
    else:
        return -1

# 主程序
if __name__ == "__main__":
    # 从JSON文件中读取URL
    print("start")
    urls = read_urls_from_json('./data/msg_history_urls_filtered.json')

    # OCR识别
    path = Path(download_dir)
    if os.path.getsize(output_file) == 0:
        results = {}  # 或者 results = []，根据你的用途选择空字典或空列表
        print(f"文件 {output_file} 是空的，已返回空结果。")
    else:
        with open(output_file, 'r', encoding='utf-8') as file:
            results = json.load(file)
    # times 为 results 中最后一个元素的counting
    times = 0
    if results:
        counting_values = [item.get("counting", -1) for item in results.values() if "counting" in item]
        if counting_values:
            times = max(counting_values) + 1
    
    files = [file for file in path.iterdir() if file.is_file()]
    files_sorted = sorted(files, key=extract_number)
    for file in files_sorted:
        if file.is_file():
            print(f"ocring {file.name}")
            match = re.search(r"\[([0-9]+)\]....", file.name)
            number = match.group(1)
            num = int(number)
            if num >= 1938:   # 上界
                break 
            if num >= 1932:    # 下届
                url = urls[num]
                ocr_result = ocr_recognize_text(f"./data/others/{file.name}")
                keywords = extract_keywords_links(ocr_result,number)

                if keywords:
                    result1 = {
                        number: {
                            "url": url,
                            "ocr_result": ocr_result,
                            "keywords": keywords,
                            "counting": times
                        }
                    }
                    append_result_to_json(output_file, result1)
                    print(f"{num} has been writen.")
                    times = times + 1
    # 保存结果到JSON文件
    # save_results_to_json(results, output_file)