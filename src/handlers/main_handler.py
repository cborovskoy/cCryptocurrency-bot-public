from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, BufferedInputFile

from src.config import load_config, LABEL_1H, LABEL_15M, LABEL_1M
from src.utils.keyboards import get_main_kb
from src.utils.charts import make_chart
from src.utils.price import get_historical_price

router = Router()


@router.message()
async def all_msg_handler(message: Message, state: FSMContext):
    await message.delete()
    await send_chart(bot=message.bot, user_id=message.from_user.id, state=state)


@router.callback_query()
async def all_cb_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(interval=callback.data)
    await send_chart(user_id=callback.from_user.id, bot=callback.bot, state=state, bot_msg_to_edit=callback.message)
    await callback.answer()


async def send_chart(user_id: int, bot: Bot, state: FSMContext, bot_msg_to_edit: Message = None):
    state_data = await state.get_data()
    interval: str = state_data.get('interval', LABEL_1H)
    await state.update_data(interval=interval)

    period = {LABEL_1M: 1, LABEL_15M: 2, LABEL_1H: 3}[interval]
    hist_df = await get_historical_price(period_in_days=period, interval=interval)

    chart_img_bytes = await make_chart(df=hist_df)
    chart_img = BufferedInputFile(chart_img_bytes, filename="chart.png")

    last_price = round(hist_df.tail(1)['Close'].item(), 2)
    text = f"{last_price}$ - 1₿"

    config = load_config()
    kb = get_main_kb(coinbase_invite=config.coinbase_invite, binance_invite=config.binance_invite, interval=interval)

    if bot_msg_to_edit is None:
        await bot.send_photo(chat_id=user_id, photo=chart_img, caption=text, reply_markup=kb)
    else:
        await bot_msg_to_edit.edit_media(media=InputMediaPhoto(media=chart_img, caption=text), reply_markup=kb)
