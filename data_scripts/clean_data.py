from math import nan
import pandas as pd


def convert_start_end(text):
    text = str(text).strip()
    time_formatter = {}
    # if both time_start and time_end empty, return
    if text == "nan":
        return
    h = text.find("H")
    if h != -1:
        text = text[:-1]
   # extract last 2 characters
    t = text[-2:]
    # print("t is:", t)

    colon_pos = text.find(":")
    new_time = 0

    if len(text) == 3:
        hours = text[0]
        minutes = 0
    elif len(text) == 4:
        hours = text[:2]
        minutes = 0
    elif len(text) == 6:
        hours = text[0]
        minutes = text[2:4]
    elif len(text) == 7:
        hours = text[:2]
        minutes = text[3:5]
    if t == "AM" or t == "am" or text == "12pm":
        new_time = int(hours)*100 + int(minutes)
    elif t == "PM" or t == "pm":
        new_time = 1200 + int(hours)*100 + int(minutes)
    else:
        new_time = text
    new_time = str(new_time)
    if len(new_time) == 3:
        new_time = "0" + new_time        
    return new_time


def main():
    df = pd.read_excel("data_with_coordinates.xlsx")
    new_time_start = df['Time_Start'].apply(convert_start_end)
    new_time_end = df['Time_End'].apply(convert_start_end)

    df["updated_time_start"] = new_time_start
    df["updated_time_end"] = new_time_end

    df.to_csv('cleaned_time.csv', index=False)

if __name__ == '__main__':
    main()
