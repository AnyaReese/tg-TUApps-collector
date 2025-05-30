# Telegram Underground App Distribution Analysis Project

## 1. Project Overview

This project aims to investigate the distribution of underground mobile applications (related to pornography, gambling, financial fraud, etc.) via the Telegram platform. The process involves:

1.  **Channel Discovery:** Identifying relevant Telegram channels and groups using bots, third-party websites, and snowballing techniques.
2.  **URL Extraction:** Crawling historical messages from these channels to extract URLs.
3.  **Download Page Identification & App Acquisition:** Visiting collected URLs to identify app download pages, potentially downloading app samples.
4.  **Content Risk Assessment (Innovation):** Utilizing Optical Character Recognition (OCR) on webpage screenshots to analyze page content for keywords associated with high-risk activities.
5.  **Data Analysis & Reporting:** Analyzing the collected data to understand the characteristics of this underground ecosystem.

This project is for academic research purposes as part of a Social Network Analysis course.

## 2. Directory Structure

```
lab2/
├── code/
│   ├── crawler.py                 # Telegram data crawler (Telethon)
│   ├── data/                      # Processed data and results
│       ├── url.csv    # Output from crawler.py, input for downloader_analyzer.py
│       ├── 300KeyWord.txt     # General keywords for searching channels via bots
│       ├── bot.txt            # Initial bot usernames for crawling
│       ├── readme.md          # readme
└── topic.md                       # Project assignment description
```
