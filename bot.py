import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def help(update: Update, context: CallbackContext) -> None:
    "send a message when command help is issued"
    s = "Hi and welcome"
    update.message.reply_text(s)
    reply_keyboard = [["/a", "/b", "/c"]]
    update.message.reply_text("More Commands:",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    update.message.reply_text(update.message.text)


# Define a few command handlers
def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [["/a", "/b"]]
    update.message.reply_text("Choose a or b?",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def a(update: Update, context: CallbackContext) -> None:
    t = ""
    update.message.reply_text(t)
    reply_keyboard = [["/a", "/b", "/help"]]
    update.message.reply_text("More Commands:",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def b(update: Update, context: CallbackContext) -> None:
    t = ""
    update.message.reply_text(t)
    reply_keyboard = [["/a", "/b", "/c"]]
    update.message.reply_text("More Commands:",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def main() -> None:
    token = os.getenv("TOKEN")
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("a", a))
    dispatcher.add_handler(CommandHandler("b", b))
    dispatcher.add_handler(CommandHandler("help", help))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
