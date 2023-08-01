from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from src.config import LABEL_TIME, LABEL_1M, LABEL_15M, LABEL_1H


def get_main_kb(coinbase_invite: str, binance_invite: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=LABEL_TIME, callback_data=LABEL_TIME),
                InlineKeyboardButton(text=LABEL_1M, callback_data=LABEL_1M),
                InlineKeyboardButton(text=LABEL_15M, callback_data=LABEL_15M),
                InlineKeyboardButton(text=LABEL_1H, callback_data=LABEL_1H))
    builder.row(InlineKeyboardButton(text='open BINANCE', url=binance_invite),
                InlineKeyboardButton(text='open Coinbase', url=coinbase_invite))
    return builder.as_markup(resize_keyboard=True)
