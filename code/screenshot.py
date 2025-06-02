import json
import time
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from pathlib import Path

download_dir = "imgs"
start_processing_from_index = 1200
failed_urls_log = "./data/failed_screenshot_urls.txt"
input_urls_file = './data/msg_history_urls_filtered.json'

os.makedirs(download_dir, exist_ok=True)

def read_urls_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = json.load(file)
        if not isinstance(urls, list):
            print(f"错误: {file_path} 中的内容不是一个列表。")
            return []
        print(f"读取到 {len(urls)} 个URL。")
        return urls
    except Exception as e:
        print(f"读取URL失败: {e}")
        return []

def try_click_continue_buttons(driver):
    possible_texts = ['进入', '继续', '我已满18岁', 'Continue', 'Access', 'Accept', 'Enter', '游客进入']
    for text in possible_texts:
        try:
            btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{text}')]"))
            )
            btn.click()
            print(f"  点击按钮: {text}")
            time.sleep(2)
            break
        except:
            continue

def visit_and_capture_screenshot(url, current_idx):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.get(url)
        time.sleep(4)
        try_click_continue_buttons(driver)

        url_content_part = url.split('//', 1)[1] if '//' in url else url
        filename_slug = re.sub(r'[\\/*?:"<>|]', '_', url_content_part)
        filename_slug = filename_slug.replace('/', '_')[:50]
        screenshot_filename = f"[{current_idx:05d}] {filename_slug}.png"
        screenshot_path = os.path.join(download_dir, screenshot_filename)

        driver.save_screenshot(screenshot_path)
        print(f"  ✅ URL #{current_idx} 的截图已保存: {screenshot_path}")
        return screenshot_path
    except TimeoutException:
        print(f"  ❌ 超时: URL #{current_idx}: {url}")
        return ""
    except WebDriverException as e:
        print(f"  ❌ WebDriver错误: URL #{current_idx}: {e}")
        return ""
    except Exception as e:
        print(f"  ❌ 其他错误: URL #{current_idx}: {e}")
        return ""
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    print("开始执行网页截图脚本...")

    urls = read_urls_from_json(input_urls_file)
    if not urls:
        print("没有读取到URL。退出。")
        exit()

    screenshots_taken = 0
    with open(failed_urls_log, 'w', encoding='utf-8') as f_log:
        f_log.write("截图失败的URL列表 (索引\tURL):\n")

    for i in range(start_processing_from_index, len(urls)):
        url = urls[i]
        print(f"处理 URL #{i}: {url}")
        screenshot_path = visit_and_capture_screenshot(url, i)

        if screenshot_path:
            screenshots_taken += 1
        else:
            with open(failed_urls_log, 'a', encoding='utf-8') as f_log:
                f_log.write(f"{i}\t{url}\n")

    print(f"\n截图完成，共成功截图 {screenshots_taken} 张。")
