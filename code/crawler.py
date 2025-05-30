import asyncio
from logging import error
from telethon import TelegramClient
import telethon
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import CheckChatInviteRequest, ImportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest

import random
import pandas as pd
import re
import os
import socks
import csv

from telethon.tl.types import Channel, Chat, Dialog, BotApp

# 首先注册一个 telegram 账号
# 从 my.telegram.org 申请 api_id 和 api_hash
api_id = 25001850
api_hash = '1abcf966ec6c5d4ffb17686f5f59e340'

# 如果有代理，设置一下
host = "127.0.0.1"  # a valid host
port = 7890  # a valid port
proxy = (socks.SOCKS5, host, port)

client = TelegramClient("anon", api_id, api_hash, proxy=proxy)

current_dir = os.getcwd()

f = open(current_dir+'/url.csv', 'w', encoding='utf-8-sig')
csv_writer = csv.writer(f)
csv_writer.writerow(["url", "channel_id"])

with open(current_dir+'/300KeyWord.txt', 'r') as f1:
    keywords = f1.read().splitlines()
keywords = [keyword.strip() for keyword in keywords]
random.shuffle(keywords)

keyword_num = 2 # 向 bot 发送的关键词数量


async def main():
    global groups, edges, to_be_processed, done, package_dir

    me = await client.get_me() # Getting information about yourself
    
    await join_channels_from_file() # join bot channel from bots.txt
    
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id, 'with type: ', type(dialog.entity))
        await search_for_channels(dialog.entity)


        
async def search_for_channels(entity):
    async with client.conversation(entity) as conv:
        #向 bot 发送消息
        words = random.sample(keywords, keyword_num) # 随机选取 num 个关键词发送
        for word in words:
            try:
                await conv.send_message(word)
                message = await conv.get_response()
                # Check if the message is a valid response
                if not message or not hasattr(message, 'entities'):
                    print(f"No valid response for {word} in {entity.title}")
                    continue
                print(f"Sent message: {word} to {entity.title}")
                for i in message.entities:
                    if hasattr(i, 'url'):
                        csv_writer.writerow([i.url, entity.id])
                # asyncio.sleep(2) # 不要太快发送消息，容易被禁言
            except:
                print("Error: Channel ", entity.title, " does not respond to messages.")
                return

async def join_channels_from_file():
    with open(current_dir + '/bot.txt', 'r') as f:
        bot_urls = f.read().splitlines()
    for url in bot_urls:
        try:
            await join_channel(url)
        except:
            continue

async def join_channel(url):
    try:
        result = await client(JoinChannelRequest(url))
        print("Joined the channel:", result.chats[0].title)
    except:
        print("Failed to join the channel:", url)         


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
        client.disconnect()
