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
    s1 = "<u> What is this bot for? </u> \n\n Did you know that you can get cash incentives for simply recycling? Do your part for the environment with us today 😊! It's easy to r(easy)cle like 1 2 3!<br><br>"
    s2 = "<u> Key Features </u> \n\n <ul> <li>Find your nearest recycling locations</li> </ul><br><br>"
    s3 = "<u> What is Cash For Trash? </u> <br><br> Cash-for-Trash is an incentive programme by Public Waste Collectors, where residents may bring their recyclables to the Cash-for-Trash stations and cash is given in exchange for recyclables. More information <a href='https://www.nea.gov.sg/our-services/waste-management/3r-programmes-and-resources/recycling-collection-points'>here</a>. <br><br>"
    s4 = "<u> What is the E-Waste recyling program? </u> <br><br> E-Waste is your mother"
    reply_keyboard = [["/cashfortrash", "/ewaste"]]
    update.message.reply_text(s1 + s2 + s3 + s4,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def start(update: Update, context: CallbackContext) -> None:
    s = "Welcome to the Recycle Incentive Bot! We are glad to have you here today 🌻🌼🌷🌸💮🌹🥀\n\n Click on /help to find out more about this bot or get started by clicking on the following buttons!"
    reply_keyboard = [["/cashfortrash", "/ewaste"]]
    update.message.reply_text(s,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), parse_mode='HTML')


# entry points

def cashfortrash(update: Update, context: CallbackContext) -> None:
    t = "Welcome to Cash for Trash. You are Trash. Would you like to send your location?"
    # update.message.reply_text(t)
    buttons = [[KeyboardButton("Send Location for Cash For Trash", request_location=True)]]
    update.message.reply_text(t,
                              reply_markup=ReplyKeyboardMarkup(buttons))
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

    df = pd.read_excel(data_path, sheet_name="cash_for_trash", converters={'updated_time_start': str, 'updated_time_end': str})
    df['updated_time_start'] = df['updated_time_start'].apply(lambda x: "0" + str(x) if len(str(x)) == 3 else str(x))
    df['updated_time_end'] = df['updated_time_end'].apply(lambda x: "0" + str(x) if len(str(x)) == 3 else str(x))
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
