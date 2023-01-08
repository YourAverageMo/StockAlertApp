import json

import pandas
import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = "HEY THIS IS MINE!"
NEWS_API_KEY = "dont touch my api key!"
YESTERDAY = "2023-01-06"
DAY_BEFORE = "2023-01-05"
PERCENT_CHANGE = 2


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_new_data():
    response = requests.get(
        url=
        f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK}&apikey={API_KEY}"
    )
    response.raise_for_status()
    daily_data = response.json()["Time Series (Daily)"]
    with open("stock_data.json", mode="w") as file:
        file.write(f"{daily_data}")


def get_news():
    response = requests.get(
        url=
        f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&searchIn=title&from=2023-01-05&sortBy=popularity&apiKey={NEWS_API_KEY}"
    )
    response.raise_for_status()
    news_data = response.json()["articles"]
    with open("news_data.json", "w") as f:
        three_articles = []
        for article in range(0, 3):
            try:
                three_articles.append(news_data[article])
            except IndexError:
                pass
        json.dump(three_articles, f)


def check_price_change():
    yesterdays_close = pandas.read_json(
        "./stock_data.json")[YESTERDAY]["4. close"]
    day_befores_close = pandas.read_json(
        "./stock_data.json")[DAY_BEFORE]["4. close"]

    if abs(yesterdays_close -
           day_befores_close) / yesterdays_close * 100 >= PERCENT_CHANGE:
        return True
    else:
        return False


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if check_price_change():
    get_news()
    # thats where im going to leave the project. if you want to print out the three articles just use pandas to read the news_data file -> make a list from it -> then access each dict printing out the data you need. this gets really redundant so ya...

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
