import time
from io import BytesIO
from pathlib import Path
from random import randint
from typing import NamedTuple, IO

import requests
import toml
from telegram import Bot, InputMediaPhoto
from telegram.ext import Updater


class TelegramConfig(NamedTuple):
    channel: str
    token: str


class CrawlerConfig(NamedTuple):
    origin: str
    source: str
    min_delay: int
    max_delay: int


class Config(NamedTuple):
    telegram: TelegramConfig
    crawler: CrawlerConfig


def parse_config(f):
    data = toml.load(f)
    return Config(
        telegram=TelegramConfig(**data['telegram']),
        crawler=CrawlerConfig(**data['crawler'])
    )


def randomly_sleep(config: CrawlerConfig):
    t = randint(config.min_delay, config.max_delay)
    print("Sleeping", t, 'min')
    time.sleep(t * 60)


def get_image(config: CrawlerConfig) -> IO:
    s = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    s.get(config.origin, headers=headers)
    headers['Referer'] = config.origin
    resp = s.get(config.source, headers=headers)
    bio = BytesIO()
    bio.write(resp.content)
    bio.seek(0)
    return bio


def post_image(config: TelegramConfig, img: IO):
    updater = Updater(config.token, use_context=False)
    bot: Bot = updater.bot
    media = InputMediaPhoto(img)
    bot.send_media_group(f"@{config.channel}", [media])


def main():
    config_path = Path(__file__).parent / 'config.toml'
    with open(config_path) as f:
        config = parse_config(f)
    bio = get_image(config.crawler)
    post_image(config.telegram, bio)


if __name__ == '__main__':
    main()
