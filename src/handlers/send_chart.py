from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, BufferedInputFile

from src.config import load_config, LABEL_1H, LABEL_15M, LABEL_1M
from src.keyboards.main_kb import get_main_kb
from src.service.charts import make_chart
from src.service.price import get_historical_price

router = Router()


@router.message()
async def all_msg_handler(message: Message):
    await message.delete()
    await send_chart(bot=message.bot, user_id=message.from_user.id)


@router.callback_query()
async def all_cb_handler(callback: CallbackQuery):
    await send_chart(user_id=callback.from_user.id, bot=callback.bot, interval=callback.data,
                     msg_id=callback.message.message_id)
    await callback.answer()


async def send_chart(user_id, bot: Bot, interval: str = LABEL_1H, msg_id=None):
    period = {LABEL_1M: '1d', LABEL_15M: '2d', LABEL_1H: '3d'}[interval]
    hist_df = await get_historical_price(period=period, interval=interval)

    chart_img_bytes = await make_chart(df=hist_df)
    chart_img = BufferedInputFile(chart_img_bytes, filename="chart.png")

    last_price = round(hist_df.tail(1)['Close'].item(), 2)
    msg_txt = f"{last_price}$ - 1₿"

    config = load_config()
    kb = get_main_kb(coinbase_invite=config.coinbase_invite, binance_invite=config.binance_invite)

    if msg_id is None:
        await bot.send_photo(chat_id=user_id, photo=chart_img, caption=msg_txt, reply_markup=kb)
    else:
        await bot.edit_message_media(chat_id=user_id, message_id=msg_id, reply_markup=kb,
                                     media=InputMediaPhoto(media=chart_img, caption=msg_txt))
