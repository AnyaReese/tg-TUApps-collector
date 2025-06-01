# telegram 地下应用收集程序

## 介绍

1. 根据 [Beyond App Markets: Demystifying Underground Mobile App Distribution Via Telegram](https://arxiv.org/pdf/2408.03482) 这篇文章的第 "3.2 Dataset Collection" 节算法实现。
2. 首先注册一个 Telegram 账号，如果手机收不到验证码，可以先注册 [Telegram X](https://github.com/TGX-Android/Telegram-X/releases)，二者账号通用，后者可以给中国地区手机号发消息。
3. 申请开发者 API，参考[https://core.telegram.org/api/obtaining_api_id]。
4. 从文章资料中已经获得下面信息：
    - `bot.txt`：搜索机器人，通过关键词搜索相关频道
    - `300keywords.txt`：关键词列表
    - `urls.json`：从频道中获取的其他频道 URL 列表
    - `msg_history_urls.json`：从频道中获取的疑似存在地下应用下载链接的 URL 列表

## 代码

建议创建虚拟环境，安装 `requirements.txt` 中的依赖。

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

`crawler.py` 当前实现：

1. 自动添加机器人
2. 向机器人发送关键词，并从回复中获得相关频道的 URL，存储在 `urls.json` 中
3. 从频道中获取消息历史，并提取疑似存在地下应用下载链接的 URL，存储在 `msg_history_urls.json` 中

## TODO

- 处理 `msg_history_urls.json` 中的 URL，爬取页面内容，通过 OCR 确定是否存在地下应用下载链接
    - 注意 `msg_history_urls.json` 中的许多 URL 是可以首先筛选掉的，比如 `x.com`、`youtube.com` 等等
    - 这一步可以单独写一个脚本来处理，不用继续在 `crawler.py` 中处理
