import requests
from twilio.rest import Client
from datetime import datetime as dt

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
percent_decrease = 0
amount_decrease = 0

up_down = None

account_sid = ""
auth_token = ""

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ENDPOIN_API_STOCKS =  ""
ENDPOIN_API_NEWS = ""
parameters_stocks = {
    "function":"TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey":ENDPOIN_API_STOCKS
}

parameters_news = {
    "apiKey": ENDPOIN_API_NEWS,
    "qInTitle": COMPANY_NAME,
}
date_today = dt.now()
date = date_today.date()

#function to get porcentage an amount of dollars dicrease
def difference(price_yesterday, price_day_before_y):
    global amount_decrease, percent_decrease
    amount_decrease = round(float(price_yesterday) - float(price_day_before_y), 6)
    global up_down 
    if amount_decrease < 0:
        up_down = "🔺"
    else:
        up_down = "🔻"
    percent_decrease = round(abs(amount_decrease)/ float(price_yesterday)*100,2)
    print(f"The diference is by {abs(amount_decrease)}, meaning to {percent_decrease}% difference")

#Getting API's info
stock_value_response = requests.get("https://www.alphavantage.co/query", params=parameters_stocks)
#print(stock_value_response.status_code)
stock_value_response.raise_for_status()
data_stock = stock_value_response.json()
#print(data_stock)
data_stocks = data_stock["Time Series (Daily)"]
#turning from dict into list
data_list = [value for (item,value) in data_stocks.items()]

#gettin yesterday's date
yesterday_data = data_list[0]
yesterday_price = yesterday_data['4. close']

#Getting day before yesterday
day_before_yesterday = data_list[1]
day_before_yesterday_price = day_before_yesterday["4. close"]

difference(yesterday_price, day_before_yesterday_price)
if percent_decrease > 1:
    print(f"Getting News")

    #Getting artichles of each news 
    response_news = requests.get(NEWS_ENDPOINT, params=parameters_news)
    data_news = response_news.json()["articles"][:3]
    #print(data_news)

    list_arthicles = [f"{STOCK}: {up_down}{percent_decrease}%\nHeadline: {artichle['title']}. \nBrief:{artichle['description']}" for artichle in data_news]
    #print(list_arthicles)
    print(f"I have ready the list artihcles ")
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
    client = Client(account_sid, auth_token)
        
    for arthicle in list_arthicles:
        message = client.messages.create(
            body=f"{arthicle}",
            from_='+',
            to='+'
        )
        print("\nMessage sent")
