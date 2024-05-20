from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from src.config import LABEL_15M, LABEL_1H, LABEL_1M


def get_main_kb(coinbase_invite: str, binance_invite: str, interval: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(*[InlineKeyboardButton(text=f'·{t}·' if cd == interval else t, callback_data=cd)
                  for cd, t in {LABEL_1M: '1m [1d]', LABEL_15M: '15m [2d]', LABEL_1H: '1h [3d]'}.items()])
    builder.row(InlineKeyboardButton(text='open BINANCE', url=binance_invite),
                InlineKeyboardButton(text='open Coinbase', url=coinbase_invite))
    return builder.as_markup()
