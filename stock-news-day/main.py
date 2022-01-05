import os
from datetime import datetime
import time
import requests
from newsapi import NewsApiClient
import json
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
api_key = os.environ["API_KEY"]
api_endpoint = "https://www.alphavantage.co/query"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
    "apikey": api_key
}

response = requests.get(url=api_endpoint,params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]

data_list = [value for key,value in data.items()]
# list comprehension kullanarak str olan tarihleri almadık dict'ten list yaptık
##bu şekil yaptık çünkü dierinde tarih str olarak geliodu ve hafta sonlarını da işe katarsak gün değiştiğinde takibini yapmak
## zor olurdu otomatiğe bağlamak olmazdı çünki str olan bir tarihi değiştiricende hafta sonlarını atlayacaksında....
print(data_list) # içinde dict olan liste tarih kısımı yok


yesterday_dict = data_list[0]
day_before_yesterday_dict = data_list[1]
yesterday_dict_open = float(data_list[0]["1. open"])
day_before_yesterday_dict_open = float(data_list[1]["1. open"])
yesterday_dict_close = float(data_list[0]["4. close"])
day_before_yesterday_dict_close = float(data_list[1]["4. close"])



######################################################

new_api_key = os.environ["NEW_API_KEY"]

#new_api_endpoint = "https://newsapi.org/v2/everything"
newsapi = NewsApiClient(api_key=new_api_key)

everything = newsapi.get_everything(q='IBM',
                                       sources='bbc-news,the-verge',
                                       language='en')
# everything_json = json.dumps(everything) # json viewerda daha rahat görmek için json'a çevirdim KULLANMAMA GEREK YOK
only_articles = everything["articles"]

IBM_title_news = []
for data in only_articles[1:]:
    title = data["title"]
    content = data["content"]
    tuple_form = (title,content)
    IBM_title_news.append(tuple_form)
user = "mynewforpython@gmail.com"
pas_api = os.environ["PAS_API"]
to_addres = "forpythonmynew@yahoo.com"


### abs() sonucu pozitife çevirir yani -20 ise 20 yapar
if ((abs(yesterday_dict_close - yesterday_dict_open)) / yesterday_dict_open == 0.05) and ((abs(day_before_yesterday_dict_close-
    day_before_yesterday_dict_open)) / day_before_yesterday_dict_open == 0.05) or (abs((yesterday_dict_close - yesterday_dict_open)) / yesterday_dict_open == -0.05) and (abs((day_before_yesterday_dict_close-
    day_before_yesterday_dict_open)) / day_before_yesterday_dict_open == -0.05):
    with smtplib.SMTP(port=587, host="smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=user, password=pas_api)
        for mail in IBM_title_news:
            connection.sendmail(from_addr=user, to_addrs=to_addres,
                                msg=f"Subject: NEWS ABOUT IBM\n\nHEADLINE: {mail[0]}\ncontent: {mail[1]}")
            time.sleep(60)
else:
    with smtplib.SMTP(port=587, host="smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=user, password=pas_api)
        connection.sendmail(from_addr=user, to_addrs=to_addres,
                            msg=f"Subject: NEWS ABOUT IBM\n\nThere happened no sharp increase or decrease ")
