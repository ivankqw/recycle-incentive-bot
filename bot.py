import logging
from tkinter import Button
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
LOCATION, LOCATIONEWASTE, EWASTESELECT = range(3)

ewaste_item = 0


# Define a few command handlers

def help(update: Update, context: CallbackContext) -> None:
    "send a message when command help is issued"
    s1 = "<b>🌟What is Re(easy)cle?🌟 </b> \n\nDid you know that you can get cash incentives for simply recycling? Do your part for the environment with us today 😊! It's easy to r(easy)cle like 1 2 3🥳\n\n"
    s2 = "<b><u>Key Features </u></b> \n 1️⃣ Find your nearest recycling locations based on category \n 2️⃣ Updated with latest locations from NEA\n 3️⃣ This service is fully automated and available 24/7\n\n"
    s3 = "<b><u>What is Cash For Trash? </u></b> \nCash-for-Trash is an incentive programme by Public Waste Collectors, where residents may bring their recyclables to the Cash-for-Trash stations and cash is given in exchange for recyclables. More information <a href='https://www.nea.gov.sg/our-services/waste-management/3r-programmes-and-resources/recycling-collection-points'>here</a>.\n\n"
    s4 = "<b><u>What is the E-Waste National Recyling Program? </u></b>\nE-waste is electrical and electronic equipment of any kind that has been discarded. Under this programme launched in April 2001, the public waste collectors (PWCs) licensed by NEA are required to provide recycling bins and recycling collection services to all HDB estates, private landed properties and condominiums/private apartments opted into the public waste collection scheme. More information <a href='https://www.nea.gov.sg/our-services/waste-management/3r-programmes-and-resources/e-waste-management'>here</a>."
    reply_keyboard = [["/cashfortrash", "/ewaste"]]
    update.message.reply_text(s1 + s2 + s3 + s4,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),parse_mode='HTML')

    return ConversationHandler.END

def start(update: Update, context: CallbackContext) -> None:
    s = "🌸🌼🌻Welcome to the Re(easy)cle! We are glad to have you here today 🌻🌼🌸\n\n Click on /help to find out more about this bot or get started by clicking on the following buttons!"
    reply_keyboard = [["/cashfortrash", "/ewaste"]]
    update.message.reply_text(s,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), parse_mode='HTML')


# entry points

def cashfortrash(update: Update, context: CallbackContext) -> None:
    t = "Welcome to Cash for Trash Point Finder 💰 Send me your location so that I can locate your nearest Cash for Trash collection points!"
    # update.message.reply_text(t)
    buttons = [[KeyboardButton("Send Location 📍 for Cash For Trash 💰", request_location=True)]]
    update.message.reply_text(t,
                              reply_markup=ReplyKeyboardMarkup(buttons))
    return LOCATION


def ewaste(update: Update, context: CallbackContext) -> None:
    t = "Welcome to E-waste Point Finder 🤖 Please select the type of item that you would like to recycle."
    update.message.reply_text(t)
    buttons = [
        [KeyboardButton("💻 ICT")],
        [KeyboardButton("🔋 Batteries")],
        [KeyboardButton("🛋️ Lamps")],
        [KeyboardButton("🔵 Regulated")],
        [KeyboardButton("🍎 Non-regulated")],
    ]
    update.message.reply_text("Type of item:",
                              reply_markup=ReplyKeyboardMarkup(buttons))
    return EWASTESELECT


def ewaste_select(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'{update.message.text} Selected!')

    global ewaste_item
    ewaste_item = update.message.text[2:]

    buttons = [[KeyboardButton("Send Location 📍 for E-Waste 🤖", request_location=True)]]
    update.message.reply_text("Send me your location so that I can locate your nearest E-waste collection points!", reply_markup=ReplyKeyboardMarkup(buttons))
    return LOCATIONEWASTE


def cancel():
    pass


def location(update: Update, context: CallbackContext) -> None:
    message = update.message
    curr_longitude = message.location['longitude']
    curr_latitude = message.location['latitude']
    directions_base_url = 'https://www.google.com/maps/dir/?api=1&destination='

    df = pd.read_excel(data_path, sheet_name="cash_for_trash",
                       converters={'updated_time_start': str, 'updated_time_end': str})
    df['updated_time_start'] = df['updated_time_start'].apply(lambda x: "0" + str(x) if len(str(x)) == 3 else str(x))
    df['updated_time_end'] = df['updated_time_end'].apply(lambda x: "0" + str(x) if len(str(x)) == 3 else str(x))
    df['distances'] = df.apply(lambda x: distance(x['Longitude'], x['Latitude'], curr_longitude, curr_latitude), axis=1)
    result_df = df.sort_values('distances').iloc[0:5]

    long_list = result_df['Longitude'].tolist()
    lat_list = result_df['Latitude'].tolist()
    directions_list = [directions_base_url + str(x) + "," + str(y) for x, y in zip(lat_list, long_list)]
    address_list = result_df['Address'].tolist()
    day_list = result_df['Day'].tolist()
    time_start_list = result_df['updated_time_start'].tolist()
    time_end_list = result_df['updated_time_end'].tolist()
    s = 'Here are your current top 5 nearest Cash For Trash locations! 🚮😸'
    for i in range(5):
        s += f'\n\n {i + 1}. \n <u>Address: {address_list[i]}</u> \n Collection day(s): {day_list[i]} \n Start Time: {time_start_list[i]} \n End Time: {time_end_list[i]} \n\n <b>Get Directions: {directions_list[i]}</b>'
    message.reply_text(s, parse_mode='HTML')
    
    return ConversationHandler.END

def location_ewaste(update: Update, context: CallbackContext) -> None:
    message = update.message
    curr_longitude = message.location['longitude']
    curr_latitude = message.location['latitude']

    directions_base_url = 'https://www.google.com/maps/dir/?api=1&destination='

    df = pd.read_excel(data_path, sheet_name="e_waste")
    df = df.loc[df[ewaste_item]]
    df['distances'] = df.apply(lambda x: distance(x['Longitude'], x['Latitude'], curr_longitude, curr_latitude), axis=1)
    result_df = df.sort_values('distances').iloc[0:5]

    long_list = result_df['Longitude'].tolist()
    lat_list = result_df['Latitude'].tolist()
    directions_list = [directions_base_url + str(x) + "," + str(y) for x, y in zip(lat_list, long_list)]
    address_list = result_df['Location'].tolist()

    s = f'Here are your current top 5 nearest E-Waste recycling locations ({ewaste_item})! 🚮😸'

    if len(address_list) < 5:
        for i in range(1):
            s += f'\n\n {i + 1}. \n <u>Address: {address_list[i]}</u> \n \n\n <b>Get Directions</b>: {directions_list[i]}'
    else:
        for i in range(5):
            s += f'\n\n {i + 1}. \n <u>Address: {address_list[i]}</u> \n \n\n <b>Get Directions</b>: {directions_list[i]}'
    message.reply_text(s, parse_mode='HTML')
    return ConversationHandler.END



def distance(lon1, lat1, lon2, lat2):
    R = 6371000  # radius of the Earth in m
    x = (lon2 - lon1) * cos(0.5 * (lat2 + lat1))
    y = (lat2 - lat1)
    return (2 * pi * R / 360) * sqrt(x * x + y * y)


def main() -> None:
    token = os.getenv("TOKEN")
    updater = Updater(token)
    j = updater.job_queue

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("cashfortrash", callback=cashfortrash),
                      CommandHandler("ewaste", callback=ewaste)],
        states={
            LOCATION: [MessageHandler(Filters.location, callback=location)],
            LOCATIONEWASTE: [MessageHandler(Filters.location, callback=location_ewaste)],
            EWASTESELECT: [MessageHandler(Filters.text, callback=ewaste_select)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)
    # dispatcher.add_handler(CallbackQueryHandler(handle_callback))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
