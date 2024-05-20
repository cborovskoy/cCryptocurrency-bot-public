from dataclasses import dataclass
from pathlib import PurePath, Path
import configparser

LABEL_1M = '1m'
LABEL_15M = '15m'
LABEL_1H = '60m'


@dataclass
class Config:
    bot_token: str
    admin_id: int
    binance_invite: str
    coinbase_invite: str


def load_config(path=None) -> Config:
    path = PurePath(Path(__file__).parents[1], 'bot.ini') if path is None else path
    config = configparser.ConfigParser()
    config.read(path)
    config = config['DEFAULT']

    return Config(bot_token=config.get('bot_token'),
                  admin_id=config.get('admin_id'),
                  binance_invite=config.get('binance_invite'),
                  coinbase_invite=config.get('coinbase_invite'))
