import json

# 加载原始数据
with open("msg_history_urls.json", "r", encoding="utf-8") as f:
    data = json.load(f)

blacklist_substrings = [
    "github", "cointelegraph.com", "maps.google.com", "cn.investing.com",
    "x.com", "youtu.be", "tg://premium", "www.youtube.com", "www.wsj.com",
    "www.tiktok.com", "www.twitter.com", "www.theblock.co", "www.instagram.com",
    "www.facebook.com", "www.binance.com", ".jpg", "lh3.googleusercontent.com",
    "bjres.net", "discord.com", "www.wublockchain.xyz", "youtube.com",
    "tg://", "google.com", "tracker.bubblebuybot.com", "https://telegra.ph/", "discord.gg"
]

def is_blacklisted(url: str) -> bool:
    url_lower = url.lower()
    return any(substr in url_lower for substr in blacklist_substrings)

def common_prefix_length(s1: str, s2: str) -> int:
    match_len = 0
    for a, b in zip(s1, s2):
        if a == b:
            match_len += 1
        else:
            break
    return match_len

# 执行过滤逻辑
filtered = []
prev_url = ""

for item in data:
    if is_blacklisted(item):
        continue
    if common_prefix_length(prev_url, item) > 20:
        continue
    filtered.append(item)
    prev_url = item

# 保存结果
with open("msg_history_urls_filtered.json", "w", encoding="utf-8") as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)

print(f"过滤完成，剩余 {len(filtered)} 条有效 URL。")
