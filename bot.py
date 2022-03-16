import os
import logging

import telegram
from google.cloud import dialogflow
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('bot')


def start(update, context):
    update.message.reply_text('Hello!')


def detect_intent_texts(update, context):
    project_id = context.bot_data['project_id']
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        project_id, session=update.message.chat_id,
    )
    text_input = dialogflow.TextInput(text=update.message.text, language_code='RU-ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    update.message.reply_text(response.query_result.fulfillment_text)


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
        Filters.text & ~Filters.command, detect_intent_texts
    ))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
