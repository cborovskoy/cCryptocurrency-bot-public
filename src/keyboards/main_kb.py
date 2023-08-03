from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from src.config import LABEL_15M, LABEL_1H, LABEL_1M


def get_main_kb(coinbase_invite: str, binance_invite: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='1m [1d]', callback_data=LABEL_1M),
                InlineKeyboardButton(text='15m [2d]', callback_data=LABEL_15M),
                InlineKeyboardButton(text='1h [3d]', callback_data=LABEL_1H))
    builder.row(InlineKeyboardButton(text='open BINANCE', url=binance_invite),
                InlineKeyboardButton(text='open Coinbase', url=coinbase_invite))
    return builder.as_markup()
