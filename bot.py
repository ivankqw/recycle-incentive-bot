import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler, \
    MessageHandler, Filters
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# defining the states
LOCATION = range(1)


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
    # update.message.reply_text(t)
    buttons = [[KeyboardButton("Send Location for Cash For Trash", request_location=True)]]
    update.message.reply_text(t,
                              reply_markup=ReplyKeyboardMarkup(buttons))
    # message = update.message
    # message.reply_text(f'you are at {message.location.latitude}, {message.location.longitude}')
    return LOCATION


def ewaste(update: Update, context: CallbackContext) -> None:
    t = ""
    update.message.reply_text(t)
    reply_keyboard = [["/a", "/b", "/c"]]
    update.message.reply_text("More Commands:",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def handle_callback(update: Update, context: CallbackContext) -> None:
    call = update.callback_query
    data = call.data
    if "send_location_cash_trash" in data:
        message = update.callback_query
        message.edit_message_text(f'you are at {message.location.latitude}, {message.location.longitude}')


def cancel():
    pass


def location(update: Update, context: CallbackContext) -> None:
    message = update.message
    curr_longitude = message.location['longitude']
    curr_latitude = message.location['latitude']
    message.reply_text(f'so you are at {curr_longitude}, {curr_latitude}')


def main() -> None:
    token = os.getenv("TOKEN")
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("cashfortrash", cashfortrash), CommandHandler("ewaste", ewaste)],
        states={
            LOCATION: [MessageHandler(Filters.location, location)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CallbackQueryHandler(handle_callback))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
