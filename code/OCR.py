import json
from paddleocr import PaddleOCR
import time
import os
import re
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from pathlib import Path


# 设置下载目录
download_dir = "imgs"
os.makedirs(download_dir, exist_ok=True)

# cnt=400

# 初始化OCR模型
ocr = PaddleOCR(use_textline_orientation=True, lang='en')

def read_urls_from_json(file_path):
    # 从JSON文件中读取URL
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = json.load(file)
    return urls

# def visit_and_capture_screenshot(url):
#     # 使用Selenium访问网页并截图
#     chrome_options = webdriver.ChromeOptions()
#     try:
#         driver = webdriver.Chrome(options=chrome_options)
#         driver.get(url)
#         time.sleep(5)  # 等待页面加载
#         screenshot_path = f"{download_dir}/[{cnt:05}] {url.split('//')[-1].replace('/', '_')[:5]}.png"
#         driver.save_screenshot(screenshot_path)
#     except WebDriverException as e:
#         driver.quit()
#         print(f"     #{cnt}:Failed!!")
#         return ""
#     return screenshot_path

def ocr_recognize_text(image_path):
    # 使用OCR识别文本
    result = ocr.predict(image_path)
    for res in result:
        text = res["rec_texts"]
        return text

def extract_keywords_links(ocr_result,num):
    # 提取下载链接
    keywords = []
    if "download" in ocr_result or "下载" in ocr_result:
        keywords.append("download")
    if "iOS" in ocr_result or "IOS" in ocr_result or "ios" in ocr_result or "苹果" in ocr_result:
        keywords.append("iOS")
    if "apk" in ocr_result:
        keywords.append("apk")
    if "android" in ocr_result or "安卓" in ocr_result or "Android" in ocr_result:
        keywords.append("android")
    if "web" in ocr_result:
        keywords.append("web")
    if "vpn" in ocr_result or "VPN" in ocr_result:
        keywords.append("vpn")
    if "free" in ocr_result or "免费" in ocr_result:
        keywords.append("free")
    if "porn" in ocr_result or "PORN" in ocr_result or "色情" in ocr_result:
        keywords.append("porn")
    if "女优" in ocr_result:
        keywords.append("女优")
    if "成人" in ocr_result or "ADULT" in ocr_result or "adult" in ocr_result:
        keywords.append("adult")
    if "赌场" in ocr_result or "casino" in ocr_result or "CASINO" in ocr_result:
        keywords.append("casino")
    if "体育" in ocr_result or "sports" in ocr_result:
        keywords.append("sports")
    if "$" in ocr_result or "￥" in ocr_result or "money" in ocr_result or "MONEY" in ocr_result:
        keywords.append("money")
    return keywords

def save_results_to_json(results, output_file):
    # 将结果保存为JSON格式
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    print(f"结果已保存到 {output_file}")


# 主程序
if __name__ == "__main__":
    # 从JSON文件中读取URL
    print("start")
    urls = read_urls_from_json('msg_history_urls.json')

    # url_list = urls[400:]
    # for url in url_list:
    #     print(f"Visiting: {url}")
    #     screenshot_path = visit_and_capture_screenshot(url)
    #     print(f"Captured screenshot: {screenshot_path}")
    #     cnt = cnt + 1

    # OCR识别
    path = Path(download_dir)
    results = {}
    times = 0
    for file in path.iterdir():
        if file.is_file():
            print(f"ocring {file.name}")
            match = re.search(r"\[([0-9]+)\]....", file.name)
            number = match.group(1)
            num = int(number)
            url = urls[num]
            ocr_result = ocr_recognize_text(f"imgs/{file.name}")
            keywords = extract_keywords_links(ocr_result,number)
            results[number] = {
                "url": url,
                "ocr_result": ocr_result,
                "keywords": keywords
            }
    # 保存结果到JSON文件
    save_results_to_json(results, "ocr_results.json")