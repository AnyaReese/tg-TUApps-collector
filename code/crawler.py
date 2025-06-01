import asyncio
from logging import error
from telethon import TelegramClient
import telethon
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import CheckChatInviteRequest, ImportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest

import random
import re
import os
import socks
import json

from telethon.tl.types import Channel, Chat, Dialog, BotApp

# 首先注册一个 telegram 账号
# 从 my.telegram.org 申请 api_id 和 api_hash
api_id = 25001850
api_hash = '1abcf966ec6c5d4ffb17686f5f59e340'

# 如果有代理，设置一下
host = '127.0.0.1'  # a valid host
port = 1080  # a valid port
proxy = (socks.HTTP, host, port)

client = TelegramClient('anon', api_id, api_hash, proxy=proxy)

with open('300keywords.txt', 'r') as f:
    keywords = list(set(keyword.strip() for keyword in f.read().splitlines() if keyword.strip()))
random.shuffle(keywords)

keyword_num = 2 # 向 bot 发送的关键词数量


async def main():
    me = await client.get_me() # Getting information about yourself
    dialogs = await client.get_dialogs()

    # await join_channels_from_file()  # join bot channel from bots.txt

    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as f:
            urls = json.load(f)
    else:
        urls = await search_channel_urls()

    flat_urls = list(set(url for url_list in urls.values() for url in url_list))
    print(f'Found {len(flat_urls)} unique URLs across {len(urls)} channels.')

    if os.path.exists('msg_history_urls.json'):
        with open('msg_history_urls.json', 'r') as f:
            msg_history_urls = json.load(f)
    else:
        msg_history_urls = []
        for url in flat_urls:
            msg_history_urls.extend(await search_channel_history(url))
        msg_history_urls = list(set(msg_history_urls))  # 去重
        msg_history_urls.sort()
        with open('msg_history_urls.json', 'w') as f:
            json.dump(msg_history_urls, f, indent=4, ensure_ascii=False)
    print(f'Found {len(msg_history_urls)} unique message history URLs.')


async def search_channel_urls():
    urls: dict[int, list[str]] = {}
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id, 'with type', type(dialog.entity))
        for url in await search_single_channel(dialog.entity):
            channel_id, url = url
            if channel_id not in urls:
                urls[channel_id] = []
            if url not in urls[channel_id]:
                urls[channel_id].append(url)
    with open('urls.json', 'w') as f:
        json.dump(urls, f, indent=4, ensure_ascii=False)
    return urls


async def search_channel_history(ident: str) -> list[str]:
    try:
        entity = await client.get_entity(ident)
    except:
        print(f'Error: Could not find entity with identifier {ident}.')
        return []
    if not isinstance(entity, Channel):
        print(f'Entity {ident} is not a channel.')
        return []

    urls = []
    print(f'Searching in channel: {entity.title} ({entity.id})')

    async for message in client.iter_messages(entity, limit=1000):  # 调整 limit 来控制获取的消息数量
        try:
            if message.entities:
                for msg in message.entities:
                    if hasattr(msg, 'url'):
                        urls.append(msg.url)
        except:
            print(f'Error processing message {message} in {entity.title}')
            continue
    print(f'Found {len(urls)} URLs in channel: {entity.title} ({entity.id})')
    return urls


async def search_single_channel(entity) -> set[tuple[int, str]]:
    urls: set[tuple[int, str]] = set()

    pattern = re.compile(r'^(https://t.me/[^/?]+)')  # 匹配 Telegram URL

    async with client.conversation(entity) as conv:
        # 向 bot 发送消息
        words = random.sample(keywords, keyword_num)  # 随机选取 num 个关键词发送
        for word in words:
            try:
                await conv.send_message(word)
                message = await conv.get_response(timeout=5)
                # Check if the message is a valid response
                if not message or not hasattr(message, 'entities'):
                    print(f'No valid response for {word} in {entity.title}')
                    continue
                print(f'Sent message: {word} to {entity.title}')
                for msg in message.entities:
                    if hasattr(msg, 'url'):
                        if match := pattern.search(msg.url):
                            urls.add((entity.id, match.group(1)))
                await asyncio.sleep(5)  # 不要太快发送消息，容易被禁言
            except:
                print('Error: Channel', getattr(entity, 'title', entity), 'does not respond to messages.')
                continue
    return urls


async def join_channels_from_file():
    with open('bot.txt', 'r') as f:
        bot_urls = f.read().splitlines()
    for url in bot_urls:
        try:
            await join_channel(url)
        except:
            pass


async def join_channel(url):
    try:
        result = await client(JoinChannelRequest(url))
        print('Joined the channel:', result.chats[0].title)
    except:
        print('Failed to join the channel:', url)


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
        client.disconnect()
