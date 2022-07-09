import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler, \
    MessageHandler, Filters
from dotenv import load_dotenv
import os
import pandas as pd
from math import cos, sqrt, pi

load_dotenv()  # take environment variables from .env.
data_path = "./data/data_with_coordinates.xlsx"

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
    # message.reply_text(f'so you are at {curr_longitude}, {curr_latitude}, yes?')

    df = pd.read_excel(data_path, sheet_name="cash_for_trash")
    df['distances'] = df.apply(lambda x: distance(x['Longitude'], x['Latitude'], curr_longitude, curr_latitude), axis=1)
    result_df = df.sort_values('distances').iloc[0:5]
    address_list = result_df['Address'].tolist()
    day_list = result_df['Day'].tolist()
    time_start_list = result_df['updated_time_start'].tolist()
    time_end_list = result_df['updated_time_end'].tolist()
    s = ''
    for i in range(5):
        s += f'\n\n {i+1}. \n address: {address_list[i]} \n day: {day_list[i]} \n start: {time_start_list[i]} \n end: {time_end_list[i]}'
    message.reply_text(s)


def distance(lon1, lat1, lon2, lat2):
    R = 6371000  # radius of the Earth in m
    x = (lon2 - lon1) * cos(0.5*(lat2+lat1))
    y = (lat2 - lat1)
    return (2*pi*R/360) * sqrt( x*x + y*y )

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
