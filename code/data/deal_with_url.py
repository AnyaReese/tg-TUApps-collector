import json

# 读取原文件
with open("msg_history_urls.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 过滤掉包含github的部分
filtered = [
    item
    for item in data
    if "github" not in json.dumps(item).lower()
    and "cointelegraph.com" not in json.dumps(item).lower()
    and "maps.google.com" not in json.dumps(item).lower()
    and "cn.investing.com" not in json.dumps(item).lower()
    and "x.com" not in json.dumps(item).lower()
    and "youtu.be" not in json.dumps(item).lower()
    and "tg://premium" not in json.dumps(item).lower()
    and "www.youtube.com" not in json.dumps(item).lower()
    and "www.wsj.com" not in json.dumps(item).lower()
    and "www.tiktok.com" not in json.dumps(item).lower()
    and "www.twitter.com" not in json.dumps(item).lower()
    and "www.theblock.co" not in json.dumps(item).lower()
    and "www.instagram.com" not in json.dumps(item).lower()
    and "www.facebook.com" not in json.dumps(item).lower()
    and "www.binance.com" not in json.dumps(item).lower()
    and ".jpg" not in json.dumps(item).lower()
    and "lh3.googleusercontent.com" not in json.dumps(item).lower()
    and "bjres.net" not in json.dumps(item).lower()
    and "discord.com" not in json.dumps(item).lower()
    and "www.wublockchain.xyz" not in json.dumps(item).lower()
    and "youtube.com" not in json.dumps(item).lower()
    and "tg://" not in json.dumps(item).lower()
    and "google.com" not in json.dumps(item).lower()
    and "tracker.bubblebuybot.com" not in json.dumps(item).lower()
]

# 写入新文件
with open("msg_history_urls_filtered.json", "w", encoding="utf-8") as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)

print(f"已删除包含'github'的部分，剩余{len(filtered)}条数据。")
