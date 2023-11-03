import os
from dotenv import load_dotenv
import requests
import smtplib
import html

load_dotenv()

# Function to send email
def send_email(to_addr: str, article_lists: list):
    user = "rzmobiledev@gmail.com"
    port = 587
    smtp = "smtp.gmail.com"
    password = os.environ.get("GMAIL_API_KEY")

    change_ascii_char = "\u2019"

    for article in article_lists:

        article.replace(change_ascii_char, "-")
        with smtplib.SMTP(host=smtp, port=port) as connect:
            connect.starttls()
            connect.login(user=user, password=password)
            connect.sendmail(from_addr=user, to_addrs=to_addr, msg=f"Subject:New Stock Headline Update\n\n{html.unescape(article)}")
            print("email sent successfully")


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

# STEP 1: Use http://www.alphavantage.co/documentation/#daily
# when stock price increases/decreases by 5% between yesterday and the day before yesterday then
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": COMPANY_NAME
}

news_params = {
    "q": STOCK_NAME,
    "apiKey": NEWS_API_KEY
}

# 1. - Get yesterday's closing stock price
response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']

# 2. - Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']

# 3. - Find the positive difference between 1 and 2. eg. 40 - 20 = -20, but the possitive is 20. hints https://www.w3school.com/python?ref_func_abs
difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))

# 4. - Work out the value of 5% of yesterday's closing price
diff_percent = (difference / float(yesterday_closing_price)) * 100

# 5. - if 4 percentage is greater than 5 then print("Get the first 3 news pieces for the company name.")
if diff_percent > 5:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()['articles']

    # 6. - Use python slice operator to create a list than contains the first 3 articles.
    three_articles = (articles[:3])

    # 7. - Create a new list of the first 3 article's headline and description using list comprehension
    formated_articles = [f"headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    # TODO 8. - Send each article as a separate message via twilio
    send_email("rizal.safril@gmail.com", article_lists=formated_articles)



