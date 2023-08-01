from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, BufferedInputFile

from src.config import LABEL_1M, LABEL_TIME, LABEL_15M, LABEL_1H, CT_LINE, CT_CANDLESTICK, load_config
from src.keyboards.main_kb import get_main_kb
from src.service.charts import make_chart

router = Router()


@router.message()
async def all_msg_handler(message: Message):
    await send_chart(bot=message.bot, user_id=message.from_user.id, interval=LABEL_1M)


@router.callback_query()
async def all_cb_handler(callback: CallbackQuery):
    await send_chart(user_id=callback.from_user.id, bot=callback.bot, interval=callback.data,
                     msg_id=callback.message.message_id)
    await callback.answer()


async def send_chart(user_id, bot: Bot, interval, msg_id=None):
    charts_data = {LABEL_TIME: {'chart_type': CT_LINE, 'candle_time': None},
                   LABEL_1M: {'chart_type': CT_CANDLESTICK, 'candle_time': '1T'},
                   LABEL_15M: {'chart_type': CT_CANDLESTICK, 'candle_time': '15T'},
                   LABEL_1H: {'chart_type': CT_CANDLESTICK, 'candle_time': '1H'}}

    chart_data = charts_data[interval]
    chart_img_bytes, last_price = make_chart(chart_type=chart_data['chart_type'], candle_time=chart_data['candle_time'])
    chart_img = BufferedInputFile(chart_img_bytes, filename="chart.png")
    msg_txt = f"{last_price}$ - 1₿"

    config = load_config()
    kb = get_main_kb(coinbase_invite=config.coinbase_invite, binance_invite=config.binance_invite)

    if msg_id is None:
        await bot.send_photo(chat_id=user_id, photo=chart_img, caption=msg_txt, reply_markup=kb)
    else:

        await bot.edit_message_media(chat_id=user_id, message_id=msg_id, reply_markup=kb,
                                     media=InputMediaPhoto(media=chart_img, caption=msg_txt))
