import logging
import sys
import traceback

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
from dialog_flow import get_answer_dialogflow


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Здравствуйте! Чем можем помочь?')


def send_reply_message(update, context):
    project_id = context.bot_data['project_id']
    text = update.message.text
    chat_id = update.message.chat_id
    answer = get_answer_dialogflow(project_id, text, chat_id)
    update.message.reply_text(answer.query_result.fulfillment_text)


def error(update, context):
    payload = list()
    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    chat_id = context.bot_data['tg_chat_id']
    text = f'Ошибка {context.error} случилась{"".join(payload)}. ' \
           f'Полная трассировка:\n\n{trace}'
    context.bot.send_message(chat_id, text)


def main():
    env = Env()
    env.read_env('.env')
    project_id = env.str('PROJECT_ID')
    tg_token = env('TG_TOKEN')
    tg_chat_id = env('TG_CHAT_ID')
    updater = Updater(tg_token)
    bot = telegram.Bot(token=tg_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['project_id'] = project_id
    dispatcher.bot_data['tg_chat_id'] = tg_chat_id
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, send_reply_message
    ))
    dispatcher.add_error_handler(error)
    logger.info('Бот запущен!')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
