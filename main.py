import requests
import datetime
from twilio.rest import Client
import os

# -------------------------------------- CONSTANTS ----------------------------------------------
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")


# ------------------------------------- SEND MESSAGE --------------------------------------------
def send_message(profit_loss):
    today = datetime.datetime.now()
    news_api_parameters = {
        "q": "Tesla",
        "from": str(today - datetime.timedelta(days=2)).split(" ")[0],
        "to": str(today).split(" ")[0],
        "sortBy": "popularity",
        "domains": "techcrunch.com,forbes.com,reuters.com,bloomberg.com,electrek.co,insideevs.com,wsj.com,bbc.com,"
                   "cnn.com,theverge.com",
        "apiKey": NEWS_API_KEY
    }

    news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_api_parameters)
    news_response.raise_for_status()

    news_1 = (f"Headline: {news_response.json()['articles'][0]['title']} \n"
              f"Brief: {news_response.json()['articles'][0]['description']}")

    news_2 = (f"Headline: {news_response.json()['articles'][1]['title']} \n"
              f"Brief: {news_response.json()['articles'][1]['description']}")

    news_3 = (f"Headline: {news_response.json()['articles'][2]['title']} \n"
              f"Brief: {news_response.json()['articles'][2]['description']}")

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # Sending messages
    for news in [news_1, news_2, news_3]:
        message = client.messages.create(
            body=f"{STOCK}: {profit_loss} {news}",
            from_=TWILIO_NUMBER,
            to="+917093943408",
        )
        print(message.status)


# ------------------------------------- IMPLEMENTATION --------------------------------------------
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHAVANTAGE_API_KEY
}
stock_price_response = requests.get(url="https://www.alphavantage.co/query", params=stock_parameters)
stock_price_response.raise_for_status()

today_date = datetime.datetime.now()
yesterday = str(today_date - datetime.timedelta(days=1)).split(" ")[0]
day_before_yesterday = str(today_date - datetime.timedelta(days=2)).split(" ")[0]

yesterday_close = float(stock_price_response.json()["Time Series (Daily)"][yesterday]["4. close"])
previous_close = float(stock_price_response.json()["Time Series (Daily)"][day_before_yesterday]["4. close"])

print(yesterday_close)
print(previous_close)

price_change = yesterday_close - previous_close
price_change_percentage = (price_change / previous_close) * 100

if price_change_percentage > 5:
    profit = f"🔺{price_change_percentage:.2f}%"
    print(f"Profit: {profit}")
    send_message(profit)
elif price_change_percentage < -5:
    loss = f"🔻{abs(price_change_percentage):.2f}%"
    send_message(loss)
