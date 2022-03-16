import os
import logging

import telegram
from google.cloud import dialogflow
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
from dialog_flow import answer_dialogflow


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('bot')


def start(update, context):
    update.message.reply_text('Hello!')


def send_message(update, context):
    project_id = context.bot_data['project_id']
    text = update.message.text
    chat_id = update.message.chat_id
    update.message.reply_text(answer_dialogflow(project_id, text, chat_id))


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
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, send_message
    ))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
