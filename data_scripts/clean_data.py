import pandas as pd


def convert_start_end(text):
    time_formatter = {}
    # if both time_start and time_end empty, return
    if not text:
        return text
    # extract last 2 characters
    t = text[-2:]
    if t == "PM" or t == "pm":
        colon_pos = t.find(":")
        if colon_pos != -1:
            hours = t[:colon_pos]
            minutes = t[colon_pos + 1:-2]
            return
    elif t == "AM" or t == "am":
        pass
    return


def main():
    df = pd.read_excel("../data/data.xlsx")
    df['Time_start'] = df['Time_Start'].apply(convert_start_end)
    df['Time_End'] = df['Time_End'].apply(convert_start_end)


if __name__ == '__main__':
    main()
