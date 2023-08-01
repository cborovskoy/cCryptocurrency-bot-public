import os
from dataclasses import dataclass
from pathlib import PurePath, Path
import configparser

LABEL_TIME = 'Time'
LABEL_1M = '1m'
LABEL_15M = '15m'
LABEL_1H = '1H'

# chart types
CT_CANDLESTICK = 'candlestick'
CT_LINE = 'LINE'
CT_5MINUTES_TEST = 'CT_5MINUTES_TEST'


@dataclass
class DbConfig:
    path: str
    # host: str
    # password: str
    # user: str
    # database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list
    # use_redis: bool


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    binance_invite: str
    coinbase_invite: str


def __is_prod():
    if 'OS' in os.environ and os.environ['OS'] == 'Windows_NT':
        return False
    else:
        return True


def load_config(path=None):
    path = PurePath(Path(__file__).parents[1], 'bot.ini') if path is None else path

    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["test" if __is_prod else "prod"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("tg_token"),
            admin_ids=list(map(int, tg_bot.get("admins").split(',')))
        ),
        db=DbConfig(path=tg_bot.get("base_path")),
        binance_invite=config['invites'].get('binance_invite'),
        coinbase_invite=config['invites'].get('coinbase_invite')

    )
