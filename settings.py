import os

LABEL_TIME = 'Time'
LABEL_1M = '1m'
LABEL_15M = '15m'
LABEL_1H = '1H'

TG_TOKEN_PROD = ""
TG_TOKEN_TEST = ''

BASE_PATH_PROD = '/ccryptocurrency/price_base.db'
BASE_PATH_TEST = 'price_base.db'

BINANCE_INVITE = 'https://www.binance.com/ru/register?ref=19917906'
COINBASE_INVITE = 'https://www.coinbase.com/join/wood_ct8'
COINDESK_API_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'

# chart types
CT_CANDLESTICK = 'candlestick'
CT_LINE = 'LINE'
CT_5MINUTES_TEST = 'CT_5MINUTES_TEST'


def is_prod():
    if 'OS' in os.environ and os.environ['OS'] == 'Windows_NT':
        return False
    else:
        return True


def get_path_chart(label_interval):
    start_part_of_path = '/home/constantine/ccryptocurrency/' if is_prod() else ''
    paths = {
        LABEL_TIME: f'{start_part_of_path}chart_time',
        LABEL_1M: f'{start_part_of_path}chart_1m',
        LABEL_15M: f'{start_part_of_path}chart_15m',
        LABEL_1H: f'{start_part_of_path}chart_1h',
    }
    return paths[label_interval]


def get_tg_token():
    return TG_TOKEN_PROD if is_prod() else TG_TOKEN_TEST


def get_base_path():
    return BASE_PATH_PROD if is_prod() else BASE_PATH_TEST


if __name__ == '__main__':
    print(get_path_chart())
