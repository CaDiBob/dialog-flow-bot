import logging

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
from dialog_flow import get_answer_dialogflow


logger = logging.getLogger('tg_bot')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, chat_id, bot):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update, context):
    update.message.reply_text('Здравствуйте! Чем можем помочь?')


def send_reply_message(update, context):
    project_id = context.bot_data['project_id']
    text = update.message.text
    chat_id = update.message.chat_id
    answer = get_answer_dialogflow(project_id, text, chat_id)
    update.message.reply_text(answer.query_result.fulfillment_text)


def error(update, context):
    logger.error(context.error)


def main():
    logger.setLevel(logging.INFO)
    env = Env()
    env.read_env('.env')
    project_id = env.str('PROJECT_ID')
    tg_token = env('TG_TOKEN')
    tg_chat_id = env('TG_CHAT_ID')
    updater = Updater(tg_token)
    bot = telegram.Bot(token=tg_token)
    logger.addHandler(TelegramLogsHandler(tg_chat_id, bot))
    dispatcher = updater.dispatcher
    dispatcher.bot_data['project_id'] = project_id
    dispatcher.bot_data['tg_chat_id'] = tg_chat_id
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, send_reply_message
    ))
    logger.info('Бот запущен!')
    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
