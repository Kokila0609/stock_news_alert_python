import requests
from datetime import datetime, timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

API_KEY = "WKFCF7VPNXZ4RBN7"
NEWS_API_KEY = "21a0faecedbb474380ca6996b6512b29"

def get_previous_weekday(start_day, days_back):
    current_date = start_day
    count = 0
    while count<days_back:
        current_date -=timedelta(days=1)
        
        if current_date.weekday()<5:
            count +=1
    return current_date  

def calc_percentage(new_data, old_data):
    if new_data>old_data:
        percentage = round(((new_data-old_data)/new_data)*100)
        return f"🔺{percentage}%"
    else:
        percentage = round(((old_data-new_data)/new_data)*100) 
        return f"🔺{percentage}%"


stock_params = {
    "apikey": "WKFCF7VPNXZ4RBN7",
    "symbol": "TSLA",
    "function": "TIME_SERIES_DAILY",
}

news_params = {
    "q": "STOCK",
    "apikey": NEWS_API_KEY,

}

today = datetime.now()
# print(type(today.weekday()))
yesterday = get_previous_weekday(today, 1)
yesterday = yesterday.strftime('%Y-%m-%d')
day_before_yesterday = get_previous_weekday(today,2)
day_before_yesterday = day_before_yesterday.strftime('%Y-%m-%d')
today =  today.strftime('%Y-%m-%d')
# print(today)
# print(yesterday)
# print(day_before_yesterday)

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and 
# the day before yesterday then print("Get News").

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
stock_data = response.json()
news_response = requests.get(NEWS_ENDPOINT, params=news_params)
news_response.raise_for_status()
news_data = news_response.json()
collated_news_data = news_data["articles"][:3]


new_value = (stock_data["Time Series (Daily)"][yesterday]['4. close'])
old_value = (stock_data["Time Series (Daily)"][day_before_yesterday]['4. close'])
stock_change_percentage = calc_percentage(float(new_value), float(old_value))


if any(word == "5" for word in stock_change_percentage):
    for news in collated_news_data:
        headline = news["title"]
        brief = news["description"]
        print(f"TSLA: {stock_change_percentage}")
        print(f"Headline: {headline}")
        print(f"Brief: {brief}")

#HINT 1: Get the closing price for yesterday and the day before yesterday. 
# Find the positive difference between the two prices. e.g. 40 - 20 = -20,
#  but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price. 



## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator



## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.



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

