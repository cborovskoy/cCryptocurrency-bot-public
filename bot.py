from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, error


from work_with_files import get_new_and_old_charts
from settings import BINANCE_INVITE, COINBASE_INVITE, \
     get_path_chart, LABEL_TIME, LABEL_1M, LABEL_15M, LABEL_1H, get_tg_token


def get_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton(text=LABEL_TIME, callback_data=LABEL_TIME),
            InlineKeyboardButton(text=LABEL_1M, callback_data=LABEL_1M),
            InlineKeyboardButton(text=LABEL_15M, callback_data=LABEL_15M),
            InlineKeyboardButton(text=LABEL_1H, callback_data=LABEL_1H)
        ],
        [
            InlineKeyboardButton(text='open BINANCE', url=BINANCE_INVITE),
            InlineKeyboardButton(text='open Coinbase', url=COINBASE_INVITE)

        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard)


def alarm(context):
    try:
        context.bot.send_message(chat_id=6981917, text='test')
    except error.BadRequest:
        pass


def message_handler(update: Update, context: CallbackContext):

    try:
        if context.chat_data['job']:
            pass
    except Exception:
        new_job = context.job_queue.run_repeating(alarm, 600, context=6981917)
        context.chat_data['job'] = new_job


    send_chart(update=update, context=context, interval=LABEL_1M)




def callback_handler(update: Update, context: CallbackContext):
    callback_data = update.callback_query.data
    context.bot.edit_message_reply_markup(update.effective_user.id,
                                          message_id=context.chat_data['msg_id'])

    send_chart(update=update, context=context, interval=callback_data)


def send_chart(update: Update, context: CallbackContext, interval):
    paphs_chart = {
        LABEL_TIME: get_path_chart(LABEL_TIME),
        LABEL_1M: get_path_chart(LABEL_1M),
        LABEL_15M: get_path_chart(LABEL_15M),
        LABEL_1H: get_path_chart(LABEL_1H),
    }
    path = paphs_chart[interval]

    photo_path = get_new_and_old_charts(path=path)['new']
    price_now = photo_path.split('-')[-1][:-4]
    msg_txt = f"{price_now}$ - 1₿"

    msg = context.bot.send_photo(update.effective_user.id,
                                 photo=open(photo_path, 'rb'),
                                 caption=msg_txt,
                                 reply_markup=get_keyboard())

    context.chat_data['msg_id'] = msg.message_id


def main():
    updater = Updater(
        token=get_tg_token(), use_context=True
    )

    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
