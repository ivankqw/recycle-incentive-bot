import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# defining the states
FUCKOFF, FUCKYES = range(2)


# Define a few command handlers

def help(update: Update, context: CallbackContext) -> None:
    "send a message when command help is issued"
    s = "Hi and welcome"
    update.message.reply_text(s)
    reply_keyboard = [["/a", "/b", "/c"]]
    update.message.reply_text("More Commands:",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    update.message.reply_text(update.message.text)


def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [["/cashfortrash", "/ewaste", "/help"]]
    update.message.reply_text("Hi what would you like to recycle? You lil shit?",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


# entry points

def cashfortrash(update: Update, context: CallbackContext) -> None:
    t = "Welcome to Cash for Trash. You are Trash. Would you like to send your location?"
    update.message.reply_text(t)
    reply_keyboard = [["Yes", "No"]]
    update.message.reply_text("More Commands:",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def ewaste(update: Update, context: CallbackContext) -> None:
    t = ""
    update.message.reply_text(t)
    reply_keyboard = [["/a", "/b", "/c"]]
    update.message.reply_text("More Commands:",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def fuckoffcallback():
    return


def fuckyescallback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.data 
    return


def main() -> None:
    token = os.getenv("TOKEN")
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("cashfortrash", cashfortrash), CommandHandler("ewaste", ewaste)],
        states={
            FUCKOFF: [CallbackQueryHandler(fuckoffcallback)],
            FUCKYES: [CallbackQueryHandler(fuckyescallback)]
        }
    )

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
