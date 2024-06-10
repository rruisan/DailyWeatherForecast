import os
from twilio.rest import Client
from twilio_config import *
import time

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from datetime import datetime


def get_forecast(response, i):
    date = response["forecast"]["forecastday"][0]["hour"][i]["time"].split()[0]
    hour = int(
        response["forecast"]["forecastday"][0]["hour"][i]["time"]
        .split()[1]
        .split(":")[0]
    )
    condition = response["forecast"]["forecastday"][0]["hour"][i]["condition"]["text"]
    temperature = response["forecast"]["forecastday"][0]["hour"][i]["temp_c"]
    will_rain = response["forecast"]["forecastday"][0]["hour"][i]["will_it_rain"]

    return date, hour, condition, temperature, will_rain


def get_weather_diary(response):
    diary_forecast = response["forecast"]["forecastday"][0]["hour"]
    weather_day_by_hour = []

    for i in range(len(diary_forecast)):
        weather_day_by_hour.append(get_forecast(response, i))

    return weather_day_by_hour


def create_dataframe(weather_day_by_hour):
    col = ["Date", "Hour", "Condition", "Temperature", "Rain"]
    dataframe_weather = pd.DataFrame(weather_day_by_hour, columns=col)

    return dataframe_weather


def filter_rain_important(df):
    df = df[(df["Rain"] == 1) & (df["Hour"] > 6) & (df["Hour"] < 22)]
    df = df[["Hour", "Condition"]]
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    df = df.to_string(index=False)
    return df


def send_message_twilio(mobile_message):
    time.sleep(2)
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=mobile_message, from_=PHONE_NUMBER, to=DESTINATION_PHONE_NUMBER
    )

    print("Message sent", message.sid)


def main():
    query = "Vitoria"
    api_key = API_KEY_WAPI
    url_weather = (
        "http://api.weatherapi.com/v1/forecast.json?key="
        + api_key
        + "&q="
        + query
        + "&days=1&aqi=no&alerts=no"
    )

    response = requests.get(url_weather).json()
    
    weather_day_by_hour = get_weather_diary(response)
    df_weather_day_by_hour = create_dataframe(weather_day_by_hour)
    df_filtered = filter_rain_important(df_weather_day_by_hour)

    mobile_message = (
        "\nHi, todays forecast "
        + df_weather_day_by_hour["Date"][0]
        + " in "
        + query
        + " is: \n\n "
        + str(df_filtered)
    )
    
    send_message_twilio(mobile_message)


if __name__ == "__main__":
    main()
