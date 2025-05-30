# telegram 地下应用收集程序

## 介绍

1. 根据 [Beyond App Markets: Demystifying Underground Mobile App Distribution Via Telegram](https://arxiv.org/pdf/2408.03482) 这篇文章的第 "3.2 Dataset Collection" 节做算法实现。
2. 首先注册一个 Telegram 账号，如果手机收不到验证码，可以先注册 [Telegram X](https://github.com/TGX-Android/Telegram-X/releases)，二者账号通用，后者可以给中国地区手机号发消息。
3. 申请开发者 API，参考[https://core.telegram.org/api/obtaining_api_id]。
4. 从文章资料中已经获得 `bot.txt` 和 `300KeyWord.txt`，前者是搜索机器人，通过关键词搜索相关频道；后者是关键词列表。

## 代码

当前实现：

1. 自动添加机器人
2. 向机器人发送关键词，并从回复中获得相关频道的 URL，存储在 `url.csv` 中
