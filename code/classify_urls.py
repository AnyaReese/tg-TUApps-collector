import json
from urllib.parse import urlparse
import os # Import os module

# Define keywords for classification
porn_keywords = ['sex', 'porn', 'adult', 'erotic', '情色', '成人', '色情',"限制级", 'nude', 'XXX', 'hentai', 'jav', 'эротика', 'fetish', '黄色', '福利', '写真'
,"高清直播","美女","换妻","日本","歐美","资源", '淫', '色'] 
gambling_keywords = ['casino', 'bet', 'gambling', 'poker', '投注', '赌博', '娱乐场',
                     "sports", "体育","赌场", "博彩", "棋牌", "麻将", '扑克', "澳门", "$", "￥",
                     'win', 'jackpot', 'bonus', 'roulette', 'blackjack', 'slots', 'betting', 'odds', 'prize', 'wager', 'lotto', '中奖', '红包', '开奖', '彩票',"交易"]
piracy_keywords = ['工具箱','专业','crack', 'patch', 'keygen', 'serial', 'warez', 'free download', '盗版', '破解', '免费下载', 'torrent', '磁力', 'thunder', 'bt', '下载器', '盗版', '破解版', '免费', '资源下载', '激活码', '注册码', 'PJ', 'GF','整合'] # Keywords for pirated software
ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'neural network', 'gpt', 'llm', '大模型', '人工智能', '机器学习', '深度学习', '算法', '智能', 'ai工具', 'ai生成', 'ai绘画', 'ai写作', 'ai视频', 'ai语音', 'ai聊天', 'ai翻译', 'ai创作'] # Keywords for AI
blockchain_web3_keywords = ['blockchain', 'web3', 'crypto', 'bitcoin', 'ethereum', 'nft', 'defi', 'dao', 'dex', 'wallet', 'coin', 'token', '智能合约', '区块链', '加密货币', '数字货币', '钱包', '挖矿', '去中心化', '链', '合约', '矿池'] # Keywords for Blockchain/Web3

def classify_entry(entry, porn_kw, gambling_kw, piracy_kw, ai_kw, blockchain_web3_kw):
    """Classify an entry based on keywords in URL, hostname, path, or ocr_result."""
    url = entry.get('url')
    ocr_result = entry.get('ocr_result', [])

    if not url or not isinstance(url, str):
        # print(f"Skipping invalid entry: {entry}") # Optional: log invalid entries
        return '其他' # Cannot classify without a valid URL

    try:
        parsed_url = urlparse(url)
        # Check hostname and path for keywords (case-insensitive)
        target_string = ""
        if parsed_url.hostname:
            target_string += parsed_url.hostname.lower()
        if parsed_url.path:
             target_string += parsed_url.path.lower()

        # Also include OCR result text for keyword checking
        if isinstance(ocr_result, list):
             target_string += " ".join(map(str, ocr_result)).lower()
        elif isinstance(ocr_result, str):
             target_string += ocr_result.lower()

        # Classification order: Porn -> Gambling -> Piracy -> AI -> Blockchain/Web3 -> Other
        for kw in porn_kw:
            if kw in target_string:
                return '色情软件'
        
        for kw in gambling_kw:
            if kw in target_string:
                return '赌博软件'

        for kw in piracy_kw:
             if kw in target_string:
                  return '盗版软件'

        for kw in ai_kw:
             if kw in target_string:
                  return 'AI'

        for kw in blockchain_web3_kw:
             if kw in target_string:
                  return '区块链web3'

        return '其他' # Default category
    except Exception as e:
        print(f"Error processing entry for URL {url}: {e}")
        return '其他' # Default to other if processing fails

# Load data from the JSON file
file_path = './data/valid_url.json'
data = {}
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {file_path}")
    exit()

# Classify entries
classified_urls = {
    '色情软件': [],
    '赌博软件': [],
    '盗版软件': [],
    'AI': [],
    '区块链web3': [],
    '其他': []
}

# Iterate through the dictionary items and classify each entry
for key, entry in data.items():
    category = classify_entry(entry, porn_keywords, gambling_keywords, piracy_keywords, ai_keywords, blockchain_web3_keywords)
    # Store the original URL in the classified list
    url = entry.get('url')
    if url and isinstance(url, str):
         classified_urls[category].append(url)
    # else: # This case is handled inside classify_entry now
        # print(f"Skipping entry without valid URL for key {key}")

# Print classification summary
total_classified_count = sum(len(urls) for urls in classified_urls.values())
print("URL Classification Summary:")
print(f"色情软件 (Pornographic Software): {len(classified_urls['色情软件'])} URLs")
print(f"赌博软件 (Gambling Software): {len(classified_urls['赌博软件'])} URLs")
print(f"盗版软件 (Pirated Software): {len(classified_urls['盗版软件'])} URLs")
print(f"AI: {len(classified_urls['AI'])} URLs")
print(f"区块链web3 (Blockchain/Web3): {len(classified_urls['区块链web3'])} URLs")
print(f"其他 (Other): {len(classified_urls['其他'])} URLs")
# The total count should be the number of entries with valid URLs
valid_url_count_in_data = sum(1 for entry in data.values() if isinstance(entry, dict) and isinstance(entry.get('url'), str))
print(f"Total Entries with Valid URLs Processed: {valid_url_count_in_data} URLs")

# Save the classified URLs to new files in the ./result/ directory
output_dir = './result'
os.makedirs(output_dir, exist_ok=True) # Create output directory if it doesn't exist

for category, url_list in classified_urls.items():
    # Replace spaces and Chinese characters in category for a cleaner filename (optional, but good practice)
    # Simple replacement, might need more robust handling for complex names
    safe_category_name = category.replace(' ', '_').replace('软件', '_software').replace('区块链web3', 'blockchain_web3')
    
    output_filename = os.path.join(output_dir, f'{safe_category_name}_urls.json')
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            json.dump(url_list, outfile, indent=4, ensure_ascii=False)
        print(f"Saved {len(url_list)} {category} URLs to {output_filename}")
    except Exception as e:
        print(f"Error saving {category} URLs to {output_filename}: {e}") 