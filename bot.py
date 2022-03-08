import os
import logging


from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('bot')


def start(update, context):
    user = update.effective_user
    update.message.reply_text('Hello!')


def echo(update, context):
    update.message.reply_text(update.message.text)


def main():
    env = Env()
    env.read_env('.env')
    tg_token = env('TG_TOKEN')
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo
    ))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
