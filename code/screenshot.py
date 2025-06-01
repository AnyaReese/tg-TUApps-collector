import json
# from paddleocr import PaddleOCR # OCR相关，暂时注释
import time
import os
import re
import requests # 虽然requests在此版本中未直接用于截图，但保留以备将来扩展或原始意图
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from pathlib import Path

# --- 配置区 ---
# 设置截图保存目录
download_dir = "imgs"
# 设置处理URL的起始索引 (例如，如果想从第400个URL开始，设置为400)
# 如果想从头开始，设置为0
start_processing_from_index = 432
# 日志文件名，用于记录截图失败的URL
failed_urls_log = "./data/failed_screenshot_urls.txt"
# OCR结果输出文件名 (暂时不使用)
# ocr_results_output_file = "ocr_results.json"
# 输入的URL文件名
input_urls_file = './data/msg_history_urls.json'


# --- 初始化 ---
os.makedirs(download_dir, exist_ok=True)

# 初始化OCR模型 (暂时注释掉整个OCR初始化部分)
# print("正在初始化OCR模型...")
# try:
#     ocr = PaddleOCR(use_textline_orientation=True, lang='en') # lang='ch' 用于中文，'en'用于英文
#     print("OCR模型初始化成功。")
# except Exception as e:
#     print(f"OCR模型初始化失败: {e}")
#     print("请确保PaddleOCR已正确安装并配置。脚本将退出。")
#     exit()

# --- 函数定义 ---
def read_urls_from_json(file_path):
    """从JSON文件中读取URL列表"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = json.load(file)
        if not isinstance(urls, list):
            print(f"错误: {file_path} 中的内容不是一个列表。请检查文件格式。")
            return []
        print(f"从 {file_path} 中成功读取 {len(urls)} 个URL。")
        return urls
    except FileNotFoundError:
        print(f"错误: 输入文件 {file_path} 未找到。")
        return []
    except json.JSONDecodeError:
        print(f"错误: {file_path} 不是一个有效的JSON文件。")
        return []
    except Exception as e:
        print(f"读取URL文件时发生未知错误: {e}")
        return []

def visit_and_capture_screenshot(url, current_idx):
    """
    使用Selenium访问网页并截图。
    文件名包含current_idx和从URL派生的slug。
    失败时跳过。
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # 无头模式，不在前台打开浏览器窗口
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu") # 在无头模式下通常需要
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    # 您可以根据需要添加更多选项，例如代理服务器等

    driver = None  # 初始化driver为None，以便在finally块中使用
    try:
        # 尝试找到 ChromeDriver，如果不在PATH中，需要指定路径
        # 例如: driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)  # 设置页面加载超时时间（例如30秒）
        driver.get(url)
        # 等待页面加载，对于动态加载内容可能需要更智能的等待策略 (WebDriverWait)
        time.sleep(5)

        # 为文件名创建一个更具描述性的“中间部分”
        if '//' in url:
            url_content_part = url.split('//', 1)[1]
        else:
            url_content_part = url
        
        # 清理文件名：替换常见的无效字符
        filename_slug = re.sub(r'[\\/*?:"<>|]', '_', url_content_part)
        filename_slug = filename_slug.replace('/', '_') # 特别替换斜杠
        filename_slug = filename_slug[:50] # 截断到合理长度

        screenshot_filename = f"[{current_idx:05d}] {filename_slug}.png"
        screenshot_path = os.path.join(download_dir, screenshot_filename)
        
        driver.save_screenshot(screenshot_path)
        print(f"     成功: URL #{current_idx} 的截图已保存至 {screenshot_path}")
        return screenshot_path
        
    except TimeoutException:
        print(f"     失败 (超时)!! URL #{current_idx}: {url}。正在跳过。")
        return ""
    except WebDriverException as e:
        # 捕获更广泛的WebDriver异常，例如连接被拒绝等
        print(f"     失败 (WebDriverException)!! URL #{current_idx}: {url} - {type(e).__name__}。正在跳过。")
        if "net::ERR_CONNECTION_REFUSED" in str(e):
            print(f"     提示: 连接被拒绝。请检查目标URL是否可访问或网络设置。")
        elif "chrome not reachable" in str(e).lower() or "unable to discover open pages" in str(e).lower():
             print(f"     提示: ChromeDriver 可能无法启动或连接到Chrome浏览器。请检查ChromeDriver和Chrome版本兼容性以及安装。")
        return ""
    except Exception as e:
        print(f"     失败 (常规异常)!! URL #{current_idx}: {url} - {type(e).__name__}: {e}。正在跳过。")
        return ""
    finally:
        if driver:
            driver.quit()

# OCR相关函数暂时注释
# def ocr_recognize_text(image_path):
#     """使用OCR识别图像中的文本"""
#     try:
#         ocr_output = ocr.ocr(image_path, cls=True) 
#         if ocr_output and ocr_output[0]: 
#             texts = [line[1][0] for line in ocr_output[0]] 
#             full_text = "\n".join(texts) 
#             return full_text
#         else:
#             return "" 
#     except Exception as e:
#         print(f"     OCR识别图片 {image_path} 时出错: {e}")
#         return ""

# def extract_keywords_links(ocr_text, num_for_context_not_used):
#     """从OCR结果中提取预定义的关键词 (注意：当前未提取链接)"""
#     keywords = []
#     if not ocr_text: 
#         return keywords
        
#     ocr_text_lower = ocr_text.lower() 

#     keyword_map = [
#         ("download", "download"), ("下载", "download"), ("安装", "download"),
#         ("ios", "iOS"), ("苹果", "iOS"), 
#         ("apk", "apk"),
#         ("android", "android"), ("安卓", "android"),
#     ]

#     for search_term, keyword_to_add in keyword_map:
#         if search_term.lower() in ocr_text_lower: 
#             if keyword_to_add not in keywords: 
#                  keywords.append(keyword_to_add)
#     return keywords

# def save_results_to_json(results_data, output_file):
#     """将结果保存为JSON格式"""
#     try:
#         with open(output_file, 'w', encoding='utf-8') as file:
#             json.dump(results_data, file, ensure_ascii=False, indent=4)
#         print(f"结果已成功保存到 {output_file}")
#     except Exception as e:
#         print(f"保存结果到JSON文件时出错: {e}")

# --- 主程序 ---
if __name__ == "__main__":
    print("脚本开始执行 (仅截图模式)...")
    
    urls = read_urls_from_json(input_urls_file)

    if not urls:
        print("未能读取到URL，脚本将退出。")
        exit()

    # --- 1. 网页截图阶段 ---
    screenshots_taken_count = 0
    
    # 清空或创建失败日志文件
    with open(failed_urls_log, 'w', encoding='utf-8') as f_log:
        f_log.write("截图失败的URL列表 (索引\tURL):\n")

    if start_processing_from_index >= len(urls):
        print(f"错误: 起始索引 {start_processing_from_index} 超出了URL列表的范围 (总长度 {len(urls)})。")
    else:
        print(f"\n--- 开始网页截图阶段 (从索引 {start_processing_from_index} 开始) ---")
        # 这里的 'i' 是原始urls列表中的绝对索引
        for i in range(start_processing_from_index, len(urls)):
            current_url = urls[i]
            print(f"正在处理 URL #{i}: {current_url}")
            
            screenshot_path = visit_and_capture_screenshot(current_url, i)
            
            if screenshot_path:
                screenshots_taken_count += 1
            else:
                # 记录失败的URL及其原始索引
                with open(failed_urls_log, 'a', encoding='utf-8') as f_log:
                    f_log.write(f"{i}\t{current_url}\n")
        
        print(f"\n网页截图阶段完成。")
        print(f"成功截取 {screenshots_taken_count} 张图片。")
        if os.path.exists(failed_urls_log) and os.path.getsize(failed_urls_log) > len("截图失败的URL列表 (索引\tURL):\n"): # 检查文件是否非空（除了表头）
            print(f"截图失败的URL详情已记录在: {failed_urls_log}")
        elif screenshots_taken_count > 0 : # 如果有截图成功，但日志文件为空，说明全部成功
             print("所有在处理范围内的URL均截图成功。")
        else: # 如果没有截图成功，并且日志文件也为空（或只有表头），说明没有进行有效操作或所有尝试都失败了
            if len(urls) > start_processing_from_index : # 确保有URL在处理范围内
                 print("未能成功截取任何图片，请检查日志和错误信息。")
            else:
                 print("没有在指定处理范围内的URL进行截图操作。")


    # --- 2. OCR识别与关键词提取阶段 (暂时注释) ---
    # print(f"\n--- OCR识别与关键词提取阶段已跳过 ---")
    # ocr_results = {}
    # image_files_processed = 0
    
    # image_dir_path = Path(download_dir)
    # if not image_dir_path.exists():
    #     print(f"错误：图片目录 {download_dir} 不存在。跳过OCR阶段。")
    # else:
    #     image_files = [f for f in image_dir_path.iterdir() if f.is_file() and f.name.lower().endswith('.png')]
    #     if not image_files:
    #         print(f"在目录 {download_dir} 中没有找到PNG图片文件进行OCR处理。")
    #     else:
    #         print(f"找到 {len(image_files)} 个PNG图片文件进行处理。")
    #         for image_file_path in image_files:
    #             print(f"  正在OCR处理图片: {image_file_path.name}")
    #             match = re.search(r"\[(\d{5})\]", image_file_path.name)
    #             if match:
    #                 original_index_str = match.group(1)
    #                 try:
    #                     original_index_int = int(original_index_str)
    #                     if original_index_int < len(urls):
    #                         corresponding_url = urls[original_index_int]
    #                         ocr_text_result = ocr_recognize_text(str(image_file_path))
    #                         extracted_keywords = extract_keywords_links(ocr_text_result, original_index_int)
    #                         ocr_results[original_index_str] = {
    #                             "url": corresponding_url,
    #                             "ocr_result": ocr_text_result,
    #                             "keywords": extracted_keywords,
    #                             "image_filename": image_file_path.name
    #                         }
    #                         image_files_processed += 1
    #                     else:
    #                         print(f"     警告: 从文件名 {image_file_path.name} 提取的索引 {original_index_int} 超出原始URL列表范围。")
    #                 except ValueError:
    #                     print(f"     警告: 无法将文件名 {image_file_path.name} 中的索引 '{original_index_str}' 转换为整数。")
    #             else:
    #                 print(f"     警告: 无法从文件名 {image_file_path.name} 中提取索引。跳过此文件。")
            
    #         print(f"\nOCR识别与关键词提取阶段完成。")
    #         print(f"成功处理了 {image_files_processed} 张图片。")

    #         # --- 3. 保存结果到JSON文件 (暂时注释) ---
    #         if ocr_results:
    #             # save_results_to_json(ocr_results, ocr_results_output_file)
    #             print(f"OCR结果已生成但未保存 (功能已注释)。共有 {len(ocr_results)} 条记录。")
    #         else:
    #             print("没有生成OCR结果。")

    print("\n脚本执行完毕。")
