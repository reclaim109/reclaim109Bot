import logging
import os

import re
from telegram import Update
from telegram.ext import Filters, MessageHandler, Updater, CommandHandler, CallbackContext

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

TOKEN = os.getenv("TOKEN")


def run(updater):
    port = int(os.environ.get("PORT", "8443"))
    heroku_app_name = os.environ.get("HEROKU_APP_NAME")
    logger.info("Starting webhook for {}".format(heroku_app_name))
    # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
    updater.start_webhook(listen="0.0.0.0",
                          port=port,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(heroku_app_name, TOKEN))


def start(update, context):
    """Send a message when the command /start is issued."""
    logger.info("User {} started bot".format(update.effective_user["first_name"]))
    update.message.reply_text('http://hundertneun.net/')


def message_response_handler(update: Update, context: CallbackContext):
    # Creating a handler-function for /start command
    if re.search('goldhorn', update.message.text, re.IGNORECASE):
        update.message.reply_text("zur Info: http://hundertneun.net/", ('quote', True))


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, message_response_handler))

    run(updater)