from django.shortcuts import render
from django.conf import settings

from sentiment_analysis_app import forms

import requests
import re
import numpy
import pandas as pd
from datetime import datetime as dt
import datetime
import os
from textblob import TextBlob
import matplotlib.pyplot as plt

from matplotlib.dates import DateFormatter 

BEARER_TOKEN ="AAAAAAAAAAAAAAAAAAAAAPTjLAEAAAAAKh0Mtws1SooymTlc4NUjL7GbYk4%3DJdg31lv1aUdPukS2LWQtcwEpdNrxIo4Qryt0NVOHcgtAMnr5nt"
IGNORE_NEUTRAL_TWEETS = True

def clean_tweet(tweet): 
    ''' 
    Utility function to clean tweet text by removing links, special characters 
    using simple regex statements. 
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

def get_day_month_year(tweet_date_time):
    #d = datetime.date(tweet_date_time)
    d = dt.strptime(tweet_date_time, "%a %b %d %H:%M:%S %z %Y")

    yr = str(d.year)
    mnth = str(d.month)
    day=str(d.day)
    return(datetime.datetime(d.year, d.month, d.day))



def get_tweet_sentiment(tweet_text):
    analysis = TextBlob(tweet_text)
    sentiment_polarity_score = analysis.sentiment.polarity
    # set sentiment 
    if analysis.sentiment.polarity > 0.25: 
        sentiment = 'Positive'
    elif analysis.sentiment.polarity < 0: 
        sentiment =  'Negative'
    else: 
        sentiment = 'Neutral'
    return (sentiment_polarity_score, sentiment)




def get_data(tweet):
    tweet_text = clean_tweet(tweet['full_text'])
    sentiment_polarity_score, sentiment = get_tweet_sentiment(tweet_text)

    if IGNORE_NEUTRAL_TWEETS == True and sentiment =='Neutral':
        return ''
    
    
    data = {'Tweet Id': tweet['id_str'],
            'Tweet Date': get_day_month_year(tweet['created_at']),
            'Tweet Text': tweet_text,
            'Tweet Sentiment':sentiment,
            'sentiment_polarity_score': sentiment_polarity_score
            }
    return data




# Create your views here.

def index(request):
    # try:
    if request.method=='GET':
        return render(request, 'sentiment_analysis_app/index.html',  {'user_sentiment_analysis_form': forms.SentimentEntryForm()})
    
    if request.method=='POST':
        user_sentiment_analysis_form = forms.SentimentEntryForm(request.POST)

        if user_sentiment_analysis_form.is_valid():
            stock_symbl = user_sentiment_analysis_form.cleaned_data['stock_symbl']
            sentiment_txt = user_sentiment_analysis_form.cleaned_data['sentiment_txt']

            twitter_sentiment_Fig_URL = ''
            stock_price_fig_URL=''

            fn_successful, stock_price_fig_URL = get_stock_prices(stock_symbl)
            if fn_successful==True:
                twitter_sentiment_Fig_URL = get_twitter_sentiment(sentiment_txt)
            

            context={
                'twitter_sentiment_Fig_URL':twitter_sentiment_Fig_URL,
                'stock_price_fig_URL':stock_price_fig_URL,
            }
            return render(request, 'sentiment_analysis_app/result.html',  context)


    # except BaseException as e:
    #    print("Error", e)


def get_twitter_sentiment(twittertxt):
    params = {
        'q': twittertxt,
        'tweet_mode': 'extended',
        'result_type':'mixed',
        'lang': 'en',
        'count': '100'
        }
    response = requests.get(
                    'https://api.twitter.com/1.1/search/tweets.json',
                    params=params,
                    headers={'authorization': 'Bearer '+BEARER_TOKEN}
                )

    # Create an Empty data frame

    df = pd.DataFrame()

    for tweet in response.json()['statuses']:
        row = get_data(tweet)
        if row !='' :
            df = df.append(row, ignore_index=True)
    
    df_summary = df.groupby(["Tweet Date", "Tweet Sentiment"])[["Tweet Sentiment"]].count().unstack()
    axes = df_summary.plot(kind="bar", color=['red', 'CornflowerBlue', 'purple'])

    
    axes.set_xlabel ('Tweet Sentiment Date')
    axes.set_ylabel ('Tweet Count')
    axes.set_title('Tweet sentiment of ' + twittertxt, loc='center', pad=15)

    date_form = DateFormatter("%d-%b")
    axes.xaxis.set_major_formatter(date_form)

    plt.xticks(rotation="45")

    """
    plt.title("Tweet Sentiment Analysis")
    plt.xlabel("Tweet Date")
    plt.ylabel("Tweet Sentiment")
    
    """
    
    USER_FILES_ROOT = getattr(settings, "USER_FILES_ROOT", None)

    now = dt.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    filePath = os.path.join(USER_FILES_ROOT, "image" + dt_string + ".png")
    plt.savefig(filePath)
    USER_FILES_URL = getattr(settings, "USER_FILES_URL", None)
    fileURL =    USER_FILES_URL + "image" + dt_string + ".png"
    return fileURL

def get_stock_prices(stock_symbl):
    API_KEY = "4X2KS13Z6U46J4BI"
    DAYS_DATA = 8

    # response = requests.get("https://www.alphavantage.co/query?function=SMA&symbol=BSE:"+stock_symbl+ "&interval=weekly&time_period=10&series_type=open&apikey="+ API_KEY)
    try:
        response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BSE:"+stock_symbl+ "&apikey="+ API_KEY)
        data_list = list(response.json()["Time Series (Daily)"])

    except KeyError:
         # This means this Stock Symbol does not exist
        return (False, '')


    try:

        stock_df = pd.DataFrame()
        date_today= datetime.date.today()
        # json_response = response.json()["Technical Analysis: SMA"]
        json_response = response.json()["Time Series (Daily)"]

        data_list = list(json_response)
        for item in data_list:
            #print(item)
            dict = json_response[item]
            stock_price_date = convert_to_date(item)
            delta = date_today - stock_price_date
            if delta.days <= DAYS_DATA:
                #dict = json_response[data_list[0]]
                #print(dict["SMA"])
                row={
                    'Date':stock_price_date,
                    'Close Price':dict["4. close"]
                }
                stock_df = stock_df.append(row, ignore_index=True)


        # convert column "SMA" of a DataFrame
        stock_df["Close Price"] = pd.to_numeric(stock_df["Close Price"])

        stock_df['Date']= pd.to_datetime(stock_df['Date'])

        axes = stock_df.plot(x="Date", y="Close Price")
        axes.set_xlabel ('Share price date')
        axes.set_ylabel ('Closing Share price in Rs')
        axes.set_title('Share price of ' + stock_symbl + ' over the past ' + str(DAYS_DATA) + " days", loc='center', pad=15)

        date_form = DateFormatter("%d-%b")
        axes.xaxis.set_major_formatter(date_form)

    

        USER_FILES_ROOT = getattr(settings, "USER_FILES_ROOT", None)

        now = dt.now()
        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
        filePath = os.path.join(USER_FILES_ROOT, "image" + dt_string + ".png")
        plt.savefig(filePath)
        USER_FILES_URL = getattr(settings, "USER_FILES_URL", None)
        fileURL =    USER_FILES_URL + "image" + dt_string + ".png"
        return (True, fileURL)

    except BaseException as e:
        return (False, '')
    


def convert_to_date(string_date):
    d = dt.strptime(string_date, "%Y-%m-%d")
    
    yr = str(d.year)
    mnth = str(d.month)
    day=str(d.day)
    return(datetime.date(d.year, d.month, d.day))

