import json
import os
import csv
input_file="./data/ocr_results1931.json"
output_file="./data/valid_url.json"
result="./data/result.csv"

def filter_download_related(input_file, output_file):
    # 下载相关关键词
    download_keywords = {"download","ios","apk","android"}

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            filtered_data = json.load(f)
    else:
        filtered_data = {}

    for key, value in data.items():
        keywords = value.get("keywords", [])
        if any(k for k in keywords if any(d in k for d in download_keywords)):
            filtered_data[key] = value

    # 保存结果到新文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)

    print(f"筛选后保存了 {len(filtered_data)} 条包含下载相关关键词的记录到 {output_file}")

def get_valid_url(input_file,output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(output_file, "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["url"]) 
        for key, value in data.items():
            url = value.get("url", "")
            writer.writerow([url])

if __name__=="__main__":
    # filter_download_related(input_file, output_file)
    get_valid_url(output_file,result)